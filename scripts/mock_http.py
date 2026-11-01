"""Process lifecycle and HTTP-only trials for the pinned private mock."""
import base64
import datetime as dt
import json
import os
import signal
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from mock_contract import Invalid, TIMING, digest, require


class Deadline(Invalid):
    pass


class Budget:
    def __init__(self, seconds=60, clock=time.monotonic):
        self.clock = clock
        self.start = clock()
        self.end = self.start + seconds

    def remaining(self):
        remaining = self.end - self.clock()
        if remaining <= 0:
            raise Deadline('Trial deadline exceeded; outcome is unknown; evidence is not exportable')
        return remaining

    def elapsed_ms(self):
        self.remaining()
        return (self.clock() - self.start) * 1000


class API:
    # Instances are role-scoped. Reviewer credentials never enter actor requests.
    def __init__(self, url, role, trace=None, budget=None):
        self.url, self.role = url, role
        self.trace = trace if trace is not None else []
        self.budget = budget
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def call(self, method, path, body=None, key=None, fault=None, expected=None, raw=False):
        timeout = min(5, self.budget.remaining()) if self.budget else 5
        headers = {'Authorization': f'Bearer dev-{self.role}-token', 'Content-Type': 'application/json'}
        if method == 'POST': headers['Idempotency-Key'] = key or path
        if fault: headers['X-Mock-Fault'] = fault
        req = urllib.request.Request(self.url + '/api/v1/' + path,
                                     data=json.dumps(body).encode() if body is not None else None,
                                     headers=headers, method=method)
        try:
            response = self.opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            response = e
        except (OSError, TimeoutError) as e:
            raise Invalid(f'HTTP infrastructure failure: {self.role} {method} {path}') from e
        with response:
            payload = response.read(8 * 1024 * 1024)
            status = response.status
        try:
            value = payload if raw and status < 300 else json.loads(payload)
        except ValueError as e:
            raise Invalid('Malformed HTTP response') from e
        code = value.get('error', {}).get('code', '') if isinstance(value, dict) else ''
        self.trace.append(dict(method=method, path=path, identity=self.role, status=status,
                               code=code, fault=fault or '', key=key or (path if method == 'POST' else '')))
        if self.budget: self.budget.remaining()
        if expected:
            require((status, code) == expected, f'Unexpected HTTP response: {status} {code}; expected {expected}')
        else:
            require(status in (200, 201), f'HTTP failure: {status} {code} for {method} {path}')
        return value

    def items(self, path):
        value = self.call('GET', path + '?limit=100')
        require(len(value['items']) < 100, 'Unexpected evidence pagination')
        return value['items']


