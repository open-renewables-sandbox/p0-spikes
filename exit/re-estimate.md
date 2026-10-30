# P0 re-estimate of P1 to P4 (draft, 2026-10-28)

Status: **proposal, not applied.** Label: **[Inf]** throughout; person-days for one maintainer, as in SDD §14.

## Result

| Phase | SDD §14 now | Revised | Change |
| --- | --- | --- | --- |
| Set-up | 0.5 | 0.5 | done |
| P0 Verification | 2–3 | 2–3 (done) | see "What P0 cost" |
| P1 Core tooling | 10–15 | **11–16** | +1 |
| P2 CI and governance | 8–12 | **9.5–14.5** | +1.5 to +2.5 |
| P3 Site, release, skills | 4–6 | **5–7** | +1 |
| P4 Pilot and hardening | 5–8 | 5–8 | none |
| **Remaining after P0 (P1 to P4)** | 27–41 | **30.5–45.5** | +3.5 to +4.5 |
| **Whole programme** | 29.5–44.5 (table total) | **33–49** | +3.5 to +4.5 |

The revised range overlaps the 25 October review's 35–55 (QA-45), with its lower end slightly below it. It cannot be narrowed further before P1 delivers actuals, because no spike exercised the core module: the spikes tested platforms, tools and renderers, not `okfprofile`.

## Where the additions come from

| Phase | Added work, from a V-item | Days |
| --- | --- | --- |
| P1 | Map okf-skills messages to `OKF1xx` by text and test the mapping against the pinned messages, or patch the vendored script to emit codes (V-08) | +0.5 to 1 |
| P1 | Check for two-space nesting in formats with children; lower-case anchor-id comparison; `.gitattributes`; escaped imports in `CLAUDE.md` (V-02, V-01, V-13, V-10) | +0.25 |
| P1 | Link check follows the P-15 decision; if relative links only, the root-relative handling is dropped, which is slightly less code | −0.25 to +0.25 |
| P2 | App creation and recording the approval, stale-approval and App-bypass fixtures that were carried (V-05 5a, 5c) | +0.5 to 1 |
| P2 | Revision writer retries or falls back when `commits/{sha}/pulls` lags the push (V-05) | +0.25 to 0.5 |
| P2 | Document the optional Claude Code adapter and give it one command or task; no copy path (V-09, P-8 option (n), owner decision 2026-10-30) | +0.1 to 0.25 |
| P2 | Archive rule across zlib implementations: choose the digest or compressor rule and test it on 3.11 and 3.14 (V-12) | +0.25 to 0.5 |
| P2 | Platform-step timing with a second person (V-06, carried) | +0.25 |
| P3 | Shared `mkdocs.yml` for both builders, Zensical output checks, licence exceptions (V-03) | +0.5 to 1 |

## What P0 cost

Elapsed: 2026-10-26 to 2026-10-28 for the spikes and the exit documents, done by an agent with the owner approving; the owner's own time was a few reviews and decisions and was not measured, so P0's 2–3 days is not re-based. Items carried out of P0 add to P2 and P3 above, not to P0.

## Largest uncertainties

1. P1 (11–16): the biggest block and untested by any spike; the 85 % coverage and mypy-strict limits in `constraints.md` add effort that is easy to underestimate.
2. P2 (9.5–14.5): the `git-local` adapter, W-12 and the reproducible archive carry the widest spread.
3. Any carried item that fails when run (V-05 5a, 5c) moves work into P2.
