# Site generator recommendation (P0 exit draft)

Date: 2026-10-28. Status: **recommendation and Proposed ADR text; nothing here is applied to the template.** Evidence: `spikes/V-03-zensical`, `spikes/V-04-docusaurus`, `spikes/V-01-anchors`, `spikes/V-10-spaces`.

## Recommendation

**Option A, confirmed by the owner on 2026-10-28:** keep MkDocs 1.6.1 with Material 9.7.x as the blocking build and build the same `mkdocs.yml` with Zensical in parallel, non-blocking. The release site is expected to move to Zensical later, by the switch criterion AD-13 already carries. This is AD-13 as written, not an amendment to it.

The route is the one Zensical's migration guide describes ("Adopt Zensical gradually": keep the MkDocs deployment, build the same project with Zensical, compare the output, switch commands when confident). The guide does not mention links, strict mode or ignored settings, and the spike found differences in exactly those areas; they are listed below.

## Basis against the SPEC criteria

| Criterion | Result at the evidence date |
| --- | --- |
| 1. Zensical eligible as blocking (all six FR8.2 checks by configuration alone, exact pin, licences on the allowlist) | **Not yet.** Zensical 0.0.73 (2026-10-26) fails check 2 and no configuration key fixes it; MPL-2.0 `pathspec` needs an exception in either stack |
| 2. Option A eligible when Zensical fails a check | Yes. Exposure after Material's end of life (2026-11-05) is the cost; see below |
| 3. Docusaurus eligible only if it passes all six | No: fails check 5 (`slug`, `id`), adds Node and 1,274 packages and licences off the allowlist |
| 4. Recommendation to the owner as a proposed ADR | The draft is at the end of this file |

## Known issues to carry (instead of rerunning the Zensical checks in P0)

The Zensical checks were run once, on 0.0.73. They are not rerun for P0 (owner direction); the parallel Zensical job re-tests every change from P3.

| # | Issue | Effect on the switch | Where it lands |
| --- | --- | --- | --- |
| 1 | `/`-rooted links are emitted verbatim (FR8.2 check 2). `validation.links.absolute_links` is ignored and no other key helps. GitHub also resolves rooted links from the repository root, not `knowledge/` (V-10) | **The blocker.** A relative-links-only rule would fix both | Decision on P-15 before P1's link check |
| 2 | `validation.links.anchors` is ignored; Zensical's own keys are `invalid_links` and `invalid_link_anchors`. Whether MkDocs tolerates those keys in the shared file is **untested** | The shared `mkdocs.yml` may need both sets | P3, with the first shared config |
| 3 | Zensical skips unsupported settings without warning, so an exit code proves nothing | Judge on output: page-list comparison and offline link check (W-08) | P3 |
| 4 | Non-ASCII automatic slugs differ from GitHub's in MkDocs and Zensical (`uberschuss` against `überschuss`) | Explicit anchors, as AD-14 already requires | None beyond AD-14 |
| 5 | Alpha software: 0.0.72 to 0.0.73 took one day; behaviour can change between releases | Exact pin; review the build on each bump | P3 onwards |
| 6 | No `gh-deploy`, no `--site-dir`, no `tags.json` | Publishing is host-specific (Pages artifact); build in separate copies | P3 |
| 7 | MPL-2.0 `pathspec` in both stacks (and `certifi` in MkDocs) | Recorded exception in `constraints.md` under an ADR, whichever builder is blocking | P1 or P3 |
| 8 | Material ends on 2026-11-05; the blocking build then has no fixes, and Material prints a MkDocs 2.0 banner | Exposure limited while sites are private previews; `mkdocs<2` pin; review date set | Recorded in ADR-001 |
| 9 | Python 3.14 on Windows uses zlib-ng (unrelated to the site, relevant to archives) | None for the site | P-11 |

## Proposed ADR-001 (text for approval; number assigned on approval)

**Title:** `ADR-001-site-generator.md`

**Status:** Proposed. Links: none (no RFC).

**Context.** AD-13 and QA-38 require the generator decision at the P0 exit because Material for MkDocs reaches end of life on 2026-11-05. V-03 and V-04 (2026-10-27, Zensical 0.0.73, Docusaurus 3.10.2) found that Zensical fails FR8.2 check 2 by configuration alone and Docusaurus fails check 5.

**Decision.** Confirm AD-13: MkDocs 1.6.1 with Material 9.7.x is the blocking build (`mkdocs<2`); Zensical, exact-pinned, builds the same `mkdocs.yml` non-blocking, with an offline link check and a page-list comparison on its output. The expected release site is Zensical. Zensical becomes blocking, and MkDocs non-blocking, when it passes all six FR8.2 checks on the pilot bundle by configuration alone and its dependency licences are on the allowlist or recorded as exceptions. The switch is recorded in a later ADR. Docusaurus is not adopted.

**Consequences.**
- The blocking build depends on software past its end of life from 2026-11-05; the exposure is accepted while sites are previews, with review no later than the pilot (P4) and at the switch.
- The link rule (P-15) is a precondition of the switch, since check 2 cannot pass with `/`-rooted links.
- `docs/development/constraints.md` row "Site" ("Zensical build non-blocking until the P0 generator decision") needs its wording changed to "until the switch criterion in ADR-001 is met"; that change needs this ADR.
- MPL-2.0 exceptions (`pathspec`, `certifi`) are recorded in `constraints.md` under their own ADR.

**Supersedes:** none. It confirms AD-13 and settles the review item in QA-38.

**Alternatives.** Zensical blocking now (fails check 2). Docusaurus (fails check 5; Node toolchain; licences). Waiting for a later Zensical release (does not remove the post-end-of-life exposure and delays the decision past its due date).
