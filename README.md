# The Aftermarket Imperative

An original 20-page position paper and 10-slide Beamer presentation by newdarwindev. Both PDFs and all TeX/BibTeX sources are public and editable.

- [Landing page](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/)
- [Paper PDF](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/paper.pdf)
- [Beamer PDF](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/deck.pdf)

## Review the open-issue variations

The [decision index](review/decisions.md) covers 55 open planning, evidence and
package decisions. Issues #45, #47, #49, #51, #53 and #54 are labeled wontfix
and are excluded. Every included issue has a proposed disposition, rationale,
alternatives and unchecked selection boxes. Retaining an existing feature or
deferring an unnecessary dependency is an explicit decision.

Three complete ten-page decks share the argument and differ on slides 5 and 7:

| Option | Source | Preview |
| --- | --- | --- |
| Argument (proposed default) | [deck.tex](deck.tex) | [PDF](docs/review/argument.pdf) |
| Synthetic evidence | [deck-evidence.tex](deck-evidence.tex) | [PDF](docs/review/evidence.pdf) |
| Proposed fleet evaluation | [deck-fleet.tex](deck-fleet.tex) | [PDF](docs/review/fleet.pdf) |

Open [the local review gallery](docs/review/index.html) after downloading the
repository, or review the PR's embedded previews and checkboxes. Gallery controls
are previews only; save preferences in the PR. Choose one variant and one option
per issue (one per D1/D2/D3 for #1); resolve conflicting choices before merging.
Checking a box does not run code or change the source. The proposed default is
argument; to adopt another option, change the default variant in deck.tex before
merging and rebuild all outputs.

The [fleet protocol](review/fleet-protocol.md) is a proposed, unrun comparison.
The [asset provenance](assets/provenance.json) pins the genuine synthetic-demo
images and test source. The [HTTP checks](review/link-checks.json) record
reachability separately from the earlier content audit, runtime/CI and playback.
No tests in other repositories were rerun.

After building paper.tex and all three deck entrypoints into build, regenerate
and check the review with:

    python3 scripts/review.py
    python3 scripts/verify.py
    python3 scripts/render.py

Verification needs pypdf 5.9.0; rendering needs Pillow 12.0.0 and Poppler.
The PR workflow builds every option with the same XeLaTeX/TeX Live 2025 contract
as publication and retains every page render, PDF and log as an artifact.

## Argument

The paper argues that a high-leverage commercial research opportunity for some teams outside frontier laboratories is **aftermarket harness engineering**: making consumer-accessible frontier AI products complete valuable, legitimate work they currently decline or leave unfinished without repeated user nudging. The saleable unit is an independently accepted task result. The claim that this is the *greatest* opportunity is an argued hypothesis, not an empirical ranking.

An observed stop can reflect limited model capability, missing product context or tools, missing authority, a proper safety refusal, or a platform restriction. The proposed research separates these causes and compares stock products, expert nudging, conventional automation, and a same-model aftermarket harness. It accounts for human effort, verification, exceptions, maintenance, and provider improvements. Credential connection, enrollment, and authorized defensive work are brief illustrations, not proposed bypasses. The paper reports no new benchmark, deployed prototype, market size, or return on investment.

## Sources

- `paper.tex` and `sections/*.tex`: manuscript
- `deck.tex`: Beamer slides
- `references.bib`: primary papers and official reports
- `figures/*.tex`: seven editable TikZ, PGFPlots, and Forest figures
- `docs/index.html`: GitHub Pages landing page
- `.github/workflows/publish.yml`: pinned standard-runner build and Pages publication

## Build locally

Tectonic 0.16.9 or a compatible XeLaTeX toolchain is required. From the repository root:

```sh
mkdir -p build
tectonic -X compile paper.tex --outdir build
tectonic -X compile deck.tex --outdir build
pdfinfo build/paper.pdf | grep Pages   # 20
pdfinfo build/deck.pdf | grep Pages    # 10
```

The public GitHub Actions workflow uses the standard `ubuntu-24.04` runner, TeX Live 2025, pinned actions, and a pinned PDF parser. It verifies the page and slide counts before Pages deployment, then writes the producing commit to [source-commit.txt](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/source-commit.txt). No repository secrets or paid runner are required.

## Private business API mock

The optional [`mock/`](https://github.com/newdarwindev/dots-paper-workflow-mock) Git submodule contains a private Go/SQLite application and automation API with business-facing resources, a PHP client guide, OpenAPI, and deterministic synthetic tests. Access to the private repository is required; the paper, deck and their public build remain independent of it.

```sh
# From an authorized checkout of this paper repository:
git submodule update --init -- mock
python3 -m venv build/mock-venv
build/mock-venv/bin/pip install -r scripts/mock-requirements.txt
build/mock-venv/bin/python scripts/mock.py run --repeats 5 --seed 63
build/mock-venv/bin/python scripts/mock.py verify --bundle build/mock/run
```

The submodule pins a reviewed implementation commit; it does not follow the private repository's branch automatically. See [mock scope, setup and protocol mapping](review/mock-api.md). These checks test synthetic workflows and recovery; they do not establish real fleet capability, model performance or commercial advantage.

The parent-owned command verifies the committed pin and clean source, runs the
unchanged functional suite and a separate 200-trial HTTP experiment, then checks
the existing PHP client. Go 1.26.4 and PHP CLI with cURL are required. Generated
files stay under ignored `build/mock/`.

**Deterministic synthetic simulation:** the [approved outcome summary](review/mock-summary.json)
is a historical run record. Full evidence is private and retained for 14 days;
current availability requires authenticated verification and becomes unavailable
after expiry. See [availability, reproduction and rollback](review/mock-api.md#evidence-availability).
