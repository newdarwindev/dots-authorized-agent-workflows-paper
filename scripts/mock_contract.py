"""Versioned evidence validation. This module needs no private checkout."""
import base64
import datetime as dt
import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CLASSIFICATION = 'deterministic synthetic simulation'
CASES = ['fixture-A', 'fixture-B', 'missing-approval', 'wrong-workspace',
         'revoked-approval', 'expired-approval', 'lost-confirmation',
         'temporary-failure', 'corrupted-output', 'restart-recovery']
CONDITIONS = ['direct_script', 'automation', 'without_placement', 'without_recovery']
OUTCOMES = ['accepted', 'correctly_stopped', 'failed', 'pending', 'unknown']
TIMING = ('Monotonic seconds from after service readiness, request creation and approval setup '
          'to scripted terminal outcome, including execution, recovery, restart and independent '
          'review; excludes compilation, fixture preparation, initial startup and teardown. '
          'Post-terminal evidence audit is excluded. Deadline: 60 seconds; HTTP call bound: 5 seconds.')
LIMITATIONS = [
    'Scripted synthetic actors; no model calls, native-product baseline, real-host or production evaluation.',
    'direct_script has both workspaces; without_placement selects A and stops on mismatches; without_recovery omits recovery.',
    'Accepted deliveries require independent review. Correct stops, rejected output, pending and unknown outcomes remain separate.',
    'Corrupted output is an expected acceptance failure. Scheduled denominators include every trial.',
    'Faults skipped by placement stops are not injected. Recovery eligibility excludes corruption; no public recovery rate is claimed.',
    'Service timings and detailed verification records remain private. Functional timings include setup and teardown.',
    'Human effort, actual cost, ROI and commercial advantage are unknown. The real-host pilot remains proposed.',
    'Private Actions artifacts expire after 14 days; historical success does not establish current evidence availability.',
]

class Invalid(ValueError):
    pass


def require(value, message):
    if not value:
        raise Invalid(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(value):
        raise Invalid('Non-finite JSON number')
    try:
        return json.loads(Path(path).read_text(), object_pairs_hook=unique, parse_constant=nonfinite)
    except (ValueError, OSError) as e:
        raise Invalid(f'Cannot read JSON: {path}') from e


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + '\n')


def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    require(p.returncode == 0, f'Git operation failed: {args[0]} (required source revision may be unavailable)')
    return p.stdout


def pin(root, revision='HEAD'):
    entry = git(root, 'ls-tree', revision, '--', 'mock').decode().split()
    require(len(entry) >= 3 and entry[0] == '160000', 'Parent revision has no committed mock gitlink')
    return entry[2]


def contract(root=ROOT, revision=None):
    data = (git(root, 'show', f'{revision}:review/mock-contract.json') if revision
            else (root / 'review/mock-contract.json').read_bytes())
    c = json.loads(data)
    require(c['schema_version'] == 1, 'Unsupported consumer contract')
    return c


def preflight(root=ROOT):
    parent = git(root, 'rev-parse', 'HEAD').decode().strip()
    expected = pin(root)
    dep = root / 'mock'
    require((dep / '.git').exists(), 'Private mock is absent or inaccessible. With existing authorized access run: git submodule update --init -- mock')
    actual = git(dep, 'rev-parse', 'HEAD').decode().strip()
    require(actual == expected, f'Mock revision mismatch: expected {expected}, found {actual}; select the committed pin explicitly')
    require(not git(dep, 'status', '--porcelain', '--untracked-files=all'), 'Private mock checkout is dirty; preserve or commit changes before running')
    require(not git(root, 'status', '--porcelain', '--untracked-files=normal', '--ignore-submodules=all'),
            'Parent checkout is dirty; commit consumer changes before recording source provenance')
    c = contract(root)
    descriptor = (dep / 'testdata/http-scenarios.v1.json').read_bytes()
    fixture = (dep / 'testdata/paper-fixture.json').read_bytes()
    require(digest(descriptor) == c['descriptor_sha256'], 'Private scenario descriptor hash mismatch')
    require(digest(fixture) == c['fixture_sha256'] == digest((root / 'review/fleet-fixture.json').read_bytes()), 'Original fixture hash mismatch')
    d = json.loads(descriptor)
    validate_descriptor(d)
    version = subprocess.run(['go', 'env', 'GOVERSION'], check=True, capture_output=True, text=True).stdout.strip()
    require(version == c['go_version'] == d['go_version'], f'Unsupported Go toolchain {version}; require {c["go_version"]}')
    return parent, expected, d, version


