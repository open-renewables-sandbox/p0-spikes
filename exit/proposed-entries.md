# Proposed decision entries (P0 exit draft, 2026-10-28)

Status: **all Proposed; nothing is written to `adr/`, the DDR, the SDD, the SRS or `constraints.md`.** P-1 (generator) is in `generator-recommendation.md`; the SDD §1, §14 and §15 edits are in `sdd-s1-s14-s15.diff`; the re-estimate is in `re-estimate.md`. IDs: the next ADR number is ADR-001, taken by P-1; the numbers below are assigned on approval. The frozen QA-/DR- series is not extended (QA-68).

## Summary

| # | Subject | Triggered by | Form | Needs owner? | Blocks |
| --- | --- | --- | --- | --- | --- |
| P-1 | Site generator | V-03, V-04 | ADR-001 | Approve text | P3 |
| P-2 | Re-estimate | P0 exit | SDD edit + change-log row | Approve | — |
| P-5 | W-05 commit-to-PR lookup can lag | V-05 | SDD edit (W-05, C-03 `platforms`) | Approve | P2 |
| P-8 | Skills on Windows without symlinks | V-09 | ADR amending AD-16 | **Decide** | P2 `init_library.py` |
| P-9 | `CLAUDE.md` import form | V-10 | ADR + `CLAUDE.md` edit | Approve | P1 start |
| P-10 | `ci:` to `process:` in the `verified` mapping | V-11 | SDD edit (I-08) | Optional | P2 |
| P-11 | Archive checksum across zlib implementations | V-12 | ADR amending QA-61, I-12 | **Decide** | P2 `release.py` |
| P-14 | Outcomes recorded in the DDR | P0 exit | Change-log rows + SDD §15 diff | Approve | — |
| P-15 | Link rule: root-relative links | V-10, V-03 | ADR amending I-01; **requirement-level request** | **Decide** | P1 link check |
| P-16 | Carried verification items and gates | P0 exit | SDD §14 edit (in the diff) | Approve | — |
| P-17 | MPL-2.0 licence exceptions | V-03 | ADR + `constraints.md` | Approve | P1 or P3 |
| P-18 | `.gitattributes` in the layout | V-13 | SDD §6 edit | Approve | P1 |

Not triggered: P-3 (AD-14 holds), P-4 (four-space rule holds), P-6 (immutable releases work on Free, public), P-7 (validator vendors and runs), P-12 (poe and hooks pass), P-13 (V-06 not measured in P0).

## P-2 Re-estimate

`re-estimate.md`: remaining P1 to P4 effort 31–46 person-days, programme 33.5–49.5, inside QA-45's 35–55. Form: edit SDD §1 and §14 (in the diff) and a DDR change-log row citing QA-45.

## P-5 Commit-to-pull-request lookup lags the push

**Context.** W-05 says "per commit: pull request". V-05: `GET /commits/{sha}/pulls` returned `[]` right after a merge and `[1]` about 20 seconds later; `pulls?state=closed&base=…` returned the merge commit at once; the squash message ends `(#n)`.
**Proposal.** W-05 and C-03 `platforms`: the GitHub adapter resolves a commit's pull request by the closed-pull-request list (match `merge_commit_sha`), falls back to `(#n)` in the subject, retries the commit endpoint with a short delay, and records `PR none` only after all three fail. No change to AD-11 or AD-12.

## P-8 Skills where symlinks are unavailable (amends AD-16)

**Context.** V-09: `.claude/skills/<name>` as a git symlink survives git, GitHub archives and Linux, macOS and hosted Windows checkouts, but on a Windows checkout with `core.symlinks=false` it becomes a text stub and Claude Code does not list the skill; a plain copy and a directory junction work.
**Options.** (a) `init_library.py` writes copies into `.claude/skills/` when symlinks are unavailable (the fallback SDD §15 names); (b) document Developer Mode and `core.symlinks=true` as a prerequisite; (c) always copy, and have a task re-sync them. **Recommendation:** (a), with a W-10 case for it, and (b) stated in the README. **Consequence:** P2 `init_library.py` gains a copy path; the template keeps the symlinks.

## P-9 `CLAUDE.md` import form

**Context.** V-10: the four `@docs/development/…` imports with spaces do not load; only the backslash-escaped form loads (also with hyphens, nested folders and nested imports). QA-36 and QA-67 keep the exact file names.
**Decision proposed.** Keep the file names; write the imports as `@docs/development/requirements/OKF\ Library\ Template\ -\ Software\ Requirements\ Spec.md` and so on; update the comment in `CLAUDE.md` that anticipates V-10. Amends the wording of QA-36 (links `%20` or angle brackets remain valid for Markdown links; imports use backslashes). The edit to the template's `CLAUDE.md` is made after approval, in a docs-only pull request.

