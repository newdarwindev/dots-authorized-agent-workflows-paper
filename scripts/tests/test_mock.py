"""Evidence rejection, real HTTP execution, failure cleanup and clock boundaries."""
import copy
import datetime as dt
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mock as cli
import mock_contract as c
import mock_http as h


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init','-q')
        self.git('config','user.email','synthetic@example.invalid')
        self.git('config','user.name','Synthetic test')
        (self.root/'README').write_text('synthetic')
        self.git('add','README')
        self.git('commit','-qm','initial')
        self.sha = self.git('rev-parse','HEAD').strip()
        self.git('update-index','--add','--cacheinfo','160000,'+self.sha+',mock')
        self.git('commit','-qm','pin')

    def git(self,*args):
        return subprocess.run(['git','-C',str(self.root),*args],check=True,capture_output=True,text=True).stdout

    def test_missing_private_access_does_not_mutate_checkout(self):
        before = self.git('status','--porcelain')
        with self.assertRaisesRegex(c.Invalid,'absent or inaccessible'):
            c.preflight(self.root)
        self.assertEqual(before,self.git('status','--porcelain'))

    def dependency(self):
        dep=self.root/'mock'
        subprocess.run(['git','clone','-q',str(self.root),str(dep)],check=True,capture_output=True)
        subprocess.run(['git','-C',str(dep),'checkout','-q',self.sha],check=True)
        return dep

    def test_mismatched_revision_is_not_reset(self):
        dep=self.dependency()
        subprocess.run(['git','-C',str(dep),'checkout','-q',self.git('symbolic-ref','--short','HEAD').strip()],check=True)
        before=c.git(dep,'rev-parse','HEAD')
        with self.assertRaisesRegex(c.Invalid,'revision mismatch'): c.preflight(self.root)
        self.assertEqual(before,c.git(dep,'rev-parse','HEAD'))

    def test_dirty_dependency_is_not_changed(self):
        dep=self.dependency()
        (dep/'untracked').write_text('keep me')
        with self.assertRaisesRegex(c.Invalid,'dirty'): c.preflight(self.root)
        self.assertEqual((dep/'untracked').read_text(),'keep me')


class PureTests(unittest.TestCase):
    def test_unsupported_schema_and_public_extra_fields(self):
        with self.assertRaisesRegex(c.Invalid,'schema'):
            c.validate_schema({'schema_version':2},'manifest')
        schema=c.read_json(c.ROOT/'review/schemas/public-summary.v1.json')
        self.assertFalse(schema['additionalProperties'])
        self.assertNotIn('service_duration_ms',schema['properties'])

    def test_subprocess_keeps_diagnostics_out_of_json(self):
        with tempfile.TemporaryDirectory() as temp:
            out, errors = Path(temp)/'output.json', Path(temp)/'diagnostics.log'
            cli.command([sys.executable, '-c', 'import sys,json; print(json.dumps(dict(status="completed"))); print("diagnostic",file=sys.stderr)'], c.ROOT, out, error_log=errors)
            self.assertEqual(c.read_json(out)['status'], 'completed')
            self.assertIn('diagnostic', errors.read_text())

    def test_monotonic_deadline(self):
        now=[10.0]
        b=h.Budget(clock=lambda:now[0])
        now[0]=12
        self.assertEqual(b.elapsed_ms(),2000)
        now[0]=70
        with self.assertRaises(h.Deadline): b.remaining()

    def test_expiry_and_denial_are_distinct(self):
        summary={'artifact':{'expires_at':'2000-01-01T00:00:00Z','id':123}}
        self.assertIn('unavailable',cli.availability(summary))
        with patch.object(cli,'gh_api',side_effect=c.Invalid('access denied')):
            with self.assertRaisesRegex(c.Invalid,'access denied'): cli.availability(summary,True)
        with patch.object(cli,'gh_api',return_value={'id':123,'name':'parent-http-evidence','expired':True}):
            with self.assertRaisesRegex(c.Invalid,'confirmed artifact expiry'): cli.availability(summary,True)

    def test_public_counts_and_stale_pin(self):
        # Once a snapshot exists, exercise the complete public allowlist validator.
        path=c.ROOT/'review/mock-summary.json'
        if not path.exists(): self.skipTest('snapshot generated after private CI')
        summary=c.read_json(path)
        c.validate_public(summary)
        for mutate in (
            lambda d:d.update(schema_version=2),
            lambda d:d.update(service_duration_ms=1),
            lambda d:d.update(mock_sha='0'*40),
            lambda d:d['experiments']['http']['automation'].update(accepted=999),
            lambda d:d['artifact'].update(run_id=1),
            lambda d:d.update(run_at='invalid-date'),
            lambda d:d['limitations'].append('Unsupported claim'),
        ):
            d=copy.deepcopy(summary); mutate(d)
            with self.assertRaises(c.Invalid): c.validate_public(d)


