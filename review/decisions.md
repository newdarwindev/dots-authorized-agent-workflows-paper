# Open-issue review

Snapshot: 2026-11-01. 55 decisions; six wontfix issues excluded. Proposals are reviewable dispositions, not selected preferences. Choose one option per issue (one per D1/D2/D3 for #1) in the PR. Multiple choices in a group conflict; reconcile before merging.

Three full ten-page options: deck.tex (argument, proposed default), deck-evidence.tex (synthetic evidence), deck-fleet.tex (proposed fleet). Only slides 5 and 7 vary; all preserve thesis, boundaries and economics.

Excluded without changes: #45, #47, #49, #51, #53, #54.

Package/build evidence is in validation.txt and the retained CI TeX logs. Deferred packages are not added. HTTP reachability is not runtime/CI verification.

## #1 — Fleet product brief: dots-authorized-agent-workflows-paper positioning and decision matrix

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/1)

Proposed: **D1-A / D2-A / D3-A**. Add a proposed two-host evaluation, explicitly authorized placement and independent receipts, sanitized fixtures, metric definitions and failure cases. All fleet execution remains unrun.

- [ ] D1-A — Matched native versus authorized fleet comparison
- [ ] D1-B — Within-fleet placement/recovery ablation
- [ ] D2-A — Full predefined metrics
- [ ] D2-B — Feasibility study
- [ ] D3-A — Editable TeX diagram
- [ ] D3-B — Versioned static vector

Original acceptance requirements (not certified passed):

Documented proposed test; do not claim a fleet experiment has run.

## #2 — [CTAN decision] beamer: Native frames, columns, templates, handout mode

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/2)

Proposed: **D1-A**. Use the existing Beamer theme, dynamic total-frame counter, consistent evidence/limitation captions and no overlays.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Verify 10 frames and exactly 10 output pages. Replace hard-coded total only if it preserves the same visual contract; overlays must not silently increase page count.
- [ ] AC3 — Given the same ten-slide content, when rendered at presentation and read-alone sizes, then hierarchy, margins and evidence labels are consistent with no clipping, overcrowding or unreadably scaled text.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #3 — [Evidence decision] Aftermarket deck and companion paper

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/3)

Proposed: **A**. Keep the ten-slide argument as the editorial spine; add a compact claim → evidence → limitation strip and clickable bibliography. Highest priority: protect the falsifiable thesis rather than add portfolio decoration. The 20-page paper reports no new benchmark, market estimate or ROI.

Evidence boundary (issue audit): Published source `88b0465`; position paper, **no new benchmark, market estimate or ROI**

[Aftermarket deck](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/deck.pdf) · [paper](https://newdarwindev.github.io/dots-authorized-agent-workflows-paper/paper.pdf)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Verify the chosen paper/deck build SHA and page counts, retain bibliography, and label thesis/economics as hypotheses rather than personal achievements.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #4 — [CTAN decision] beamertheme-metropolis: Restrained presentation theme

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/4)

Proposed: **D1-B**. Keep the custom NewPX theme across the three full-deck comparisons. Metropolis adds a font/theme migration without resolving an evidence gap; revisit only after a typography comparison is requested.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Compare one render using the theme against the current custom theme. Pin fonts and select only one theme strategy; inspect all ten slides, not only the title.
- [ ] AC3 — Given the same ten-slide content, when rendered at presentation and read-alone sizes, then hierarchy, margins and evidence labels are consistent with no clipping, overcrowding or unreadably scaled text.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #5 — [CTAN decision] tcolorbox: Reusable titled content boxes

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/5)

Proposed: **D1-A**. Use one compact native Beamer claim/evidence/limitation treatment. This achieves the requested visual grammar without adding tcolorbox to the deck; the paper retains its existing boxes.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Render claim/evidence/limit cards containing the longest actual labels. Boxes stay within frame bounds and their visual statuses are not interchangeable.
- [ ] AC3 — Given the same ten-slide content, when rendered at presentation and read-alone sizes, then hierarchy, margins and evidence labels are consistent with no clipping, overcrowding or unreadably scaled text.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #6 — [Evidence decision] Refinery acceptance tests and walkthrough

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/6)