## P-10 `process:` in the `verified` mapping (optional)

**Context.** V-11: OKF §5.3 derives the tier from any `human:` entry; §7 names `process:<id>` for automated processes; `ci:<bot>` works but is not the convention. **Proposal.** I-08: `{by: process:<bot>, at: …}` instead of `ci:<bot>`. Tier results are unchanged. Rule kept: no `human:` entry for a Machine-confirmed concept.

## P-11 Archive checksum across zlib implementations (amends QA-61, I-12)

**Context.** V-12: the tar is byte-identical on all eight runs; the `.tar.gz` differs when Python is linked to zlib-ng (3.14 on Windows) rather than zlib; only gzip level 0 matched across the two on the test input.
**Options.** (1) Record the SHA-256 of the **uncompressed tar** as the canonical content hash, beside the `.tar.gz` digest, and verify citations against the tar; (2) gzip level 0 everywhere (about ten times the size on the 30 KB test input); (3) build archives with one pinned interpreter build and record it in the manifest; (4) a compressor with specified output.
**Recommendation:** (1) plus (3): the manifest records both digests and the Python and zlib versions used; W-12 step 5 compares the tar digest, and the `.tar.gz` digest only when the recorded versions match. FR6.6 and FR7.3 acceptance wording ("matches its recorded checksum") is a requirement-level reading that the owner should confirm.

## P-14 Outcomes recorded in the DDR

DDR change-log rows (one per item or one row for all) pointing to the SDD §15 outcome column and the p0-spikes results, as SDD §14's gate asks ("outcomes recorded in the DDR"). No new QA or DR number (QA-68). The §15 column is in the diff.

## P-15 Link rule: root-relative links (amends I-01) — requirement-level request

**Context.** I-01 allows bundle-root-relative (`/path/to/concept.md#anchor`) and relative links. V-10: on GitHub a `/` link resolves from the **repository root**, so in a template whose bundle is `knowledge/` it points at a path that does not exist (the 404 is inferred from the path). V-03: Zensical 0.0.73 leaves `/` links unresolved (FR8.2 check 2 fails). MkDocs resolves them. Relative links resolve on GitHub, MkDocs, Zensical and Docusaurus; `%20` or angle-bracket forms handle spaces.
**Proposal.** I-01 and W-04 check 4: internal links are **relative** only (with the `%20` or angle-bracket form for spaces); the validator rejects root-relative links; `new_concept.py` and the skills emit relative links. This also removes the Zensical check-2 blocker and is a precondition of the switch in ADR-001.
**Owner request, not an edit:** FR2.10 ("a link … resolves on the hosting platform and on the site") and FR8.2 check 2 ("links starting with `/` resolve to site routes") are written around root-relative links. Under this proposal check 2 would read "relative links resolve to site routes", and root-relative links would not be permitted. Only the owner changes a requirement.

## P-16 Carried verification items and gates

In the diff (SDD §14): V-05 5a and 5c before `revision.yml` (start of P2); V-06 platform steps at the end of P2 and in full in P4; V-07 Cloudflare and private-repository releases only if a library needs them; V-09 real symlink and "Use this template" at the start of P3, with the copy-fallback decision before P2. The v1.0.0 gate still requires V-01 to V-13 closed.

## P-17 MPL-2.0 licence exceptions

**Context.** `constraints.md` allows MPL-2.0 only by recorded exception. V-03: `pathspec` 1.1.1 (both site stacks) and `certifi` (MkDocs stack) are MPL-2.0. Other metadata gaps: `python-dateutil` reports "Dual License" and `mergedeep` reports none.
**Proposal.** An ADR recording exceptions for `pathspec` and `certifi` with reason ("site dependency, unmodified, not linked into the validation set"), review-by dates, and a note that the licence check must read SPDX or classifier metadata and treat the two gaps explicitly. Edits the exception table in `constraints.md` (which needs the ADR).

## P-18 `.gitattributes` in the layout

V-13: a Windows checkout with `core.autocrlf=true` produced mixed line endings and a `ruff format --check` failure; V-12's archive build avoids the working tree, but the template needs `* text=auto eol=lf` for the tooling to behave the same on every system. **Proposal.** Add `.gitattributes` to SDD §6 and the P1 deliverables.
