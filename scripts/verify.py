#!/usr/bin/env python3
"""Verify page counts, evidence provenance, PDF links and issue coverage."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--pdf-dir", type=Path, default=ROOT / "build")
args = p.parse_args()
data = json.loads((ROOT / "review/decisions.json").read_text())
numbers = [row["number"] for row in data["issues"]]
assert len(numbers) == len(set(numbers)) == 55
assert set(numbers) == set(range(1, 63)) - {18, 45, 47, 49, 51, 53, 54}
assert set(data["excluded"]) == {45, 47, 49, 51, 53, 54}
assert (ROOT / "deck.tex").read_text().count(r"\begin{frame}") == 10
assert r"\insertframenumber/\inserttotalframenumber" in (ROOT / "deck.tex").read_text()
for filename, expected in (("paper.pdf", 20), ("deck.pdf", 10),
                           ("deck-evidence.pdf", 10), ("deck-fleet.pdf", 10)):
    reader = PdfReader(args.pdf_dir / filename)
    assert len(reader.pages) == expected, (filename, len(reader.pages))
    text = "\n".join(page.extract_text() for page in reader.pages)
    assert all(len(page.extract_text().strip()) > 40 for page in reader.pages)
    assert "??" not in text, (filename, "unresolved citation")
    links = []
    for page in reader.pages:
        for ref in page.get("/Annots", []):
            ann = ref.get_object()
            rect = ann.get("/Rect")
            if rect:
                assert -1 <= float(rect[0]) <= float(rect[2]) <= float(page.mediabox.width) + 1
                assert -1 <= float(rect[1]) <= float(rect[3]) <= float(page.mediabox.height) + 1, (filename, rect)
            action = ann.get("/A", {})
            if "/URI" in action:
                uri = action["/URI"]
                assert urlparse(uri).scheme == "https", uri
                links.append(uri)
    if filename.startswith("deck"):
        assert "10/10" in reader.pages[-1].extract_text()
        assert any("/paper.pdf" in link for link in links)
        assert any("ecd6c3e" in link for link in links)
        assert any("arxiv.org" in link for link in links), "Missing methodological source links"
        outlines = [entry["/Title"] for entry in reader.outline if isinstance(entry, dict)]
        assert {"Problem", "Mechanism", "Evidence", "Limits"} <= set(outlines), outlines
        logfile = args.pdf_dir / filename.replace(".pdf", ".log")
        if logfile.exists():
            assert not re.search(r"Overfull \\[hv]box", logfile.read_text()), filename
    print(f"{filename}: {expected} pages, extractable text, {len(links)} HTTPS links")
literal = "await expect(page.getByRole('button',{name:'Continue to evaluation'})).toBeDisabled();"
assert literal in (ROOT / "review/sources/refinery-flow.spec.js").read_text()
assert literal in (ROOT / "slides/evidence-experiment.tex").read_text()
for asset in json.loads((ROOT / "assets/provenance.json").read_text()):
    assert hashlib.sha256((ROOT / asset["path"]).read_bytes()).hexdigest() == asset["sha256"]
    assert "ecd6c3eda92d442b983d5c6d1d40435442f8a49a" in asset["source"]
assert "- [x]" not in (ROOT / "review/decisions.md").read_text().lower()


class Gallery(HTMLParser):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert "checked" not in attrs, "Choices must start unselected"
        for key in ("href", "src"):
            target = attrs.get(key, "")
            if target and not target.startswith(("https://", "#")):
                assert (ROOT / "docs/review" / target).exists(), target


Gallery().feed((ROOT / "docs/review/index.html").read_text())
for task in json.loads((ROOT / "review/fleet-fixture.json").read_text())["tasks"]:
    assert hashlib.sha256(task["expected_text"].encode()).hexdigest() == task["expected_sha256"]
print("55 issue dispositions; six wontfix exclusions; literal source and asset hashes verified")
