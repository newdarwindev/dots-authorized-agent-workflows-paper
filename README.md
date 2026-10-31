# Authorized Agent Workflows

An original technical position paper and Beamer briefing for applied AI researchers, product engineers, and founders.

- [Published landing page](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/)
- [20-page whitepaper](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/paper.pdf)
- [10-slide presentation](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/deck.pdf)

The paper argues that owner-authorized workflow engineering around general models may be a major commercial research opportunity. It distinguishes capability, integration, authorization, product/safety policy, and third-party platform restrictions. The superlative version of the thesis is a hypothesis to test, not an empirical finding. No prototype, benchmark result, ROI, or savings claim is asserted.

## Source map

- `paper.tex` — complete manuscript
- `deck.tex` — editable Beamer presentation
- `references.bib` — cited primary papers and official documentation
- `figures/architecture.tex` — reusable editable TikZ architecture figure
- `docs/index.html` — GitHub Pages landing page
- `.github/workflows/publish.yml` — public standard-runner PDF build, length validation, and Pages deployment

## Local build

With Tectonic 0.16.9 or a compatible XeLaTeX toolchain:

```sh
mkdir -p build
tectonic -X compile paper.tex --outdir build
tectonic -X compile deck.tex --outdir build
pdfinfo build/paper.pdf | grep Pages
pdfinfo build/deck.pdf | grep Pages
```

The GitHub workflow uses a pinned LaTeX action, TeX Live 2025, `ubuntu-24.04` standard hosted runners, and pinned Pages actions. It verifies the PDF lengths before publishing. No external credentials, paid runners, or repository secrets are required.

## Scope and evidence

The architecture is illustrative. Credential storage, account enrollment, and publication are framed as permissioned workflows with human handoff. The paper does not propose circumventing site controls, altering model safeguards, or using credentials without the owner's authority. Historical benchmarks inform the evaluation method, not current market estimates.

The sources are newly authored text and TikZ. Bibliography entries link to public papers and official documentation. A `source-commit.txt` file on Pages identifies the exact commit that produced the live PDFs.