Proposed: **A**. On slide 7 pair one readable gate/rollback assertion with a walkthrough still and source link. Four authored Playwright tests and a matching successful showcase build make bounded evidence inspectable; they do not demonstrate real DSPy training or model-quality gains.

Evidence boundary (issue audit): Four authored Playwright tests; matching successful showcase build; **not real DSPy training or model-quality evaluation**

[Refinery test source](https://github.com/newdarwindev/dots-workflow-refinery-demo/blob/ecd6c3eda92d442b983d5c6d1d40435442f8a49a/tests/flow.spec.js) · [walkthrough](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/artifacts/workflow-walkthrough.webm)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Match shown assertions to pinned ecd6c3e test source. Sample selected video frame and record it as actual UI interaction, not DSPy execution; distinguish four authored tests from model experiments.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #7 — [CTAN decision] adjustbox: Size, trim and align boxed material

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/7)

Proposed: **D1-B**. Use native graphicx width/height bounds and keepaspectratio; adjustbox is unnecessary for the verified layouts.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Inspect the smallest text after adjustment. Reject a solution that merely fits by shrinking type; verify cropped links and labels remain usable.
- [ ] AC3 — Given the same ten-slide content, when rendered at presentation and read-alone sizes, then hierarchy, margins and evidence labels are consistent with no clipping, overcrowding or unreadably scaled text.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #8 — [Evidence decision] Browser workflow architecture

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/8)

Proposed: **C**. Keep the portal/broker, Temporal, OpenBao and identity boundaries in a linked architecture reference; do not imply the offline checks establish full integration.

Evidence boundary (issue audit): Page distinguishes local synthetic checks from planned integrations; **not a deployed credential backend**

[Browser workflows architecture](https://newdarwindev.github.io/dots-browser-workflows-docs/#architecture)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Annotate each selected component as locally tested, synthetic or planned. Ensure the diagram never implies production credential storage or independently verified full integration.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #9 — [Evidence decision] Refinery review UI and screenshot

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/9)

Proposed: **A**. On slide 5 use a cropped review screenshot plus three callouts: redact, simulated evaluation, promotion/rollback. The UI is visually concrete and relevant to controlled workflows. Mark examples synthetic and 78%/92% invented demo values, not measured improvement.

Evidence boundary (issue audit): Real UI, **synthetic examples and simulated evaluation**; 78%/92% are invented demo values

[Workflow refinery demo](https://newdarwindev.github.io/dots-workflow-refinery-demo/) · [review screenshot](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/artifacts/review.png)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Keep SYNTHETIC/DEMO labels legible in the cropped screenshot. Show review gate state accurately and label 78%/92% invented rather than performance gains.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #10 — [CTAN decision] pgf: TikZ vector diagrams

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/10)

Proposed: **D1-A**. Reuse editable TikZ/PGF figures and add scoped host lanes, placement, receipts and verifier in the fleet option.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Review each arrow direction and legend against the source narrative. Reuse common styles and existing libraries, with no externalization requirement added.
- [ ] AC3 — Given the documented boundaries and terminal states, when the diagram is read without narration, then every permitted transition, human checkpoint and stop is distinguishable; conceptual paths must not look like measured execution.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #11 — [Evidence decision] Refinery Storybook states and vision

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/11)

Proposed: **C**. Keep the six UI states in the linked Storybook, not six claimed workflows or extra core frames.

Evidence boundary (issue audit): States/proposals, **not six independently proven workflows**

[Refinery Storybook](https://newdarwindev.github.io/dots-workflow-refinery-demo/storybook/) · [vision](https://newdarwindev.github.io/dots-workflow-refinery-demo/vision.html)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Verify selected story ID against deployed index. Count six UI states, not workflows, and keep the vision's hypothetical refinement loop separate from implemented UI.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #12 — [CTAN decision] forest: Automatically packed trees

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/12)

