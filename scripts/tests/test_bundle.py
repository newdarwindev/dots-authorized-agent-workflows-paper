"""Negative checks against a complete run; CI invokes these after measurement."""
import copy
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import mock_contract as c


@unittest.skipUnless(os.environ.get('MOCK_TEST_BUNDLE'), 'requires a newly generated private evidence bundle')
class BundleIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.bundle=Path(self.temp.name)/'evidence'
        shutil.copytree(os.environ['MOCK_TEST_BUNDLE'],self.bundle)
        self.manifest=c.read_json(self.bundle/'manifest.json')

    def reseal(self,filename):
        self.manifest['files'][filename]=c.digest((self.bundle/filename).read_bytes())
        c.write_json(self.bundle/'manifest.json',self.manifest)

    def test_valid_complete_bundle(self): c.verify_bundle(self.bundle)

    def test_tampered_report_digest(self):
        with (self.bundle/'http-report.json').open('a') as out: out.write(' ')
        with self.assertRaisesRegex(c.Invalid,'Tampered'): c.verify_bundle(self.bundle)

    def test_missing_duplicate_unexpected_rows_and_inconsistent_summary(self):
        original=c.read_json(self.bundle/'http-report.json')
        for mutate in (
            lambda d:d['trials'].pop(),
            lambda d:d['trials'].append(copy.deepcopy(d['trials'][0])),
            lambda d:d['trials'][0].update(case='unexpected'),
            lambda d:d['summary']['automation'].update(accepted=999),
            lambda d:d['trials'][0].update(schema_version=2),
        ):
            report=copy.deepcopy(original); mutate(report)
            c.write_json(self.bundle/'http-report.json',report); self.reseal('http-report.json')
            with self.assertRaises(c.Invalid): c.verify_bundle(self.bundle)

    def test_fixture_and_stale_pin_and_schema(self):
        for field,value in (('fixture_sha256','0'*64),('mock_sha','0'*40),('schema_version',2)):
            manifest=copy.deepcopy(self.manifest); manifest[field]=value
            c.write_json(self.bundle/'manifest.json',manifest)
            with self.assertRaises(c.Invalid): c.verify_bundle(self.bundle)

    def test_report_csv_probe_and_download_tampering(self):
        report=c.read_json(self.bundle/'http-report.json')
        accepted=next(row for row in report['trials'] if row['outcome']=='accepted')
        accepted['evidence']['downloads'][0]['content_base64']='dGFtcGVyZWQ='
        c.write_json(self.bundle/'http-report.json',report); self.reseal('http-report.json')
        with self.assertRaisesRegex(c.Invalid,'download bytes'): c.verify_bundle(self.bundle)

    def test_unmanifested_file(self):
        (self.bundle/'unexpected.json').write_text('{}')
        with self.assertRaisesRegex(c.Invalid,'unmanifested'): c.verify_bundle(self.bundle)
