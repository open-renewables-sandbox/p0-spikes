"""Compare V-12 digests and summarise V-13 steps across downloaded artifacts. Usage: compare_results.py <dir>"""
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
runs = {}
for d in sorted(root.iterdir()):
    if d.is_dir() and (d / "r12.json").exists():
        runs[d.name] = (json.loads((d / "r12.json").read_text(encoding="utf-8")),
                        (d / "r13.txt").read_text(encoding="utf-8") if (d / "r13.txt").exists() else "")
print("## V-12 environment")
for k, (j, _) in runs.items():
    print(f"- {k}: python {j['python']} {j['system']}/{j['machine']}, tarfile default {j['tarfile_default_format']}, "
          f"zlib {j['zlib_compile']} / runtime {j['zlib_runtime']}, entries {j['entries']}")
print("\n## V-12 digests: distinct values per variant (1 means equal on every run)")
for section in ("tar_sha256", "targz_sha256"):
    variants = sorted({v for j, _ in runs.values() for v in j[section]})
    for v in variants:
        vals = {}
        for k, (j, _) in runs.items():
            vals.setdefault(j[section].get(v, "missing")[:12], []).append(k)
        print(f"- {section} {v}: {len(vals)} distinct")
        if len(vals) > 1:
            for dig, ks in vals.items():
                print(f"    {dig}: {', '.join(ks)}")
print("\n## V-13 step exit codes")
for k, (_, t) in runs.items():
    steps = [l for l in t.splitlines() if "|" in l and not l.startswith("---")]
    print(f"- {k}: " + ", ".join(steps))
