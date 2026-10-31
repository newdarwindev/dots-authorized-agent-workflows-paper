# The Aftermarket Imperative

An original 20-page position paper and 10-slide Beamer presentation by newdarwindev. Both PDFs and all TeX/BibTeX sources are public and editable.

- [Landing page](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/)
- [Paper PDF](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/paper.pdf)
- [Beamer PDF](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/deck.pdf)

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
