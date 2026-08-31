#!/usr/bin/env python3
"""
make_matrix.py -- build the requirements x tests matrix from a Sphinx-Needs
needs.json export (the bidirectional matrix that Sphinx-Needs itself does not
render natively; it gives a table via needtable and a graph via needflow).

Generate the JSON by building the docs with needs_build_json = True (it lands
at _build/html/needs.json), then:

    python make_matrix.py --json _build/html/needs.json --out _build/html/matrix.html

By default it treats need type 'spec' as the rows and 'test' as the columns;
override with --spec-type / --test-type if you defined custom types.

It builds the matrix from the FORWARD direction (each test's forward link field
listing the specs it verifies), so it does not depend on the *_back fields being
populated. The forward field defaults to `tests` (the custom link type, correct
for copy=False); pass --link-field links if your link type uses copy=True.
Gaps fall out visually: an uncovered requirement is a row with no marks
(highlighted), and an orphan test is a column with no marks (header in red).
"""

import argparse
import html
import json
import sys


def load_needs(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    versions = data.get("versions", {})
    if not versions:
        sys.exit("ERROR: no 'versions' key in needs.json -- is this a Sphinx-Needs export?")
    version = data.get("current_version") or sorted(versions)[-1]
    needs = versions[version].get("needs", {})
    if not needs:
        sys.exit(f"ERROR: no needs found under version '{version}'.")
    return needs


def build_matrix(needs, spec_type, test_type, link_field):
    specs = sorted(nid for nid, n in needs.items() if n.get("type") == spec_type)
    tests = sorted(nid for nid, n in needs.items() if n.get("type") == test_type)
    if not specs:
        sys.exit(f"ERROR: no needs of type '{spec_type}'. Types present: "
                 f"{sorted({n.get('type') for n in needs.values()})}")
    spec_set = set(specs)

    cell = set()          # (spec_id, test_id) when that test verifies that spec
    orphan_tests = []
    for tid in tests:
        links = needs[tid].get(link_field, []) or []
        matched = [l for l in links if l in spec_set]
        if not matched:
            orphan_tests.append(tid)
        for r in matched:
            cell.add((r, tid))

    covered = {r for (r, _t) in cell}
    uncovered = [r for r in specs if r not in covered]
    return specs, tests, cell, uncovered, orphan_tests


def render_html(needs, specs, tests, cell, uncovered, orphan_tests):
    orphan_set, uncovered_set = set(orphan_tests), set(uncovered)
    n_spec = len(specs)
    n_cov = n_spec - len(uncovered)
    pct = (100.0 * n_cov / n_spec) if n_spec else 0.0

    def title(nid):
        return needs.get(nid, {}).get("title", "")

    head = "".join(
        f'<th class="rot {"orphan" if t in orphan_set else ""}" title="{html.escape(title(t))}">'
        f'<div><span>{html.escape(t)}</span></div></th>'
        for t in tests
    )
    rows = []
    for r in specs:
        cells = "".join(
            '<td class="mark">&#10003;</td>' if (r, t) in cell else "<td></td>"
            for t in tests
        )
        cls = ' class="uncovered"' if r in uncovered_set else ""
        rows.append(
            f'<tr{cls}><th class="rowhead" title="{html.escape(title(r))}">'
            f'{html.escape(r)}</th>{cells}</tr>'
        )
    body = "\n".join(rows)
    unc = ", ".join(html.escape(u) for u in uncovered) or "none"
    orph = ", ".join(html.escape(o) for o in orphan_tests) or "none"

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Traceability matrix</title>
<style>
 body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 2rem; color:#1a1a1a; }}
 h1 {{ font-size: 1.4rem; }}
 .summary {{ margin:1rem 0; padding:.75rem 1rem; background:#f4f6f8; border-radius:8px; }}
 .summary b {{ font-variant-numeric: tabular-nums; }}
 table {{ border-collapse: collapse; }}
 th, td {{ border: 1px solid #d0d5dd; }}
 td {{ width: 2.2rem; height: 2.2rem; text-align:center; }}
 td.mark {{ color:#0a7f2e; font-weight:700; }}
 th.rowhead {{ text-align:left; padding:.25rem .6rem; position:sticky; left:0; background:#fff; white-space:nowrap; }}
 tr.uncovered th.rowhead {{ background:#fde8e8; }}
 tr.uncovered td {{ background:#fff6f6; }}
 th.rot {{ vertical-align:bottom; padding:0; }}
 th.rot > div {{ position:relative; width:2.2rem; height:9rem; }}
 th.rot span {{ position:absolute; bottom:0.4rem; left:50%; transform-origin:left bottom; transform:rotate(-90deg); white-space:nowrap; font-size:.8rem; font-weight:600; line-height:1; }}
 th.rot.orphan span {{ color:#b42318; }}
 .legend {{ margin-top:1rem; font-size:.9rem; color:#475467; }}
</style></head><body>
<h1>Traceability matrix &mdash; requirements &times; tests</h1>
<div class="summary">
 Requirements: <b>{n_spec}</b> | Covered: <b>{n_cov}</b> (<b>{pct:.0f}%</b>)
 | Uncovered: <b>{len(uncovered)}</b> | Tests: <b>{len(tests)}</b>
 | Orphaned tests: <b>{len(orphan_tests)}</b>
</div>
<table><thead><tr><th></th>{head}</tr></thead>
<tbody>
{body}
</tbody></table>
<p class="legend"><b>Uncovered requirements:</b> {unc}<br>
<b>Orphaned tests:</b> {orph}</p>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Build requirements x tests matrix from needs.json")
    ap.add_argument("--json", default="_build/html/needs.json", help="path to needs.json")
    ap.add_argument("--out", default="_build/html/matrix.html", help="output HTML path")
    ap.add_argument("--spec-type", default="spec", help="need type for rows (default: spec)")
    ap.add_argument("--test-type", default="test", help="need type for columns (default: test)")
    ap.add_argument("--link-field", default="tests",
                    help="need field holding the test->spec link (default: tests, "
                         "for copy=False; use 'links' if your link type has copy=True)")
    args = ap.parse_args()

    needs = load_needs(args.json)
    specs, tests, cell, uncovered, orphan_tests = build_matrix(
        needs, args.spec_type, args.test_type, args.link_field)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(render_html(needs, specs, tests, cell, uncovered, orphan_tests))

    print(f"wrote {args.out}  ({len(specs)} requirements x {len(tests)} tests)")
    if uncovered:
        print(f"  uncovered requirements: {', '.join(uncovered)}")
    if orphan_tests:
        print(f"  orphan tests: {', '.join(orphan_tests)}")


if __name__ == "__main__":
    main()
