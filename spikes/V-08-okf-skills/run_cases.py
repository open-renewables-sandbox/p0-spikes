"""Run the pinned okf_validate.py on one broken variant of the fixture per case.
Usage: python run_cases.py <python-with-pyyaml> <okf_validate.py> <fixture knowledge dir> <scratch dir>"""
import json, shutil, subprocess, sys, pathlib
py, val, fx, scratch = sys.argv[1:5]
fx, scratch = pathlib.Path(fx), pathlib.Path(scratch)
ITEM = "example-group/example-category/example-item.md"
def sub(old, new):
    return lambda t: t.replace(old, new, 1)
cases = {
 "baseline": lambda t: t,
 "blank-line-before-frontmatter": lambda t: "\n" + t,
 "invalid-yaml": sub("title: Example item", "title: [unclosed"),
 "frontmatter-not-mapping": lambda t: "---\n- a\n- b\n---\n# x\n",
 "missing-type": sub("type: Item\n", ""),
 "empty-type": sub("type: Item", "type:"),
 "missing-title": sub("title: Example item\n", ""),
 "stale-after-no-offset": sub("stale_after: 2027-01-01T00:00:00Z", "stale_after: 2027-01-01T00:00:00"),
 "stale-after-date-only": sub("stale_after: 2027-01-01T00:00:00Z", "stale_after: 2027-01-01"),
 "stale-after-garbage": sub("stale_after: 2027-01-01T00:00:00Z", "stale_after: next week"),
 "unknown-status": sub("status: draft", "status: published"),
 "verified-human-ok": sub("status: draft", "status: draft\nverified:\n  - by: human:alice\n    at: 2026-10-20T10:00:00Z"),
 "verified-process-ok": sub("status: draft", "status: draft\nverified:\n  by: process:ci-bot\n  at: 2026-10-20T10:00:00Z"),
 "verified-near-miss": sub("status: draft", "status: draft\nverified:\n  - by: Human:alice\n    at: 2026-10-20T10:00:00Z"),
 "verified-ci-prefix": sub("status: draft", "status: draft\nverified:\n  - by: ci:bot\n    at: 2026-10-20T10:00:00Z"),
 "verified-bad-instant": sub("status: draft", "status: draft\nverified:\n  - by: human:alice\n    at: yesterday"),
 "generated-ok": sub("status: draft", "status: draft\ngenerated:\n  by: process:agent\n  at: 2026-10-20T10:00:00+00:00"),
 "footnote-no-sources": lambda t: t,  # fixture item already has [^1] and no sources
 "sources-ok": sub("status: draft", "status: draft\nsources:\n  - id: '1'\n    resource: https://example.org/x"),
 "broken-crosslink": lambda t: t + "\n[x](missing.md)\n",
}
rows = []
for name, fn in cases.items():
    d = scratch / name; shutil.rmtree(d, ignore_errors=True); shutil.copytree(fx, d)
    p = d / ITEM; p.write_text(fn(p.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    r = subprocess.run([py, "-I", val, str(d), "--json"], capture_output=True, text=True, encoding="utf-8")
    j = json.loads(r.stdout)
    base_w = {w for w in json.load(open(scratch / "_base.json"))["warnings"]} if name != "baseline" else set()
    new_w = [w for w in j["warnings"] if w not in base_w]
    rows.append((name, r.returncode, j["errors"], new_w))
    if name == "baseline": json.dump(j, open(scratch / "_base.json", "w"))
for name, rc, errs, ws in rows:
    print(f"## {name}  exit={rc}")
    for e in errs: print("   ERROR", e)
    for w in ws: print("   warn ", w)