Proposed: **D1-B**. Use existing TikZ for a boundary-first diagnostic tree with readable permitted responses. Keep Forest in the paper; no need to add it to the deck.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Check the boundary-first branching against paper figure 2, preserve the distinction between product/capability/authority causes and allow mixed causes in the caption.
- [ ] AC3 — Given the documented boundaries and terminal states, when the diagram is read without narration, then every permitted transition, human checkpoint and stop is distinguishable; conceptual paths must not look like measured execution.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #13 — [Evidence decision] Refinery paper and presentation

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/13)

Proposed: **C**. Link the original five-page concept paper and ten-slide deck; the main deck retains its own mechanism narrative.

Evidence boundary (issue audit): Design explanations, not evidence of a live platform

[Refinery paper](https://newdarwindev.github.io/dots-workflow-refinery-demo/resources/workflow-refinery-white-paper.pdf) · [deck](https://newdarwindev.github.io/dots-workflow-refinery-demo/resources/workflow-refinery-presentation.pdf)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Map selected PDF pages/figures to their original sources; keep proposal legends and do not duplicate the detailed visual-family decisions below.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #14 — [Evidence decision] Dot-status visual evidence

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/14)

Proposed: **C**. Link the evidence gallery and its synthetic-telemetry limitation; omit uninspected videos from performance claims.

Evidence boundary (issue audit): Real Chromium interactions with **synthetic telemetry**; functional tests, not pixel-diff assertions or real uptime

[Dot-status evidence](https://newdarwindev.github.io/dot-status-demo/evidence/)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Match selected screenshot/video to deployed f3e75eef evidence gallery, preserve synthetic telemetry label, and distinguish functional interaction tests from pixel-diff testing.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #15 — [CTAN decision] pgf-umlsd: Sequence diagrams

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/15)

Proposed: **D1-B**. Use existing TikZ host lanes; a second sequence-diagram engine provides no required feature.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Trace owner, broker, browser and verifier lifelines. Retained approval and unknown-result reconciliation must not disappear from the sequence.
- [ ] AC3 — Given the documented boundaries and terminal states, when the diagram is read without narration, then every permitted transition, human checkpoint and stop is distinguishable; conceptual paths must not look like measured execution.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #16 — [Evidence decision] Completion-wedge visual

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/16)

Proposed: **A**. On slide 2 use the existing completion wedge with direct curve labels and a prominent hypothesis caption. It quickly explains the main delivery-gap thesis. Keep axes conceptual: no numeric lift, measured propensity or commercial success can be inferred.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slide 2 · hypothesized delivery gap

[TeX](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/completion-wedge.tex)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Keep hypothesized completion wedge label visible. Do not introduce quantitative ticks or measured-superiority language for hand-authored curves.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #17 — [CTAN decision] booktabs: Readable table rules and spacing

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/17)

Proposed: **D1-A**. Retain booktabs, short wrapped tables and no vertical rules for evidence and outcome states.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Check longest evidence and limitation cells. Use no misleading merged outcomes, no vertical-rule clutter, and no tiny scaled table.
- [ ] AC3 — Given a dated source with a stated denominator, when values enter the table/plot, then units, unknowns, exclusions and cutoff remain visible; conceptual curves carry no invented measured ticks.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #19 — [CTAN decision] tabularray: Declarative table widths, styles and cells

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/19)

Proposed: **D1-B**. Use ordinary wrapped tabular/booktabs in the deck and a separate HTML artifact matrix; no need to add tabularray to Beamer.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Compile with the pinned TeX Live 2025 package version. Compare wrapping and spacing with the existing tabular/booktabs alternative.
- [ ] AC3 — Given a dated source with a stated denominator, when values enter the table/plot, then units, unknowns, exclusions and cutoff remain visible; conceptual curves carry no invented measured ticks.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #20 — [Evidence decision] Refusal diagnosis tree

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/20)

Proposed: **A**. Slide 3 needs a compact diagnosis tree: incapacity, missing context/tool, missing authorization, or proper stop. Label each permitted response explicitly. This is central to the thesis and safety boundary; an observed refusal alone does not prove latent capability or justify bypassing a stop.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slide 3 · boundary/cause diagnosis

[TeX](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/refusal-tree.tex)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Retain correct policy/platform boundary as a stop, distinguish capability/product/authority gaps, and do not imply bypass or hidden capability.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #21 — [CTAN decision] siunitx: Consistent numbers, units and aligned numeric columns

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/21)

