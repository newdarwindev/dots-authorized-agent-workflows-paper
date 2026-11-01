#!/usr/bin/env python3
"""Run the pinned mock through HTTP, verify private evidence, export a public summary."""
import argparse
import datetime as dt
import io
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
import zipfile
from pathlib import Path

from mock_contract import (ROOT, CLASSIFICATION, CASES, CONDITIONS, TIMING, LIMITATIONS,
                           Invalid, aggregates, contract, digest, git, ordering, pin,
                           preflight, read_json, require, validate_public, verify_bundle, write_json)
from mock_http import Deadline, Stack, execute, contract_probe

PRIVATE_REPO = 'newdarwindev/dots-paper-workflow-mock'


def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')


def command(args, cwd, log, env=None, timeout=180):
    with Path(log).open('wb') as output:
        subprocess.run([str(x) for x in args], cwd=cwd, stdout=output, stderr=output,
                       env=env, check=True, timeout=timeout)


def ci_provenance():
    if not os.environ.get('GITHUB_ACTIONS'):
        return None
    require(os.environ['GITHUB_REPOSITORY'] == PRIVATE_REPO, 'HTTP evidence CI must run in the private repository')
    run_id = int(os.environ['GITHUB_RUN_ID'])
    return dict(repository=PRIVATE_REPO, run_id=run_id,
                run_attempt=int(os.environ['GITHUB_RUN_ATTEMPT']),
                run_url=f'https://github.com/{PRIVATE_REPO}/actions/runs/{run_id}',
                commit_sha=os.environ['GITHUB_SHA'])


