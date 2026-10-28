"""Build the proposed SDD section 1, 14 and 15 edits against the committed SDD and write a unified diff. Applies nothing."""
import re, subprocess, pathlib, sys
here = pathlib.Path(__file__).parent
base = (here / "SDD-base.md").read_text(encoding="utf-8")
new = base

def sub1(old, repl):
    global new
    assert new.count(old) == 1, ("expected one match", old[:70], new.count(old))
    new = new.replace(old, repl)

# --- section 1
sub1("Effort was estimated at 27–41 person-days for one maintainer; the review of 25 October 2026 estimated 35–55, and effort is re-estimated at the end of P0.",
     "Effort was estimated at 27–41 person-days for one maintainer; the review of 25 October 2026 estimated 35–55; at the end of P0 (2026-10-28) the remaining effort for P1 to P4 is re-estimated at 31–46 person-days (section 14).")
sub1("Thirteen behaviours are not yet verified and are scheduled as spikes before build (section 15).",
     "Thirteen behaviours were scheduled as spikes before build (section 15); nine are answered, three (V-05, V-07, V-09) are partly answered and V-06 is carried, each carried part to a named gate (section 14).")

# --- section 14 intro and rows
sub1("the review of 25 October 2026 estimated 35–55, mainly for P1 and P2, and effort is re-estimated at the P0 exit (DDR QA-45).",
     "the review of 25 October 2026 estimated 35–55, mainly for P1 and P2, and effort was re-estimated at the P0 exit on 2026-10-28 (DDR QA-45): the table below carries the revised figures for P1 to P3, 31–46 person-days for P1 to P4 in total **[Inf]**. The basis is in the P0 re-estimate; the largest uncertainty is P1, which no spike exercised.")
sub1("| 2–3 | Each V-item answered; generator decided; design and estimate updated |",
     "| 2–3 | Done 2026-10-28: each V-item answered or carried to a named gate; generator decided (ADR-001); design and estimate updated |")
sub1("| 10–15 | All finding codes tested; v0.1.0 (alpha) |", "| 11–16 | All finding codes tested; v0.1.0 (alpha) |")
sub1("| 8–12 | Each approval and tier case recorded correctly in a scratch library, including a dropped run |",
     "| 10–15 | Each approval and tier case recorded correctly in a scratch library, including a dropped run |")
sub1("| 4–6 | v0.5.0 (beta) |", "| 5–7 | v0.5.0 (beta) |")

carried = """
Verification items carried past P0 (decided 2026-10-28; each has a gate, and the v1.0.0 gate below still requires them closed):

| Item | Part carried | Gate |
| --- | --- | --- |
| V-05 | App "always" bypass on a protected `main` (5a); approval, stale approval and review `commit_id` API shape (5c) | Before `revision.yml` is written, at the start of P2 |
| V-06 | Second person times W-01: platform steps first, then the whole | End of P2 (platform steps); P4 (full, FR6.1) |
| V-07 | Cloudflare Pages access-policy limits on the free plan; immutable releases on a private repository | Only if a library wants a private preview or release; otherwise none |
| V-09 | A real symlink against Claude Code; "Use this template" keeps the symlink | Start of P3; the copy fallback decision comes before P2 |
"""
sub1("P1 starts only when the SRS is aligned with this document (DDR QA-35; done 25 October 2026).",
     "P1 starts only when the SRS is aligned with this document (DDR QA-35; done 25 October 2026)." + carried)

# --- section 15: add an outcome column
outcomes = {
 "V-01": "Confirmed 2026-10-27: AD-14 holds on GitHub; GitHub lower-cases explicit ids, so ids are lower case. **[Test]**",
 "V-02": "Confirmed: four-space nesting is identical on GitHub, Python-Markdown (MkDocs, Zensical) and Docusaurus; two-space differs. **[Test]**",
 "V-03": "Zensical 0.0.73 fails FR8.2 check 2 (`/`-rooted links); other tested features equal. Option A (AD-13) with Zensical in parallel; ADR-001 (Proposed). **[Test]**",
 "V-04": "Docusaurus 3.10.2 passes five checks and fails check 5 (`slug`, `id`); not adopted. **[Test]**",
 "V-05": "Partly confirmed: admin bypass, check naming, concurrency cancellation, fork privacy **[Doc]**; commit-to-pull-request lookup can lag the push. App bypass and approval cases carried to the start of P2. **[Test]**",
 "V-06": "Carried (section 14): platform steps end of P2, full timing in P4.",
 "V-07": "Immutable releases confirmed on Free for a public repository. Private repository and Cloudflare limits carried. **[Test]**",
 "V-08": "Confirmed: one script, the same one the Action runs; no finding codes, so mapping is by message text; offset-less datetimes pass. **[Test]**",
 "V-09": "Partly confirmed: symlinks survive git, GitHub archives and Linux, macOS and hosted Windows checkouts; a symlink-less Windows checkout breaks skill discovery. Real symlink and template flow carried to the start of P3. **[Test]**",
 "V-10": "`CLAUDE.md` imports with spaces do not load; the backslash-escaped form does (with hyphens, nested folders, nested imports). **[Test]**",
 "V-11": "Confirmed: tier from any `human:` entry; `process:` is the convention for non-human actors. **[Doc]**",
 "V-12": "Tar identical across systems and Python 3.11 and 3.14; tar.gz differs under zlib-ng. **[Test]**",
 "V-13": "Confirmed on Windows, macOS, Linux and Python 3.11 and 3.14. **[Test]**",
}
out = []
in15 = False
for line in new.split("\n"):
    if line.startswith("## 15. Verification items"): in15 = True
    elif line.startswith("## 16."): in15 = False
    if in15 and line.startswith("| ID | Item | Outcome needed |"):
        line = line.rstrip() + " Outcome (2026-10-28) |"
    elif in15 and line.startswith("| --- | --- | --- |"):
        line = line.rstrip() + " --- |"
    elif in15:
        m = re.match(r"\| (V-\d\d) \|", line)
        if m:
            line = line.rstrip() + " " + outcomes[m.group(1)] + " |"
    out.append(line)
new = "\n".join(out)
(here / "SDD-new.md").write_text(new, encoding="utf-8", newline="\n")
d = subprocess.run(["git", "diff", "--no-index", "--no-color", "--stat", "-p", str(here / "SDD-base.md"), str(here / "SDD-new.md")], capture_output=True, text=True, encoding="utf-8")
txt = d.stdout.replace(str(here).replace("\\", "/") + "/SDD-base.md", "a/docs/development/architecture/OKF Library Template - Software Design Document.md")
txt = re.sub(r"[a-zA-Z]/[^\n ]*/exit/work/SDD-base\.md", "a/docs/development/architecture/OKF Library Template - Software Design Document.md", txt)
txt = re.sub(r"[a-zA-Z]/[^\n ]*/exit/work/SDD-new\.md", "b/docs/development/architecture/OKF Library Template - Software Design Document.md", txt)
(here.parent / "sdd-s1-s14-s15.diff").write_text(txt, encoding="utf-8", newline="\n")
print(len(txt.splitlines()), "diff lines")