Proposed: **D1-C**. Defer until a reviewed measurement export has real units, denominators and uncertainty. No numeric results are invented.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Verify number/unit formatting and alignment with missing values and uncertainty. Do not convert a missing measurement to zero.
- [ ] AC3 — Given a dated source with a stated denominator, when values enter the table/plot, then units, unknowns, exclusions and cutoff remain visible; conceptual curves carry no invented measured ticks.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #22 — [Evidence decision] Translation-contract visual

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/22)

Proposed: **A**. Slide 5 should use four aligned Specify / Reach / Persist / Prove cards, each linked to an artifact and a limitation. This is the paper’s central mechanism, so clarity outranks ornamental changes. The contract is conceptual, not four shipped capabilities.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slide 5 · four obligations

[TeX](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/translation-contract.tex)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Preserve all four obligations Specify/Reach/Persist/Prove and connect each to only the actual selected artifact's demonstrated scope.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #23 — [Evidence decision] Nudge-ledger visual

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/23)

Proposed: **A**. On slide 4 use parallel human/system swimlanes to expose reframing, context transfer, approval and checking. Preserve genuine human decisions while illustrating reduced tactical steering. Highest priority for the nudge-tax thesis; lane lengths are not measured minutes or claimed savings.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slide 4 · human/system responsibilities, not measured time

[TeX](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/nudge-ledger.tex)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Keep owner approvals and final verification on both paths. Label touch reductions schematic, not measured user minutes saved.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #24 — [Evidence decision] Paired-comparison visual

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/24)

Proposed: **A**. On slide 7 retain four comparable arms converging on one independent verifier: stock product, expert nudging, deterministic integration, harness. Make shared tasks/permissions visible and match stock/harness model versions. This is the falsification design, not a completed benchmark or ranking.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slide 7 · shared tasks/verifier

[TeX](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/paired-test.tex)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Preserve same held-out tasks, permissions and independent acceptance rule across all four arms. Explicitly label experiment design rather than executed comparison.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #25 — [CTAN decision] pgfplots: Axes, curves, bars and uncertainty plots

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/25)

Proposed: **D1-A**. Reuse existing PGFPlots schematics with compat=1.18, nonnumeric axes, direct labels and distinct dash patterns.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Retain compat=1.18 unless separately justified. Conceptual durability curves stay explicitly conceptual; measured plots need source data and denominator.
- [ ] AC3 — Given a dated source with a stated denominator, when values enter the table/plot, then units, unknowns, exclusions and cutoff remain visible; conceptual curves carry no invented measured ticks.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #26 — [Evidence decision] Economics and durability visuals

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/26)

Proposed: **A**. Slides 8–9 should pair the cost-per-accepted-outcome denominator with clearly labeled conceptual durability scenarios. Keep pending/unknown/correctly stopped separate from accepted completions. Strong thesis fit, but curves are not forecasts and no ROI or measured market advantage is established.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slides 8–9 · hypotheses, no ROI or forecasts

[Amortization](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/amortization.tex) · [durability](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/blob/88b04652f828514f41c5b51aea44198631066ee0/figures/durability-fan.tex)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Keep conceptual labels and distinct line styles. Show no measured ROI, break-even point, trajectory or forecast unless later separately sourced data supports it.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #27 — [CTAN decision] pgfplotstable: Load and format numerical evidence tables

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/27)

Proposed: **D1-C**. Defer numerical table loading until a versioned measured dataset exists; the review manifest is editorial metadata.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Compare every output value with the reviewed input CSV, including missing values and rounding. Record input version/cutoff.
- [ ] AC3 — Given a dated source with a stated denominator, when values enter the table/plot, then units, unknowns, exclusions and cutoff remain visible; conceptual curves carry no invented measured ticks.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #28 — [Evidence decision] Dataset control-plane and provenance diagrams

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/28)

Proposed: **C**. Link the grouped control-plane/provenance diagrams, preserving separate holdout, experiment and owner-reviewed promotion paths.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slides 5, 7 · reviewed examples → holdout → candidate → separately reviewed promotion