def run(args):
    parent, mock_sha, descriptor, version = preflight()
    out = args.out.resolve()
    require(out.is_relative_to((ROOT / 'build/mock').resolve()), 'Generated evidence must be inside ignored build/mock/')
    require(not out.exists(), f'Evidence destination already exists: {out}; choose --out build/mock/NEW')
    require(shutil.which('php'), 'PHP CLI with cURL is required for the existing walkthrough (install php-cli/php-curl)')
    out.mkdir(parents=True, mode=0o700)
    bins = ROOT / 'build/mock/bin'
    bins.mkdir(parents=True, exist_ok=True)
    (out / 'logs').mkdir()
    for name in ('application', 'automation', 'devdb', 'evaluate'):
        command(['go', 'build', '-o', bins / name, './cmd/' + name], ROOT / 'mock', out / 'logs' / ('build-' + name + '.log'))
    shutil.copyfile(ROOT / 'mock/testdata/http-scenarios.v1.json', out / 'descriptor.json')
    shutil.copyfile(ROOT / 'mock/testdata/paper-fixture.json', out / 'paper-fixture.json')
    command([bins / 'evaluate', '-repeats', args.repeats, '-seed', args.seed, '-out', out / 'functional'], ROOT / 'mock', out / 'logs/functional.log')
    report = dict(schema_version=1, classification=CLASSIFICATION, seed=args.seed, repeats=args.repeats, trials=[], summary={})
    try:
        for i, (case, condition, repeat) in enumerate(ordering(descriptor, args.repeats, args.seed)):
            with Stack(bins, out, f'{i:03d}') as stack:
                try:
                    row = execute(stack, case, condition, repeat)
                except Deadline:
                    # Failed runs retain an explicit unknown partial record and are
                    # never given a successful manifest or exported.
                    write_json(out / 'deadline-unknown.json', dict(case=case['id'], condition=condition,
                               repeat=repeat, outcome='unknown', reason='deadline_exceeded'))
                    raise
                report['trials'].append(row)
            if (i + 1) % 40 == 0:
                print(f'HTTP trials: {i + 1}/{40 * args.repeats}', flush=True)
        report['summary'] = aggregates(report['trials'])
        write_json(out / 'http-report.json', report)
        with Stack(bins, out, 'contract') as stack:
            write_json(out / 'contract-probes.json', contract_probe(stack))
        with Stack(bins, out, 'php') as stack:
            env = dict(os.environ, APPLICATION_URL=stack.application.url, AUTOMATION_URL=stack.automation.url)
            command(['php', '-l', ROOT / 'mock/examples/php/workflow.php'], ROOT, out / 'logs/php-lint.log', env)
            command(['php', ROOT / 'mock/examples/php/workflow.php'], ROOT, out / 'php-smoke.json', env, timeout=60)
        c = contract()
        php_version = subprocess.run(['php','-r','echo PHP_VERSION;'], check=True, capture_output=True, text=True).stdout
        manifest = dict(schema_version=1, classification=CLASSIFICATION, parent_source_sha=parent,
                        mock_sha=mock_sha, descriptor_sha256=c['descriptor_sha256'], fixture_sha256=c['fixture_sha256'],
                        protocol_sha256=digest((ROOT / 'review/fleet-protocol.md').read_bytes()),
                        tools=dict(go=version, python=platform.python_version(), php=php_version),
                        seed=args.seed, repeats=args.repeats, scenarios=CASES, conditions=CONDITIONS,
                        timing_definition=TIMING, order_algorithm='paired-sha256-v1',
                        run_at=utcnow(), ci=ci_provenance(), validation='passed',
                        files={str(p.relative_to(out)): digest(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()})
        write_json(out / 'manifest.json', manifest)
        verify_bundle(out)
    except BaseException:
        write_json(out / 'partial-http-report.json', report)
        (out / 'manifest.json').unlink(missing_ok=True)
        raise
    print(f'Verified {len(report["trials"])} HTTP trials plus functional suite, contract probes and PHP smoke: {out}')


def gh_api(path, binary=False):
    p = subprocess.run(['gh','api',path], capture_output=True)
    if p.returncode:
        # A private 404 can mean access denial; never label it confirmed expiry.
        raise Invalid('Private evidence availability unknown: access denied or artifact not visible; authenticate with existing repository access')
    return p.stdout if binary else json.loads(p.stdout)


def artifact_metadata(artifact_id):
    a = gh_api(f'repos/{PRIVATE_REPO}/actions/artifacts/{artifact_id}')
    require(a['id'] == artifact_id and a['name'] == 'parent-http-evidence', 'Unexpected artifact identity')
    require(not a['expired'], 'Private evidence unavailable: confirmed artifact expiry')
    require(dt.datetime.fromisoformat(a['expires_at'].replace('Z','+00:00')) > dt.datetime.now(dt.timezone.utc), 'Private evidence unavailable: artifact expiry passed')
    return a


def export(args):
    a = artifact_metadata(args.artifact_id)
    archive = gh_api(f'repos/{PRIVATE_REPO}/actions/artifacts/{args.artifact_id}/zip', binary=True)
    require(a['digest'] == 'sha256:' + digest(archive), 'Artifact archive digest mismatch')
    download = ROOT / 'build/mock' / ('artifact-' + str(args.artifact_id))
    require(not download.exists(), 'Artifact download directory already exists; preserve it or select another artifact')
    download.mkdir(parents=True, mode=0o700)
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        require(len(z.namelist()) == len(set(z.namelist())), 'Duplicate archive members')
        for entry in z.infolist():
            target = download / entry.filename
            require(not Path(entry.filename).is_absolute() and target.resolve().is_relative_to(download.resolve()), 'Unsafe artifact archive path')
            require(entry.file_size < 64 * 1024 * 1024 and (entry.external_attr >> 16) & 0o170000 != 0o120000, 'Unsafe artifact member')
        z.extractall(download)
    m, functional, http = verify_bundle(download)
    ci = m['ci']
    require(ci and ci['run_id'] == a['workflow_run']['id'] and ci['commit_sha'] == a['workflow_run']['head_sha'] == m['mock_sha'], 'Artifact run/source mismatch')
    workflow = gh_api(f'repos/{PRIVATE_REPO}/actions/runs/{ci["run_id"]}')
    require(workflow['status'] == 'completed' and workflow['conclusion'] == 'success'
            and workflow['event'] == 'workflow_dispatch' and workflow['head_sha'] == m['mock_sha'], 'Integration CI did not complete successfully')
    require(workflow['run_attempt'] == ci['run_attempt'], 'Artifact is from an earlier run attempt')
    summary = {key: m[key] for key in ('parent_source_sha','mock_sha','descriptor_sha256','fixture_sha256','protocol_sha256','seed','repeats','scenarios','conditions','ci','run_at')}
    summary.update(schema_version=1, export_allowlist_version=1, classification=CLASSIFICATION,
                   manifest_sha256=digest((download / 'manifest.json').read_bytes()),
                   report_sha256={name: m['files'][name] for name in ('functional/evaluation.json','functional/trials.csv','http-report.json')},
                   experiments=dict(functional=aggregates(functional['trials']), http=aggregates(http['trials'])),
                   human_active_minutes=None, actual_cost=None, limitations=LIMITATIONS,
                   artifact=dict(repository=PRIVATE_REPO, id=a['id'], name=a['name'], run_id=ci['run_id'],
                                 digest=a['digest'], created_at=a['created_at'], expires_at=a['expires_at'],
                                 verified_at=utcnow(), availability_at_verification='available'))
    validate_public(summary)
    write_json(args.out, summary)
    print(f'Exported allowlisted historical summary: {args.out}; private evidence expires {a["expires_at"]}')


def availability(summary, online=False):
    a = summary['artifact']
    if online:
        live = artifact_metadata(a['id'])
        require(live['digest'] == a['digest'] and live['workflow_run']['id'] == a['run_id'] and live['expires_at'] == a['expires_at'], 'Live artifact identity mismatch')
        return 'available (authenticated live check)'
    expired = dt.datetime.fromisoformat(a['expires_at'].replace('Z','+00:00')) <= dt.datetime.now(dt.timezone.utc)
    return 'unavailable (recorded expiry passed)' if expired else 'unconfirmed (authenticate with --online to check live availability)'


def verify(args):
    if args.bundle:
        verify_bundle(args.bundle)
        print('Private bundle verified: complete scenarios, hashes, outcomes, bindings and recovery invariants')
    else:
        summary = validate_public(read_json(args.summary))
        print('Historical successful run verified; private evidence is ' + availability(summary, args.online))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('run')
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--seed', type=int, default=63)
    p.add_argument('--out', type=Path, default=ROOT / 'build/mock/run')
    p.set_defaults(func=run)
    p = commands.add_parser('verify')
    choice = p.add_mutually_exclusive_group(required=True)
    choice.add_argument('--bundle', type=Path)
    choice.add_argument('--summary', type=Path)
    p.add_argument('--online', action='store_true', help='authenticated live artifact check; access denial is not expiry')
    p.set_defaults(func=verify)
    p = commands.add_parser('export')
    p.add_argument('--artifact-id', required=True, type=int)
    p.add_argument('--out', type=Path, default=ROOT / 'review/mock-summary.json')
    p.set_defaults(func=export)
    args = parser.parse_args()
    if args.command == 'run':
        require(1 <= args.repeats <= 100 and 0 <= args.seed < 2**64, 'Require repeats 1..100 and seed 0..2^64-1')
    if args.command == 'verify':
        require(not args.online or args.summary, '--online requires --summary')
    args.func(args)


if __name__ == '__main__':
    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    try:
        main()
    except (Invalid, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f'mock: {error}', file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print('mock: interrupted; service processes and runtime databases cleaned up', file=sys.stderr)
        sys.exit(130)