class Service:
    def __init__(self, binary, args, ready, log, timeout=10):
        self.ready, self.url, self.proc = Path(ready), None, None
        self.log = Path(log).open('ab')
        try:
            self.ready.unlink(missing_ok=True)
            self.proc = subprocess.Popen([str(binary), *args, '-ready-file', str(ready)],
                                         stdout=self.log, stderr=self.log, start_new_session=True)
            end = time.monotonic() + timeout
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            while time.monotonic() < end:
                require(self.proc.poll() is None, 'Service exited before readiness; inspect private service log')
                if self.ready.exists():
                    url = self.ready.read_text().strip()
                    parsed = urllib.parse.urlsplit(url)
                    require(parsed.scheme == 'http' and parsed.hostname == '127.0.0.1' and parsed.port, 'Invalid loopback readiness URL')
                    try:
                        with opener.open(url + '/health', timeout=min(.3, max(.001, end-time.monotonic()))) as response:
                            require(response.status == 200 and json.load(response)['status'] == 'ok', 'Readiness health failure')
                        self.url = url
                        return
                    except (urllib.error.URLError, OSError):
                        pass
                time.sleep(.01)
            raise Invalid('Service readiness deadline exceeded')
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.proc and self.proc.poll() is None:
            try:
                os.killpg(self.proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(self.proc.pid, signal.SIGKILL)
                self.proc.wait(timeout=2)
        self.log.close()
        self.ready.unlink(missing_ok=True)


class Stack:
    def __init__(self, bins, out, label):
        self.bins, self.out, self.label = bins, Path(out), label
        self.application = self.automation = None
        self.temp = None

    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory(prefix='runtime-', dir=self.out)
        self.dir = Path(self.temp.name)
        (self.out / 'logs').mkdir(exist_ok=True)
        try:
            with (self.out / 'logs' / (self.label + '-seed.log')).open('wb') as log:
                subprocess.run([str(self.bins / 'devdb'), '-db', str(self.dir/'application.db')],
                               check=True, stdout=log, stderr=log, timeout=10)
            self.application = self.launch('application')
            self.automation = self.launch('automation')
            return self
        except BaseException:
            self.__exit__(None, None, None)
            raise

    def launch(self, kind, timeout=10):
        args = ['-db', str(self.dir / (kind + '.db')), '-listen', '127.0.0.1:0', '-enable-test-faults']
        if kind == 'automation': args += ['-application-url', self.application.url]
        return Service(self.bins / kind, args, self.dir / (kind + '.ready'),
                       self.out / 'logs' / (self.label + '-' + kind + '.log'), timeout=timeout)

    def restart(self, budget):
        self.automation.close()
        self.automation = self.launch('automation', timeout=min(10, budget.remaining()))
        budget.remaining()

    def __exit__(self, *args):
        try:
            if self.automation: self.automation.close()
        finally:
            try:
                if self.application: self.application.close()
            finally:
                if self.temp: self.temp.cleanup()


def expires(seconds):
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=seconds)).isoformat(timespec='microseconds').replace('+00:00','Z')


def prepare(stack, case, trace):
    actor = API(stack.application.url, 'operator', trace)
    owner = API(stack.application.url, 'owner', trace)
    reviewer = API(stack.application.url, 'reviewer', trace)
    auto = API(stack.automation.url, 'operator', trace)
    req = actor.call('POST', 'work-requests', dict(workspace_id=case['workspace'], title=case['id'], requested_output=case['output']), key='create')
    path = 'work-requests/' + req['id']
    if case['scenario'] not in ('missing_approval', 'wrong_workspace'):
        expiry = expires(.5 if case['scenario'] == 'expired' else 3600)
        approval = owner.call('POST', path + '/approvals', {'expires_at': expiry}, key='approve')
        if case['scenario'] == 'revoked':
            owner.call('POST', 'approvals/' + approval['id'] + '/revoke', {}, key='revoke')
        if case['scenario'] == 'expired':
            # Approval expiry is preparation, outside the service trial clock.
            end = dt.datetime.fromisoformat(expiry.replace('Z','+00:00'))
            time.sleep(max(0, (end - dt.datetime.now(dt.timezone.utc)).total_seconds()) + .01)
    if case['scenario'] == 'wrong_workspace':
        other = actor.call('POST', 'work-requests', dict(workspace_id='workspace-a', title='Approval only for A', requested_output='A'), key='create-other')
        owner.call('POST', 'work-requests/' + other['id'] + '/approvals', {'expires_at': expires(3600)}, key='approve-other')
    identities = {'actor': actor.call('GET', 'session'), 'reviewer': reviewer.call('GET', 'session')}
    return req, actor, reviewer, auto, identities


def audit(reviewer, path, identities, trace, downloads, reconciliation, restarted):
    # Read-only observer audit after the scripted terminal outcome. No review or
    # recovery is added to direct_script/without_recovery unknown outcomes.
    return dict(request=reviewer.call('GET', path), files=reviewer.items(path + '/files'),
                deliveries=reviewer.items(path + '/deliveries'), approvals=reviewer.items(path + '/approvals'),
                activity=reviewer.items(path + '/activity'), downloads=downloads,
                reconciliation=reconciliation, restarted=restarted, http=trace, **identities)