def validate_schema(data, name, root=ROOT):
    schema = read_json(root / 'review/schemas' / (name + '.v1.json'))
    try:
        jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(data)
    except jsonschema.ValidationError as e:
        raise Invalid(f'{name} schema: {e.json_path}: {e.message}') from e


def validate_descriptor(d):
    require(d['schema_version'] == 1 and d['conditions'] == CONDITIONS, 'Unsupported scenario descriptor')
    require([c['id'] for c in d['cases']] == CASES, 'Scenario set mismatch')
    for c in d['cases']:
        require(set(c['expected']) == set(CONDITIONS), 'Missing expected outcomes')
        require(all(v in OUTCOMES for v in c['expected'].values()), 'Unknown expected outcome')


def ordering(d, repeats, seed):
    # Python's shuffle implementation may change: the algorithm and Python version
    # are recorded. Stable hash sorting also makes replay independent of stdlib RNG.
    return [(c, condition, repeat) for repeat in range(1, repeats + 1)
            for c in d['cases'] for condition in sorted(CONDITIONS, key=lambda x:
                digest(f'paired-sha256-v1:{seed}:{repeat}:{c["id"]}:{x}'.encode()))]


def aggregates(trials):
    result = {}
    for condition in CONDITIONS:
        rows = [r for r in trials if r['condition'] == condition]
        result[condition] = dict(scheduled=len(rows), **{
            outcome: sum(r['outcome'] == outcome for r in rows) for outcome in OUTCOMES})
        result[condition]['rejected_placements'] = sum(r['rejected_placement'] for r in rows)
    return result


def check_trials(rows, d, repeats, seed, http):
    expected_set = {(c['id'], v, r) for c in d['cases'] for v in CONDITIONS for r in range(1, repeats + 1)}
    actual = [(r['case'], r['condition'], r['repeat']) for r in rows]
    require(len(actual) == len(set(actual)) and set(actual) == expected_set, 'Missing, duplicate or unexpected trials')
    if http:
        require(actual == [(c['id'], v, r) for c, v, r in ordering(d, repeats, seed)], 'Seeded paired ordering mismatch')
    cases = {c['id']: c for c in d['cases']}
    for row in rows:
        c = cases[row['case']]
        require(row['expected_outcome'] == c['expected'][row['condition']] == row['outcome'], 'Unexpected business outcome')
        rejected = row['condition'] == 'without_placement' and c['workspace'] == 'workspace-b'
        injected = c['scenario'] in ('drop_response', 'fail_before_write', 'corrupt_output', 'restart') and not rejected
        recovered = injected and c['scenario'] != 'corrupt_output' and row['outcome'] == 'accepted'
        require(row['placement_correct'] == (not rejected) and row['rejected_placement'] == rejected, 'Placement invariant')
        require(row['fault_injected'] == injected and row['recovered'] == recovered, 'Recovery/injection invariant')
        protected = c['scenario'] in ('missing_approval', 'wrong_workspace', 'revoked', 'expired') or rejected
        require(row['delivery_writes'] <= 1, 'Duplicate deliveries')
        expected_files = 0 if protected else 1
        expected_deliveries = 0 if protected or (c['scenario'] == 'fail_before_write' and row['outcome'] == 'unknown') else 1
        require(row['file_writes'] == expected_files and row['delivery_writes'] == expected_deliveries, 'Unexpected persisted effect counts')
        require(row['attempts'] == (0 if rejected else 2 if recovered and c['scenario'] == 'fail_before_write' else 1), 'Unexpected execution attempts')
        duration = row['service_duration_ms' if http else 'duration_ms']
        require(isinstance(duration, (int, float)) and math.isfinite(duration) and duration >= 0, 'Invalid measured timing')
        if protected:
            require(row['file_writes'] == row['delivery_writes'] == 0, 'Unauthorized effects')
        require(row['human_active_minutes'] is None and row['actual_cost'] is None, 'Invented effort or cost')
        if http:
            validate_schema(row, 'trial-evidence')
            check_evidence(row, c)