@unittest.skipUnless((c.ROOT/'mock/testdata/http-scenarios.v1.json').exists(), 'public checkout does not initialize private dependency')
class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.base=Path(cls.temp.name)
        cls.bins=cls.base/'bin'; cls.bins.mkdir()
        for name in ('application','automation','devdb'):
            subprocess.run(['go','build','-o',str(cls.bins/name),'./cmd/'+name],cwd=c.ROOT/'mock',check=True,capture_output=True)
        cls.descriptor=c.read_json(c.ROOT/'mock/testdata/http-scenarios.v1.json')

    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=self.base)
        self.addCleanup(self.temp.cleanup)
        self.out=Path(self.temp.name)

    def trial(self,case,condition):
        with h.Stack(self.bins,self.out,case['id']+'-'+condition) as stack:
            row=h.execute(stack,case,condition,1)
            app,auto,dir_=stack.application.proc,stack.automation.proc,stack.dir
        self.assertIsNotNone(app.poll()); self.assertIsNotNone(auto.poll())
        self.assertFalse(dir_.exists())
        return row

    def test_all_cases_two_seed_identical_runs(self):
        reports=[]
        for _ in range(2):
            rows=[self.trial(case,condition) for case,condition,r in c.ordering(self.descriptor,1,63)]
            c.check_trials(rows,self.descriptor,1,63,True)
            reports.append([{k:v for k,v in row.items() if k not in ('service_duration_ms','evidence')} for row in rows])
        self.assertEqual(reports[0],reports[1])
        rows[0]['case']='unknown'
        with self.assertRaisesRegex(c.Invalid,'Missing, duplicate'): c.check_trials(rows,self.descriptor,1,63,True)
        rows[0]['case']=rows[1]['case']; rows[0]['condition']=rows[1]['condition']
        with self.assertRaisesRegex(c.Invalid,'Missing, duplicate'): c.check_trials(rows,self.descriptor,1,63,True)
        with self.assertRaisesRegex(c.Invalid,'Missing, duplicate'): c.check_trials(rows[1:],self.descriptor,1,63,True)

    def test_reviewer_and_binding_tampering(self):
        case=self.descriptor['cases'][0]
        row=self.trial(case,'automation')
        c.check_evidence(row,case)
        malformed=copy.deepcopy(row)
        malformed['evidence']['approvals'][0]['expires_at']='invalid-date'
        with self.assertRaisesRegex(c.Invalid,'schema'):
            c.validate_schema(malformed,'trial-evidence')
        for mutate in (
            lambda r:r['evidence']['deliveries'][0].update(workspace_id='workspace-b'),
            lambda r:r['evidence']['downloads'][0].update(sha256='0'*64),
            lambda r:r['evidence']['approvals'][0].update(principal='outsider'),
            lambda r:r['evidence']['activity'].clear(),
            lambda r:r['evidence']['reviewer'].update(id='operator'),
        ):
            bad=copy.deepcopy(row); mutate(bad)
            with self.assertRaises(c.Invalid): c.check_evidence(bad,case)

    def test_timing_excludes_preparation_audit_and_teardown_includes_restart(self):
        now=[0.0]; measured=[0.0]
        original_prepare,original_audit,original_call,original_restart=h.prepare,h.audit,h.API.call,h.Stack.restart
        def prepare(*args):
            value=original_prepare(*args); now[0]+=100; return value
        def audit(*args):
            now[0]+=100; return original_audit(*args)
        def call(client,*args,**kwargs):
            if client.budget: now[0]+=.01; measured[0]+=.01
            return original_call(client,*args,**kwargs)
        def restart(stack,budget):
            now[0]+=.5; measured[0]+=.5; return original_restart(stack,budget)
        with h.Stack(self.bins,self.out,'clock') as stack:
            with patch.object(h,'prepare',prepare),patch.object(h,'audit',audit),patch.object(h.API,'call',call),patch.object(h.Stack,'restart',restart):
                row=h.execute(stack,self.descriptor['cases'][-1],'automation',1,budget_factory=lambda:h.Budget(clock=lambda:now[0]))
        self.assertAlmostEqual(row['service_duration_ms'],measured[0]*1000,places=6)
        self.assertTrue(row['evidence']['restarted'])
        self.assertGreater(now[0],200)

    def test_failed_assertion_and_interrupted_service_cleanup(self):
        for failure in ('assertion','service','deadline','interrupt'):
            with self.assertRaises((c.Invalid,KeyboardInterrupt)):
                with h.Stack(self.bins,self.out,failure) as stack:
                    app,auto,dir_=stack.application.proc,stack.automation.proc,stack.dir
                    if failure=='service':
                        stack.application.proc.kill(); stack.application.proc.wait()
                        h.API(stack.application.url,'operator').call('GET','session')
                    elif failure=='assertion':
                        with patch.object(h,'audit',side_effect=c.Invalid('failed audit')):
                            h.execute(stack,self.descriptor['cases'][0],'automation',1)
                    elif failure=='interrupt': raise KeyboardInterrupt
                    else:
                        h.execute(stack,self.descriptor['cases'][0],'automation',1,budget_factory=lambda:h.Budget(seconds=0))
            self.assertFalse(dir_.exists())
            self.assertIsNotNone(app.poll()); self.assertIsNotNone(auto.poll())

    def test_readiness_failure_and_occupied_ports(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0)); sock.listen()
            port=sock.getsockname()[1]
            with self.assertRaisesRegex(c.Invalid,'before readiness'):
                h.Service(self.bins/'application',['-db',str(self.out/'app.db'),'-listen',f'127.0.0.1:{port}'],self.out/'ready',self.out/'service.log')
        with self.assertRaisesRegex(c.Invalid,'readiness deadline'):
            h.Service(sys.executable,['-c','import time; time.sleep(10)'],self.out/'no-ready',self.out/'sleep.log',timeout=.03)
        self.assertFalse((self.out/'ready').exists())

    def test_http_contract_probes(self):
        with h.Stack(self.bins,self.out,'probes') as stack:
            self.assertTrue(all(h.contract_probe(stack).values()))


if __name__=='__main__': unittest.main()