[Data PDF](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/04-golden-data.pdf) · [planes](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/05-control-planes.pdf) · [lineage](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/07-provenance.pdf)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Keep reviewed/grouped splits and held-out boundary visible. Separate experiment runner from human-reviewed deployment path; no training or automatic-promotion claim.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #29 — [Evidence decision] Scope lifecycle and approval diagrams

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/29)

Proposed: **C**. Link the grouped identity/lifecycle/approval design references; retain request, grant, execution and terminal-evidence distinctions.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Slides 3–5 · identity binding and authorized state transitions

[Identity PDF](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/01-identity.pdf) · [lifecycle](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/02-lifecycle.pdf) · [approval](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/03-approval.pdf)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Preserve canonical identity binding, observation-only external sessions, and actor/scope checks before execution. Do not imply that these public diagrams prove live service operation.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #30 — [CTAN decision] csvsimple: Filter CSV rows and generate tables

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/30)

Proposed: **D1-B**. Generate the artifact index from reviewed JSON with Python's standard library, escaping HTML/Markdown; no TeX CSV dependency.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Use a small curated manifest with long URLs and TeX-special characters. Verify escaping, row filtering and exact link targets without assuming sorting/database features.
- [ ] AC3 — Given a dated source with a stated denominator, when values enter the table/plot, then units, unknowns, exclusions and cutoff remain visible; conceptual curves carry no invented measured ticks.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #31 — [Evidence decision] Fleet topology and observation diagrams

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/31)

Proposed: **C**. Keep topology/observation references outside the core deck. Concept hosts are not active hosts, and missing observation is unknown.

Evidence boundary (issue audit): Conceptual/design visual, not measured outcome. Optional mechanism detail · **concept fleet, not active hosts**; silence does not establish failure

[Topology PDF](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/06-constellation.pdf) · [observation](https://raw.githubusercontent.com/newdarwindev/dots-workflow-refinery-demo/main/figures/pdf/08-observation.pdf)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Retain manual-placement/proposed fleet labels. Missing observations mean unknown, not failed; no assertion of active hosts or actual fleet uptime.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #32 — [Evidence decision] Backup-status denominators

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/32)

Proposed: **C**. Link only the dated denominator example with overlapping-record, exclusions and cutoff warnings.

Evidence boundary (issue audit): Snapshot 2026-10-31 22:58:59 UTC: two baselines and 1,990 **overlapping archived records**, not unique messages. Excludes DMs/attachment bytes; not billing usage

[Backup status](https://newdarwindev.github.io/dots-slackdump-status/)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Preserve cutoff2026-10-31T22:58:59Z and explain1990 overlapping archived records across two baselines. Do not label them unique messages, billing usage or complete workspace coverage.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #33 — [CTAN decision] listings: Read source snippets without external highlighter

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/33)

Proposed: **D1-A**. Use listings for a short literal gate assertion from pinned ecd6c3e source in the evidence deck. The original test file is vendored with provenance.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Compile fragile Beamer frames with the actual excerpt and relevant Unicode. Confirm no external highlighter is required and no assertion is clipped.
- [ ] AC3 — Given a pinned source excerpt, when the evidence is typeset, then its text and line scope match that source, fit at readable size, and retain the synthetic-fixture qualification; do not imply model-quality results.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #34 — [Evidence decision] Dated pipeline tracker

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/34)

Proposed: **C**. Link only the dated manual tracker snapshot; report zero training/model calls as historical source statements, not current status.

Evidence boundary (issue audit): **Outdated manual snapshot: 2026-10-31 22:41:32 UTC**. It reports 34 channels, 1,072 records, 19 notebook + 157 consumer tests; splits 0/0/0 and zero real model calls/training/deployments. Not current live status, all-channel totals or model performance

[Pipeline tracker](https://newdarwindev.github.io/dots-prompt-tracker-public/)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Recheck the public snapshot timestamp before inclusion. If reused, explicitly retain 2026-10-31T22:41:32Z and counts34/1072/19/157 with zero splits/calls/training/deployments, not live status or model quality.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #35 — [CTAN decision] minted: Pygments-based syntax highlighting

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/35)