def execute(stack, case, condition, repeat, budget_factory=Budget):
    trace = []
    req, actor, reviewer, auto, identities = prepare(stack, case, trace)
    path = 'work-requests/' + req['id']
    # The only start of the measured interval: all setup above has completed.
    budget = budget_factory()
    for client in (actor, reviewer, auto): client.budget = budget
    rejected = condition == 'without_placement' and case['workspace'] == 'workspace-b'
    protected = case['scenario'] in ('missing_approval','wrong_workspace','revoked','expired')
    fault = {'restart': 'drop_response'}.get(case['scenario'], case['scenario'])
    if fault not in ('drop_response','fail_before_write','corrupt_output'): fault = ''
    row = dict(schema_version=1, case=case['id'], condition=condition, repeat=repeat,
               expected_outcome=case['expected'][condition], placement_correct=not rejected,
               rejected_placement=rejected, fault_injected=bool(fault) and not rejected,
               recovered=False, attempts=0, human_active_minutes=None, actual_cost=None)
    downloads, reconciliation = [], []
    auto_id = None
    restarted = False
    if rejected:
        row.update(outcome='correctly_stopped', terminal_reason='placement_stop')
    elif condition == 'direct_script':
        row['attempts'] = 1
        body = dict(name='output.txt', content=case['output'])
        file = actor.call('POST', path + '/files', body, key='direct-file',
                          fault='corrupt_output' if fault == 'corrupt_output' else None,
                          expected=(403, 'approval_required') if protected else None)
        if protected:
            # Explicitly check that delivery writes are also denied.
            actor.call('POST', path + '/deliveries', {'file_id': 'absent'}, key='denied-delivery', expected=(403,'approval_required'))
            row.update(outcome='correctly_stopped', terminal_reason='authorization_stop')
        else:
            actor.call('POST', path + '/deliveries', {'file_id': file['id']}, key='direct-delivery',
                       fault=fault if fault != 'corrupt_output' else None,
                       expected=(503, 'confirmation_unavailable' if fault == 'drop_response' else 'injected_failure') if fault and fault != 'corrupt_output' else None)
    else:
        state = auto.call('POST', 'automations', {'request_id': req['id'], 'fault': fault}, key='start')
        auto_id = state['id']
        row['attempts'] = 1
        if protected:
            require(state['status'] in ('needs_approval','stopped'), 'Expected authorization stop')
            actor.call('POST', path + '/deliveries', {'file_id': 'absent'}, key='denied-delivery', expected=(403,'approval_required'))
            row.update(outcome='correctly_stopped', terminal_reason='authorization_stop')
        elif fault and fault != 'corrupt_output':
            expected_error = 'application 503: ' + ('confirmation_unavailable' if fault == 'drop_response' else 'injected_failure')
            require(state['status'] == 'checking_delivery' and state['last_error'] == expected_error, 'Unexpected infrastructure error inside automation')
            if condition != 'without_recovery':
                if case['scenario'] == 'restart':
                    stack.restart(budget)
                    auto.url = stack.automation.url
                    restarted = True
                    persisted = auto.call('GET', 'automations/' + auto_id)
                    require(persisted['id'] == auto_id, 'Lost automation state on restart')
                state = auto.call('POST', 'automations/' + auto_id + '/check-delivery', {}, key='check-before-retry')
                reconciliation.append(dict(action='check-delivery', delivery_id=state['delivery_id']))
                if not state['delivery_id']:
                    state = auto.call('POST', 'automations/' + auto_id + '/retry', {}, key='recover')
                    row['attempts'] += 1
    if 'outcome' not in row and fault and fault != 'corrupt_output' and condition in ('direct_script','without_recovery'):
        row.update(outcome='unknown', terminal_reason='recovery_omitted')
    if 'outcome' not in row:
        deliveries = reviewer.items(path + '/deliveries')
        require(len(deliveries) == 1, 'Expected exactly one delivery for independent review')
        delivery = deliveries[0]
        file = reviewer.call('GET', 'files/' + delivery['file_id'])
        content = reviewer.call('GET', 'files/' + delivery['file_id'] + '/content', raw=True)
        actual_hash = digest(content)
        downloads.append(dict(file_id=file['id'], sha256=actual_hash, content_base64=base64.b64encode(content).decode()))
        approvals = reviewer.items(path + '/approvals')
        approval = next((a for a in approvals if a['id'] == delivery['approval_id']), None)
        valid = (actual_hash == digest(case['output'].encode()) and file['sha256'] == actual_hash
                 and file['request_id'] == delivery['request_id'] == req['id']
                 and file['workspace_id'] == delivery['workspace_id'] == case['workspace']
                 and file['principal'] == delivery['principal'] == 'operator' and approval
                 and approval['request_id'] == req['id'] and approval['principal'] == 'operator' and not approval['revoked'])
        reviewed = reviewer.call('POST', 'deliveries/' + delivery['id'] + '/review', {'decision': 'accept' if valid else 'reject'}, key='review')
        verdict = 'accepted' if valid else 'rejected'
        require(reviewed['acceptance_status'] == verdict, 'Review did not persist')
        if auto_id:
            state = auto.call('POST', 'automations/' + auto_id + '/check-delivery', {}, key='final-check')
            require(state['status'] == ('completed' if valid else 'failed'), 'Unexpected final automation status')
        row.update(outcome='accepted' if valid else 'failed', terminal_reason='independent_review')
    row['service_duration_ms'] = budget.elapsed_ms()
    for client in (actor, reviewer, auto): client.budget = None
    row['evidence'] = audit(reviewer, path, identities, trace, downloads, reconciliation, restarted)
    row['file_writes'] = len(row['evidence']['files'])
    row['delivery_writes'] = len(row['evidence']['deliveries'])
    row['recovered'] = row['fault_injected'] and fault != 'corrupt_output' and row['outcome'] == 'accepted'
    return row