def check_evidence(row, case):
    e = row['evidence']
    req = e['request']
    require(req['workspace_id'] == case['workspace'] and req['created_by'] == 'operator', 'Request binding mismatch')
    require(digest(req['requested_output'].encode()) == digest(case['output'].encode()), 'Request output mismatch')
    require(e['actor'] == {'id': 'operator', 'role': 'operator'} and e['reviewer'] == {'id': 'reviewer', 'role': 'reviewer'}, 'Identity separation mismatch')
    require(len(e['files']) == row['file_writes'] and len(e['deliveries']) == row['delivery_writes'], 'Effect counts mismatch')
    for f in e['files']:
        require(f['request_id'] == req['id'] and f['workspace_id'] == case['workspace'] and f['principal'] == 'operator', 'File binding mismatch')
        a = next((a for a in e['approvals'] if a['id'] == f['approval_id']), None)
        require(a and a['request_id'] == req['id'] and a['principal'] == 'operator' and not a['revoked'], 'File approval mismatch')
        require(dt.datetime.fromisoformat(f['created_at'].replace('Z','+00:00')) < dt.datetime.fromisoformat(a['expires_at'].replace('Z','+00:00')), 'Write after approval expiry')
    for delivery in e['deliveries']:
        f = next((f for f in e['files'] if f['id'] == delivery['file_id']), None)
        require(f and all(delivery[k] == f[k] for k in ('request_id', 'workspace_id', 'principal', 'approval_id')), 'Delivery binding mismatch')
    for action in e['http']:
        require(not (action['identity'] != 'reviewer' and action['path'].endswith('/review') and action['status'] < 300), 'Actor reviewed its own delivery')
        require(not (action['identity'] != 'owner' and action['path'].endswith('/approvals') and action['method'] == 'POST' and action['status'] < 300), 'Actor granted its own approval')
    outcome = row['outcome']
    if outcome in ('accepted', 'failed'):
        require(len(e['deliveries']) == len(e['downloads']) == 1, 'Missing independent download/review')
        delivery = e['deliveries'][0]
        file = next(f for f in e['files'] if f['id'] == delivery['file_id'])
        download = e['downloads'][0]
        require(download['file_id'] == file['id'] and download['sha256'] == file['sha256'], 'Downloaded file hash mismatch')
        try:
            downloaded = base64.b64decode(download['content_base64'], validate=True)
        except ValueError as error:
            raise Invalid('Malformed recorded download') from error
        require(digest(downloaded) == download['sha256'], 'Recorded download bytes do not match hash')
        expected = digest(case['output'].encode())
        require((download['sha256'] == expected) == (outcome == 'accepted'), 'Acceptance hash mismatch')
        verdict = 'accepted' if outcome == 'accepted' else 'rejected'
        require(delivery['acceptance_status'] == verdict, 'Reviewer verdict mismatch')
        require(any(a['actor'] == 'reviewer' and a['action'] == 'delivery_' + verdict for a in e['activity']), 'Independent reviewer activity absent')
    if row['recovered']:
        require(e['reconciliation'] and e['reconciliation'][0]['action'] == 'check-delivery', 'Recovery skipped reconciliation')
        if case['scenario'] in ('drop_response', 'restart'):
            require(e['reconciliation'][0]['delivery_id'] and row['attempts'] == 1, 'Retried committed delivery')
        if case['scenario'] == 'fail_before_write':
            require(not e['reconciliation'][0]['delivery_id'] and row['attempts'] == 2, 'Missing bounded pre-write retry')
        if case['scenario'] == 'restart':
            require(e['restarted'], 'Restart recovery did not restart')
    if outcome == 'unknown':
        require(not e['reconciliation'] and not e['downloads'] and all(x['acceptance_status'] == 'pending' for x in e['deliveries']), 'Unknown converted to completion')


