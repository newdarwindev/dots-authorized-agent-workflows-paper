#!/usr/bin/env python3
"""Generate review documents from public, reviewed issue metadata."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def choices(row):
    if row["category"] == "package":
        return [("D1-A", "Refine existing usage / evaluate proposed treatment"),
                ("D1-B", "Keep current approach / existing alternative"),
                ("D1-C", "Defer until the stated requirement exists")]
    if row["category"] == "planning":
        return [("D1-A", "Matched native versus authorized fleet comparison"),
                ("D1-B", "Within-fleet placement/recovery ablation"),
                ("D2-A", "Full predefined metrics"), ("D2-B", "Feasibility study"),
                ("D3-A", "Editable TeX diagram"), ("D3-B", "Versioned static vector")]
    return [("A", "Core deck"), ("B", "Separate supplement"),
            ("C", "Link only with limits"), ("D", "Defer pending evidence")]


def generate():
    data = json.loads((ROOT / "review/decisions.json").read_text())
    md = ["# Open-issue review", "",
          "Snapshot: 2026-11-01. 55 decisions; six wontfix issues excluded. "
          "Proposals are reviewable dispositions, not selected preferences. "
          "Choose one option per issue (one per D1/D2/D3 for #1) in the PR. "
          "Multiple choices in a group conflict; reconcile before merging.", "",
          "Three full ten-page options: deck.tex (argument, proposed default), "
          "deck-evidence.tex (synthetic evidence), deck-fleet.tex (proposed fleet). "
          "Only slides 5 and 7 vary; all preserve thesis, boundaries and economics.", "",
          "Excluded without changes: " + ", ".join(f"#{n}" for n in data["excluded"]) + ".", "",
          "Package/build evidence is in validation.txt and the retained CI TeX logs. "
          "Deferred packages are not added. HTTP reachability is not runtime/CI verification.", ""]
    sections = []
    e = html.escape
    for row in data["issues"]:
        title = f'#{row["number"]} — {row["title"]}'
        md += [f'## {title}', "", f'[Original issue]({row["url"]})', "",
               f'Proposed: **{row["proposed"]}**. {row["rationale"]}', ""]
        if row["boundary"]:
            md += [f'Evidence boundary (issue audit): {row["boundary"]}', ""]
        links = " · ".join(f'[{s["title"]}]({s["url"]})' for s in row["sources"])
        if links:
            md += [links, ""]
        md += [f'- [ ] {key} — {label}' for key, label in choices(row)]
        md += ["", "Original acceptance requirements (not certified passed):", "",
               row["verification"], ""]
        link_html = " · ".join(f'<a href="{e(s["url"], quote=True)}">{e(s["title"])}</a>' for s in row["sources"])
        controls = "".join(
            f'<label><input type="radio" name="issue-{row["number"]}-{key[:2] if row["category"] == "planning" else "choice"}" value="{key}"> {key} — {e(label)}</label>'
            for key, label in choices(row))
        sections.append(f'<section id="issue-{row["number"]}"><h2><a href="{e(row["url"])}">{e(title)}</a></h2>'
                        f'<p><strong>Proposed: {e(row["proposed"])}</strong>. {e(row["rationale"])}</p>'
                        f'<p>{e(row["boundary"])}</p><p>{link_html}</p>'
                        f'<fieldset><legend>Preview a preference; record it in the PR</legend>{controls}</fieldset></section>')
    (ROOT / "review/decisions.md").write_text("\n".join(md).rstrip() + "\n")
    page = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aftermarket deck — issue review</title><style>
body{margin:auto;max-width:1100px;padding:32px;font:17px/1.55 system-ui;color:#172638}
a{color:#2563a6}h1{font:700 44px Georgia}h2{font-size:23px}section{border-top:1px solid #d8e0e7;padding:24px 0}
img{width:100%;height:auto}fieldset{border:1px solid #d8e0e7}label{display:block;margin:10px 0}
a:focus-visible,input:focus-visible{outline:3px solid #007f7a;outline-offset:3px}
</style><main><h1>Three ways to present the same thesis</h1>
<p>55 open decisions, excluding six wontfix items. Preferences start unselected.
Use the PR checkboxes to save your choices; this local form is a preview.</p>
<p>Each variant contains ten slides; slides 5 and 7 differ. The paper retains twenty pages.
Source-only architecture and dated evidence references form a separate supplement.</p>
<nav><a href="#argument">Argument</a> · <a href="#evidence">Synthetic evidence</a> · <a href="#fleet">Proposed fleet</a></nav>"""
    for variant in ("argument", "evidence", "fleet"):
        page += f'<section id="{variant}"><h2>{variant.title()}</h2><a href="{variant}.pdf">Open ten-page PDF</a><img src="{variant}.png" alt="All ten slides in the {variant} option"></section>'
    page += "<h2>Per-issue decisions and evidence supplement</h2>" + "".join(sections) + "</main></html>\n"
    dest = ROOT / "docs/review"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(page)


if __name__ == "__main__":
    generate()
