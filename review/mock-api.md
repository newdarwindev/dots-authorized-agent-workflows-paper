# Private business API mock

The `mock/` Git submodule pins private repository [dots-paper-workflow-mock](https://github.com/newdarwindev/dots-paper-workflow-mock) at `de0dd7de282ee5590cfbdd1bd00696c15f56538b`.

It supplies two Go APIs with separate SQLite databases:

- **Business application:** workspaces, work requests, owner approvals, immutable output files, deliveries, independent acceptance review and activity.
- **Automation:** start work, inspect progress, check delivery, retry and cancel. The service uses the application HTTP API and has no access to its database.

Names, OpenAPI examples and a PHP cURL walkthrough are written for UI implementers. Fleet host/grant/receipt concepts map internally to workspace, approval and delivery records. The package contains no PHP frontend, provider/model calls, shell execution or real host enrollment.

## Reproduce

An authorized GitHub account must already have access to the private repository. No credentials are stored in the public repository, its workflows or its submodule URL.

```sh
git submodule update --init -- mock
cd mock
go test -race ./...
go vet ./...
go build ./cmd/...
go run ./cmd/evaluate -repeats 5 -seed 63 -out reports
```

Go 1.26.4 is used by private CI. SQLite is embedded in the Go services and needs no separate database server. The private README covers explicit database seeding, loopback service startup and the PHP walkthrough. Development tokens are synthetic fixture identities.

To update later, test the desired private commit, check it out within `mock/`, and commit the new gitlink in a paper PR. `git submodule update --init -- mock` restores the paper's exact pinned revision. A normal public checkout and the public PDF workflows do not initialize the private submodule; public readers can still reproduce the paper and decks.

## Protocol mapping and evidence limits

The private repository preserves `review/fleet-fixture.json` from paper commit `2ce8b35` byte-for-byte, including its historical proposed/unrun status. New executed synthetic checks are documented separately, without changing the provenance of that original fixture.

| Paper protocol | Mock checks |
|---|---|
| Missing authorization | File and delivery creation rejected; zero unauthorized effects |
| Grant A and verify A | Request-specific approval, actual persisted output bytes and independent review |
| A grant does not authorize B | Separate requests/workspaces; cross-workspace submissions rejected |
| Separately grant B | Independent B request approval and original fixture output/hash |
| Lost receipt after write | Synthetic lost response, persisted delivery lookup, idempotent reconciliation |
| Expired/revoked grant | Approval checked within write transaction; zero later writes |
| Compare conditions and ablations | Direct script, automation, fixed-workspace selection and omitted recovery |

Ten cases × five independent resets × four conditions produce 200 scheduled synthetic trials. Every trial uses actual loopback HTTP and temporary on-disk SQLite databases. Reports retain accepted results, stops, failures, unknowns, placement/recovery counts and observed timings. Human effort and actual costs remain unmeasured. The direct script is a synthetic comparison condition, not a native-product baseline. The deliberately corrupted-output case must be rejected; its reported failure is an expected acceptance check.

Local race tests, OpenAPI examples/live responses, restart persistence, concurrent duplicate prevention, authorization and transaction rollback checks passed before the private commit was pushed. Private CI also executes the PHP walkthrough and retains synthetic reports. Its commit-specific run is [available to authorized readers](https://github.com/newdarwindev/dots-paper-workflow-mock/actions/runs/41273104108).

**Classification:** tested synthetic mock. Real fleet placement/enrollment/recovery, model comparisons, human-effort measurements and commercial claims remain unrun or unknown. The paper's measured two-host pilot is still proposed. V1 Argument remains the published-source default; paper/deck sources and their 20/10-page contracts are unchanged by this integration.

## Issue #65 consumer decisions

D1-C and D2-C deliver parent-owned HTTP orchestration, verified evidence and
verification of the existing PHP example together. D3-A and D4-A retain an exact
clean gitlink and authorized local/private CI execution. D5-A exports only the
allowlisted synthetic summary; D6-C accepts 14-day Actions artifact expiry.
D7-C keeps the original functional experiment intact and adds separate service
measurements. D8-C adds this compact note and summary link without a demonstration
page. D9-A links the existing [PHP business-action guide (private access required)](https://github.com/newdarwindev/dots-paper-workflow-mock/blob/de0dd7de282ee5590cfbdd1bd00696c15f56538b/docs/php-ui-guide.md).
D10-B ships one coordinated paper integration PR; merging is a separate action.
New frontends, model comparisons and real-host experiments remain deferred.

## HTTP experiment and private evidence

From the paper root, with pre-existing private access, Go 1.26.4, Python 3.10+
and PHP CLI/cURL:

```sh
git submodule update --init -- mock
python3 -m venv build/mock-venv
build/mock-venv/bin/pip install -r scripts/mock-requirements.txt
build/mock-venv/bin/python -m unittest discover -s scripts/tests -v
build/mock-venv/bin/python scripts/mock.py run --repeats 5 --seed 63
build/mock-venv/bin/python scripts/mock.py verify --bundle build/mock/run
```

Commit consumer changes before a measured run. Missing access, a dirty checkout,
a wrong revision, changed fixture/descriptor or unsupported Go toolchain fails
without modifying the dependency. Output destinations must be new directories
under ignored `build/mock/`; pass `--out build/mock/another-run` to rerun.

The runner builds each binary once. Each of the ten cases × four conditions ×
five repetitions receives fresh SQLite files and two loopback service processes
on ephemeral ports. Readiness requires a published bound address and `/health`.
All business actions, approval/revocation, file uploads/downloads, delivery,
review and reconciliation use HTTP. Expiry setup waits for a short real approval
to expire before the clock starts. Reviewer credentials stay in separate clients.
Shutdown and temporary database deletion run even on exceptions or interruption.

The private versioned descriptor is checked against the unchanged Go functional
suite and original fixture bytes. The HTTP experiment uses `paired-sha256-v1`:
for each repetition and case, sort conditions by SHA-256 of
`paired-sha256-v1:seed:repeat:case:condition`. This seeded paired ordering is
reproducible independently of runtime RNG versions. Every trial resets state.
The existing functional experiment retains its original seeded Go ordering.

Service timing uses a monotonic clock **after initial startup, request creation
and approval setup**, through execution, scripted recovery, restart and independent
review until the terminal outcome. Compilation, fixture preparation, initial
startup, teardown and post-terminal evidence audit are excluded. Trials have a
60-second deadline and HTTP calls a five-second bound. A deadline records an
explicit unknown partial result and fails the run; unexpected infrastructure
failures also fail the run. Neither can become an expected business outcome.
Functional `duration_ms` still includes setup/teardown. Timings remain private.

The unchanged functional report and separately instrumented HTTP report each
retain all 200 scheduled rows. `direct_script` accesses both workspaces but omits
recovery after uncertainty; `without_placement` selects A and stops on B;
`without_recovery` never checks/retries uncertain writes. These are configured
actors. Corruption must be independently rejected. Unknown writes remain pending
without review, even if a read-only post-terminal observer can see a delivery.
Fault injection excludes cases skipped by an earlier placement stop. Recovery
eligibility includes injected response loss, pre-write failure and restart,
excludes corruption, and is evaluated per condition. No recovery rate is exported.
Human effort and actual cost remain unknown.

The manifest, trial evidence and public summary have explicit v1 schemas in
`review/schemas/`. Private bundles bind source parent/mock SHAs, original fixture,
protocol and descriptor digests, tools, seed/repetitions, timing definition,
report/log digests and CI provenance. Trial records preserve request/workspace,
approval/principal, downloaded bytes/hash, reviewer verdict/activity, delivery
count and HTTP action trace. Authentication headers and tokens are excluded.
Verification rejects incomplete/duplicate rows, wrong outcomes/counts, unauthorized
effects, duplicate deliveries, unreviewed accepted results and recovery without
reconciliation. Separate HTTP probes cover cross-workspace submission, replayed
operation keys, conflicting key reuse and actor self-review rejection.

## Evidence availability

**Deterministic synthetic simulation:** [approved historical outcome summary](mock-summary.json).
A successful historical run is distinct from currently available evidence. Full
records, timings and logs stay in private Actions artifacts for **14 days**. The
summary records the assigned artifact ID, archive digest, run URL, actual expiry
and authenticated verification time after upload. Once expiry passes, evidence
is **unavailable**, even though the historical outcome counts remain identifiable.
Before expiry, offline validation says availability is unconfirmed; a private
404/access denial also means unknown access, not confirmed expiry.

```sh
# Public validation requires no private source checkout or GitHub credentials:
build/mock-venv/bin/python scripts/mock.py verify --summary review/mock-summary.json
# Existing authenticated access is needed to check current artifact availability:
build/mock-venv/bin/python scripts/mock.py verify --summary review/mock-summary.json --online
```

To regenerate, publish/test a private revision first and commit its exact gitlink
plus matching descriptor contract in a paper candidate. Run the private workflow
at that private revision with the explicit **40-character paper candidate SHA**:

```sh
gh workflow run test.yml --repo newdarwindev/dots-paper-workflow-mock \
  --ref PRIVATE_REVISION -f parent_sha=PAPER_CANDIDATE_SHA
# After the entire integration workflow succeeds, use its artifact ID:
build/mock-venv/bin/python scripts/mock.py export --artifact-id ARTIFACT_ID
build/mock-venv/bin/python scripts/mock.py verify --summary review/mock-summary.json --online
```

Export downloads the authenticated artifact, checks its archive digest and
successful workflow/source binding, validates every private row, then constructs
a new object from a strict public allowlist. Only names, scheduled/outcome counts,
limitations and provenance leave the private bundle. Review that JSON before
committing it. Public CI validates the schema, expected counts and pin/provenance
without checking out `mock/` or using private credentials. The landing note
computes expiry from the summary; it never claims live private availability.

The summary's `parent_source_sha` identifies the executed consumer source; the
later documentation commit that contains the summary is identified by Git history
and the PR head. This avoids a self-referential source SHA. A documentation-only
commit does not imply that its own revision was measured.

For upgrades, record old/new pins, schema/descriptor changes and private/public
CI links, regenerate evidence, and commit the pin and matching snapshot together.
Rollback restores both from the same known-good paper revision:

```sh
git restore --source=KNOWN_GOOD_PAPER_SHA -- mock review/mock-contract.json review/mock-summary.json review/mock-api.md
git submodule update --init -- mock
# Then validate the restored public summary and commit the rollback.
```

For a pre-consumer revision such as `4e02bab`, restore its pin/note and remove the
new summary/contract and consumer CI steps together; that revision has no consumer
snapshot. Never pair a later summary with an older mock pin. Six wontfix issues
#45, #47, #49, #51, #53 and #54 remain excluded.