Proposed: **D1-C**. Defer minted: the readable source excerpt needs neither Pygments nor shell escape.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Before adoption, document latexminted/Pygments availability and permitted execution setup in the pinned environment. A missing helper is a blocker, not permission to enable unrestricted execution.
- [ ] AC3 — Given a pinned source excerpt, when the evidence is typeset, then its text and line scope match that source, fit at readable size, and retain the synthetic-fixture qualification; do not imply model-quality results.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #36 — [CTAN decision] fvextra: Verbatim line wrapping and improved formatting

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/36)

Proposed: **D1-C**. Defer fvextra: no long receipt/log excerpt currently needs its wrapping features.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Test a longest literal receipt line and wrapping without altering copied content. Document current tagged-PDF compatibility limitations.
- [ ] AC3 — Given a pinned source excerpt, when the evidence is typeset, then its text and line scope match that source, fit at readable size, and retain the synthetic-fixture qualification; do not imply model-quality results.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #37 — [Evidence decision] DSPy architecture proposal

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/37)

Proposed: **C**. Link only the proposed architecture source. No deployed system or measured optimization is asserted.

Evidence boundary (issue audit): Source-only proposal; no verified Pages/PDF/release/Actions deployment

[DSPy refinery architecture](https://github.com/newdarwindev/dots-dspy-refinery-architecture)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Present only source design and synthetic contract; no deployed Pages/model/service claim. Show review-before-promotion and source-only status beside any architecture view.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #38 — [Evidence decision] Repository sitemap navigation

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/38)

Proposed: **A**. Provide a concise Paper / Source / Demo / Test evidence index on slide 10; directory membership is not proof of functioning products.

Evidence boundary (issue audit): Dated 2026-10-31 22:37; distinguishes deploy/CI/HTTP. A directory is not proof every product works

[Repository sitemap](https://newdarwindev.github.io/dots-repo-sitemap-public/)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Show cutoff2026-10-31T22:37 and independent CI/deploy/HTTP statuses. Check chosen destination links and never treat a directory entry as functional verification.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #39 — [CTAN decision] latexdiff: Review differences between TeX revisions

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/39)

Proposed: **D1-B**. Use the PR's native TeX source diff plus before/after rendered contact sheets. No latexdiff/Perl execution path is needed.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Generate only a separate review artifact in a later authorized implementation. Confirm changes to claims are visible and TikZ/layout macros do not create misleading redline output.
- [ ] AC3 — Given a pinned source excerpt, when the evidence is typeset, then its text and line scope match that source, fit at readable size, and retain the synthetic-fixture qualification; do not imply model-quality results.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #40 — [Evidence decision] Storage-fleet synthetic UI

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/40)

Proposed: **D**. Defer showcase until deployment/source mismatch and missing evidence route are reconciled; no work in the storage repository is included.

Evidence boundary (issue audit): **Live page is an older successful `383577c` deployment. Latest `36f0cfc` Quality-and-Pages run failed; `/evidence/` is 404.** No live fleet, real deletion or latest-CI-pass claim

[Storage fleet UI](https://newdarwindev.github.io/storage-fleet-demo/)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Verify live deploy SHA separately from source HEAD. Retain audited383577c live/36f0cfc failed-run distinction and evidence404 unless genuinely reverified; preserve fictional machines and in-memory cleanup.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #41 — [CTAN decision] hyperref: Clickable artifact, source and internal links

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/41)

Proposed: **D1-A**. Configure Beamer's existing hyperref with hypersetup, descriptive evidence links and explicit PDF outline entries; verify PDF annotations.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Inspect actual PDF link annotations for the selected source/demo/test URLs. Configure the Beamer-loaded package rather than introducing option clashes.
- [ ] AC3 — Given the generated PDF, when each relevant hyperlink/reference is activated, then it reaches the intended artifact/target with a meaningful label; inaccessible or changed destinations fail review.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #42 — [Evidence decision] Sidecar infrastructure proposal

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/42)

Proposed: **D**. Defer reuse until the two-cluster/small-stack design conflict is resolved in its source repository.

Evidence boundary (issue audit): Docs-only at audited `738c65c`; older two-cluster narrative conflicts with newer small-stack direction. Not deployed infrastructure

