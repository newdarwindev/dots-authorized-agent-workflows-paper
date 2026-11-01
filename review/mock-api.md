# Private business API mock

The `mock/` Git submodule pins private repository [dots-paper-workflow-mock](https://github.com/newdarwindev/dots-paper-workflow-mock) at `6f94dbc529630270638c6b4a240fd4671922ef17`.

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
