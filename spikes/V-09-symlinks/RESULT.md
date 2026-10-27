# V-09 Skill symlinks: result (partial)

Date: 2026-10-27. Labels: **[Test]** observed. Probes: `.agents/skills/{demo,copydemo,junctiondemo}`, `.claude/skills/demo` (a **git symlink**, mode `120000`, target `../../.agents/skills/demo`), `.claude/skills/copydemo/` (a plain copy) and a local-only NTFS junction `.claude/skills/junctiondemo`. Workflow run [40452563615](https://github.com/open-renewables-sandbox/p0-spikes/actions/runs/40452563615) on tag `v0.0.2-p0`; a fresh Claude Code session on this Windows machine.

## Outcome

**Git, GitHub archives and Linux, macOS and hosted Windows checkouts keep the symlink; this machine's default Windows checkout does not, and Claude Code then does not find the skill.** AD-16 holds where symlinks can exist. A true symlink was **not** tested against Claude Code, because this machine cannot create one (Developer Mode off, no administrator rights, no WSL); a junction stood in.

| Route | Result **[Test]** |
| --- | --- |
| git index | mode `120000` stored (written with plumbing, since this machine cannot create symlinks) |
| Checkout on ubuntu-latest, macos-latest | real symlink; skill file reachable through it |
| Checkout on windows-latest | `core.symlinks=true` on the hosted runner; real symlink; reachable |
| Checkout on this machine (Git for Windows default, `core.symlinks` false) | **plain 25-byte file** containing `../../.agents/skills/demo` |
| GitHub source archive `.tar.gz` for the tag | entry kept as a symlink (`linkname ../../.agents/skills/demo`) |
| GitHub source archive `.zip` | entry kept as a symlink (unix mode `0o120777`) |
| Claude Code, fresh session, skill behind a **plain-file stub** (this machine's checkout) | **not listed** |
| Claude Code, skill behind a **plain copy** | listed and invoked (`V09-PROBE-copydemo-OK`) |
| Claude Code, skill behind an NTFS **junction** (directory link, proxy for a symlink) | listed and invoked (`V09-PROBE-junctiondemo-OK`) |

## What it means

- Discovery works through a directory link (junction) and a copy, and fails through the text stub that a symlink-less Windows checkout produces. Anyone who clones the template on Windows without symlink rights gets no `author-concept` or `use-bundle` skill in Claude Code.
- GitHub's own archives preserve symlinks, so the "download a release archive" route is not the weak point; extracting a zip on Windows is untested.
- I-12's archive includes `.agents/skills/use-bundle/` only, so the `.claude/skills/` entries are not in it; this result concerns the template's own source archive and clones.

## Not tested

A real symlink against Claude Code (needs Windows Developer Mode, or Linux or macOS with Claude Code; the owner's call); "Use this template" (needs a further sandbox repository, not allowed by the D-1 default); extracting the zip on Windows; Claude Code on Linux or macOS.

## Feeds

Proposed entry **P-8 is triggered in part**: on a Windows machine without symlink rights AD-16's `.claude/skills/<name>` entries do not work. The fallback already named in SDD §15 (`init_library.py` copies the skills) would be needed for such libraries, or a documented prerequisite (Developer Mode, `core.symlinks=true`). The owner decides.