[Sidecar/cloud infrastructure](https://github.com/newdarwindev/dots-local-sidecar-cloud-infrastructure)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Before using, reconcile older two-cluster narrative with small-stack direction, label audited738c65c docs-only state, and leave hardware inventory/deployment unknown. No new infrastructure work in this issue.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #43 — [CTAN decision] bookmark: Structured PDF outline

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/43)

Proposed: **D1-B**. Use existing hyperref pdfbookmark anchors for Problem, Mechanism, Evidence and Limits; do not add bookmark.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Open the PDF outline and follow every entry. Avoid duplicate section destinations and stale page targets.
- [ ] AC3 — Given the generated PDF, when each relevant hyperlink/reference is activated, then it reaches the intended artifact/target with a meaningful label; inaccessible or changed destinations fail review.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #44 — [Evidence decision] Cloud-onboarding handoff example

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/44)

Proposed: **C**. Link only the four-gate offline handoff example; no connected-account execution is claimed.

Evidence boundary (issue audit): Source/checks exist; no connected accounts or hosted product claimed

[Cloud onboarding](https://github.com/newdarwindev/cloud-onboarding-demo)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Keep public research→owner approval→human handoff→authorized verification gates. Distinguish offline validator checks from provider/account integration.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #46 — [CTAN decision] cleveref: Type-aware figure/table/equation references

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/46)

Proposed: **D1-B**. Use descriptive links and explicit slide/figure names in the review index; no cross-reference automation is needed for ten frames.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Rename/reorder a test figure label in a controlled draft and verify generated reference type/number. Do not confuse internal labels with external-repository discovery.
- [ ] AC3 — Given the generated PDF, when each relevant hyperlink/reference is activated, then it reaches the intended artifact/target with a meaningful label; inaccessible or changed destinations fail review.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #48 — [CTAN decision] qrcode: Generate QR code in TeX

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/48)

Proposed: **D1-C**. Defer until a projection/scanning requirement exists. Ordinary descriptive hyperlinks remain usable and extractable.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Scan the actual rendered code at expected display size. Show the same destination as a descriptive ordinary link and retain a non-QR access route.
- [ ] AC3 — Given the generated PDF, when each relevant hyperlink/reference is activated, then it reaches the intended artifact/target with a meaningful label; inaccessible or changed destinations fail review.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #50 — [CTAN decision] natbib: Author-year or numeric bibliography

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/50)

Proposed: **D1-A**. Reuse references.bib with natbib and the BibTeX pipeline; cite methodological sources on relevant slides, retaining the paper bibliography.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Build using the existing references.bib/BibTeX path; no unresolved citations, and every cited claim preserves the paper source’s scope.
- [ ] AC3 — Given the generated PDF, when each relevant hyperlink/reference is activated, then it reaches the intended artifact/target with a meaningful label; inaccessible or changed destinations fail review.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #52 — [CTAN decision] xurl: Break long URLs naturally

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/52)

Proposed: **D1-B**. Keep xurl in the paper, and use descriptive hyperlinks in the deck/index so raw long URLs need not be shown.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Render the longest actual artifact URL and check line breaks/copyability; normal slides should still prefer descriptive hyperlinks.
- [ ] AC3 — Given the generated PDF, when each relevant hyperlink/reference is activated, then it reaches the intended artifact/target with a meaningful label; inaccessible or changed destinations fail review.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #55 — [CTAN decision] fontspec: Explicit OpenType font selection

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/55)

Proposed: **D1-B**. Retain T1/newpxtext/newpxmath and the TeX-bundled monospace family. Avoid stacking fontspec or changing the established font contract.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Resolve the selected fonts in clean CI, preserve licensing and glyph coverage, and remove conflicting legacy text-font setup only as a deliberate later change.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #56 — [CTAN decision] microtype: Protrusion and fine typographic adjustment

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/56)

Proposed: **D1-A**. Retain microtype for supported XeTeX protrusion. No claim of XeTeX font expansion or compensation for overcrowding.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Use only supported XeTeX features; specifically do not claim font expansion. Compare render/logs for substitution warnings.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #57 — [Evidence decision] Public demo template recordings

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/57)