def _verify_bundle(bundle, root=ROOT):
    bundle = Path(bundle)
    m = read_json(bundle / 'manifest.json')
    validate_schema(m, 'manifest', root)
    require(m['mock_sha'] == pin(root) == pin(root, m['parent_source_sha']), 'Stale mock/evidence pairing')
    for source in ('scripts/mock.py','scripts/mock_http.py','scripts/mock_contract.py',
                   'review/schemas/manifest.v1.json','review/schemas/trial-evidence.v1.json','review/schemas/public-summary.v1.json'):
        require(git(root, 'show', m['parent_source_sha'] + ':' + source) == (root/source).read_bytes(), 'Consumer implementation/schema changed since run; regenerate evidence')
    source_contract = contract(root, m['parent_source_sha'])
    require(source_contract == contract(root), 'Consumer contract changed since execution')
    require(m['descriptor_sha256'] == source_contract['descriptor_sha256'] and m['fixture_sha256'] == source_contract['fixture_sha256'], 'Fixture/descriptor provenance mismatch')
    require(m['protocol_sha256'] == digest(git(root, 'show', m['parent_source_sha'] + ':review/fleet-protocol.md')) == digest((root / 'review/fleet-protocol.md').read_bytes()), 'Protocol digest mismatch')
    require(m['tools']['go'] == source_contract['go_version'] and m['timing_definition'] == TIMING, 'Toolchain/timing definition mismatch')
    files = {str(p.relative_to(bundle)) for p in bundle.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    require(files == set(m['files']), 'Missing or unmanifested evidence files')
    for name, expected in m['files'].items():
        p = bundle / name
        require(not p.is_symlink() and p.resolve().is_relative_to(bundle.resolve()), 'Unsafe evidence path')
        require(digest(p.read_bytes()) == expected, f'Tampered evidence: {name}')
    require(m['files']['descriptor.json'] == m['descriptor_sha256'] and m['files']['paper-fixture.json'] == m['fixture_sha256'], 'Bundled source digest mismatch')
    d = read_json(bundle / 'descriptor.json')
    validate_descriptor(d)
    functional = read_json(bundle / 'functional/evaluation.json')
    require(functional['classification'] == 'deterministic_synthetic_simulation', 'Functional classification mismatch')
    for report, http in ((functional, False), (read_json(bundle / 'http-report.json'), True)):
        require(report['seed'] == m['seed'] and report['repeats'] == m['repeats'], 'Report experiment mismatch')
        check_trials(report['trials'], d, m['repeats'], m['seed'], http)
        expected = aggregates(report['trials'])
        if http:
            require(report['schema_version'] == 1 and report['classification'] == CLASSIFICATION and report['summary'] == expected, 'HTTP aggregate/schema mismatch')
        else:
            for condition in CONDITIONS:
                for key, value in expected[condition].items():
                    if key != 'pending':
                        require(report['summary'][condition][key] == value, 'Functional aggregate mismatch')
                for key, field in [('recovered','recovered'), ('fault_injected','fault_injected'), ('placement_correct','placement_correct')]:
                    require(report['summary'][condition][key] == sum(t[field] for t in report['trials'] if t['condition'] == condition), 'Functional recovery aggregate mismatch')
                require(report['summary'][condition]['cost_per_accepted'] is None, 'Invented cost')
            csv_rows = list(csv.DictReader((bundle / 'functional/trials.csv').open()))
            require(len(csv_rows) == len(report['trials']), 'Functional CSV denominator mismatch')
            for a, b in zip(csv_rows, report['trials']):
                for key, value in a.items():
                    original = b[key]
                    expected_value = 'unknown' if original is None else str(original).lower() if isinstance(original, bool) else str(original)
                    if key == 'duration_ms':
                        require(abs(float(value) - original) < 0.0011, 'CSV timing mismatch')
                    else:
                        require(value == expected_value, 'Functional CSV mismatch')
    probes = read_json(bundle / 'contract-probes.json')
    require(set(probes) == {'application_replay','application_conflict','automation_replay','automation_conflict','cross_workspace_rejected','actor_review_rejected','at_most_one_delivery'} and all(v is True for v in probes.values()), 'Incomplete HTTP contract probes')
    require(read_json(bundle / 'php-smoke.json')['status'] == 'completed', 'PHP walkthrough not verified')
    return m, functional, read_json(bundle / 'http-report.json')


def validate_public(summary, root=ROOT):
    validate_schema(summary, 'public-summary', root)
    require(summary['classification'] == CLASSIFICATION and summary['limitations'] == LIMITATIONS, 'Public limitations/classification mismatch')
    require(summary['scenarios'] == CASES and summary['conditions'] == CONDITIONS, 'Public allowlist mismatch')
    require(summary['mock_sha'] == pin(root) == pin(root, summary['parent_source_sha']), 'Stale public evidence/mock pair')
    source = contract(root, summary['parent_source_sha'])
    require(source == contract(root) and summary['descriptor_sha256'] == source['descriptor_sha256'] and summary['fixture_sha256'] == source['fixture_sha256'], 'Public source digest mismatch')
    require(summary['protocol_sha256'] == digest((root / 'review/fleet-protocol.md').read_bytes()), 'Stale public protocol')
    # Compute expected outcomes from the public names and selected semantics,
    # independently of any supplied aggregate or private source access.
    for experiment in summary['experiments'].values():
        for condition in CONDITIONS:
            counts = experiment[condition]
            expected = dict(accepted=0, correctly_stopped=0, failed=0, pending=0, unknown=0)
            for case in CASES:
                outcome = 'accepted'
                if case in CASES[2:6] or (condition == 'without_placement' and case in ('fixture-B','wrong-workspace','restart-recovery')):
                    outcome = 'correctly_stopped'
                elif case == 'corrupted-output': outcome = 'failed'
                elif condition in ('direct_script','without_recovery') and case in ('lost-confirmation','temporary-failure','restart-recovery'): outcome = 'unknown'
                expected[outcome] += summary['repeats']
            expected['scheduled'] = len(CASES) * summary['repeats']
            expected['rejected_placements'] = (3 * summary['repeats'] if condition == 'without_placement' else 0)
            require(counts == expected, 'Inconsistent public outcome counts')
    a = summary['artifact']
    parse = lambda value: dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    require(parse(a['created_at']) <= parse(a['verified_at']) < parse(a['expires_at']) <= parse(a['created_at']) + dt.timedelta(days=14, minutes=1), 'Invalid artifact retention/verification dates')
    require(summary['ci']['run_url'] == f'https://github.com/newdarwindev/dots-paper-workflow-mock/actions/runs/{a["run_id"]}', 'CI URL mismatch')
    require(a['run_id'] == summary['ci']['run_id'] and summary['ci']['commit_sha'] == summary['mock_sha'], 'Public CI binding mismatch')
    return summary


def verify_bundle(bundle, root=ROOT):
    try:
        return _verify_bundle(bundle, root)
    except Invalid:
        raise
    except (KeyError, TypeError, ValueError, OSError) as error:
        raise Invalid('Malformed or incomplete private evidence bundle') from error