def contract_probe(stack):
    actor, owner, reviewer, auto = [API(url, role) for url, role in (
        (stack.application.url,'operator'), (stack.application.url,'owner'),
        (stack.application.url,'reviewer'), (stack.automation.url,'operator'))]
    requests = []
    for workspace in ('workspace-a','workspace-b'):
        r = actor.call('POST','work-requests',dict(workspace_id=workspace,title='Contract scope probe',requested_output='probe\n'),key=workspace)
        owner.call('POST','work-requests/'+r['id']+'/approvals',{'expires_at': expires(3600)},key='approve-'+workspace)
        requests.append(r)
    a, b = ['work-requests/'+r['id'] for r in requests]
    body = dict(name='probe.txt',content='probe\n')
    file = actor.call('POST',a+'/files',body,key='file')
    require(actor.call('POST',a+'/files',body,key='file')['id'] == file['id'], 'Application replay duplicated file')
    actor.call('POST',a+'/files',dict(name='changed',content='conflict'),key='file',expected=(409,'idempotency_conflict'))
    actor.call('POST',b+'/deliveries',{'file_id':file['id']},key='cross',expected=(403,'file_scope_mismatch'))
    state = auto.call('POST','automations',{'request_id':requests[1]['id']},key='auto')
    require(auto.call('POST','automations',{'request_id':requests[1]['id']},key='auto')['id'] == state['id'], 'Automation replay duplicated execution')
    auto.call('POST','automations',{'request_id':requests[0]['id']},key='auto',expected=(409,'idempotency_conflict'))
    actor.call('POST','deliveries/'+state['delivery_id']+'/review',{'decision':'accept'},key='self-review',expected=(403,'role_denied'))
    require(len(reviewer.items(b+'/deliveries')) == 1 and not reviewer.items(a+'/deliveries'), 'Probe delivery count mismatch')
    return {key: True for key in ('application_replay','application_conflict','automation_replay','automation_conflict','cross_workspace_rejected','actor_review_rejected','at_most_one_delivery')}