Proposed: **C**. Link only the recording pattern; playback is not inspected here and no autonomous-agent or pixel-diff claim is made.

Evidence boundary (issue audit): Two synthetic counter recordings; playback not inspected; not pixel-diff testing or autonomous-agent capability

[Public demo template evidence](https://newdarwindev.github.io/public-demo-template/evidence/)

- [ ] A — Core deck
- [ ] B — Separate supplement
- [ ] C — Link only with limits
- [ ] D — Defer pending evidence

Original acceptance requirements (not certified passed):

- [ ] Inspect selected playback before making interaction claims. Retain two synthetic counter recordings and deployed99e0355 identity; no pixel-diff or autonomous-agent capability claim.
- [ ] Confirm chosen links still resolve to the reviewed content, record exact revision/cutoff and show the limitation adjacent to the artifact.
- [ ] Render the affected slide(s) at presentation size, verify legibility and link targets, and preserve the 10-frame/10-page contract unless a separate change is approved.
- [ ] Record the selected option and rationale without inventing personal role, employment, customer adoption, production deployment, ROI or measured time savings.

## #58 — [CTAN decision] xcolor: Shared semantic palette

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/58)

Proposed: **D1-A**. Use native/human/harness/stopped labels and distinct curve styles as redundant cues; keep the established palette.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Check grayscale and contrast plus text/line-style redundancy. Stop/unknown/verified statuses remain understandable without color.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #59 — [CTAN decision] graphicx: Include/crop PDF and raster graphics

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/59)

Proposed: **D1-A**. Use a genuine pinned refinery screenshot and sampled walkthrough still with aspect ratio preserved, capture/provenance dates and synthetic/demo limitations.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Use a genuine, dated evidence image or vector figure; preserve aspect ratio, capture provenance and synthetic/proposed label. Do not replace paragraphs with raster text.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #60 — [CTAN decision] pdfpages: Select and include pages from other PDFs

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/60)

Proposed: **D1-C**. Defer PDF import: the independent HTML evidence supplement supplies links without appending pages to the ten-frame deck.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Keep the ten-page deck unchanged; any review packet is a distinct optional output. Verify retained links/annotations rather than assuming imported pages preserve them.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #61 — [CTAN decision] tagpdf: PDF tagging infrastructure

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/61)

Proposed: **D1-C**. Defer implementation to a separate pdfLaTeX/LuaLaTeX compatibility study. Keep XeLaTeX; make no PDF/UA claim. Reopen on an engine-migration decision and assistive-technology test plan.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Treat as a separate compatibility/migration investigation: current CTAN guidance targets pdfLaTeX/LuaLaTeX, not current XeLaTeX. No engine change or compliance claim is selected by this issue.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.

## #62 — [CTAN decision] accsupp: Low-level replacement text and abbreviation expansion

[Original issue](https://github.com/newdarwindev/dots-authorized-agent-workflows-paper/issues/62)

Proposed: **D1-C**. Defer until extraction demonstrates a specific missing text equivalent. Provide visible descriptions now; driver-specific replacement text is not whole-document accessibility.

- [ ] D1-A — Refine existing usage / evaluate proposed treatment
- [ ] D1-B — Keep current approach / existing alternative
- [ ] D1-C — Defer until the stated requirement exists

Original acceptance requirements (not certified passed):

- [ ] AC1 — Record the selected option, rationale, inspected source/package version and any remaining uncertainty.
- [ ] AC2 — Test driver-specific text equivalents and extraction in an isolated proof before adoption. Do not imply experimental replacement text tags establish whole-document accessibility.
- [ ] AC3 — Given the produced PDF, when rendered and text-extracted, then headings/body/links remain legible, semantic status is not color-only, and diagrams have a readable textual explanation; appearance alone does not prove accessibility compliance.
- [ ] AC4 — Render all ten slides, inspect layout at reading size, verify extractable text and the relevant PDF links, and retain the exact 10-page/10-frame XeLaTeX contract.
- [ ] AC5 — Keep proposal / synthetic prototype / recorded test / production distinctions explicit. No customer adoption, ROI, career, measured improvement or production claim may be inferred from package adoption or demo metrics.
