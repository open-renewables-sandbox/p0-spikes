# V-11 Tier derivation from `verified`: result

Date: 2026-10-27. Labels: **[Doc]** read from the pinned specification, **[Test]** read from code. Sources: OKF specification at `ad30107c31c06aec8a7d5636e0d1058118604e6f` (2026-08-21), `SPEC.md` §5.2, §5.3, §7, §11 (clone of `GoogleCloudPlatform/open-knowledge-format` in git-ignored `.work/v11/`); okf-skills `a8b96420…`, `skills/visualize/scripts/okf_visualize.py` lines 276 to 284.

## Outcome

**The tier comes from any entry, not the latest one.** SPEC §5.3: no `verified` key is *unverified*; `verified` by non-`human:` actors only is *machine-confirmed*; `verified` by a `human:<id>` actor is *human-reviewed*. The reference consumer in okf-skills implements it as `verified.some(e => e.by.startsWith('human:')) ? human-reviewed : machine-confirmed`, case-sensitive on the exact lowercase `human:` prefix. "How recently" uses the latest `at` (§5.2) and does not affect the tier.

## Non-human actor prefix

§5.3 treats **every** non-`human:` actor as machine; it names no required prefix. §7 gives the convention: `<producer>/<version>` for agents and tools, `process:<id>` for an automated process. okf-skills warns on near-misses of `human:` or `process:` (for example `Human:dana`) and accepts `ci:bot` silently. A bare mapping counts as a one-element list (§5.2, §11).

## Check of I-08's `verified` mapping

| I-08 rule | Against §5.3 |
| --- | --- |
| Human-reviewed: one `{by: human:<login>, at}` per owner approval or owner self-approval in the window | Consistent: any `human:` entry gives human-reviewed |
| Machine-confirmed: one `{by: ci:<bot>, at}` and **no** `human:` entries | Tier is consistent (every actor is non-`human:`). `ci:` is not the §7 convention; `process:<bot>` would match it |
| Unverified: no `verified` key | Consistent |
| FR3.8 "an OKF tool's derived tier equals the library's" | Holds at the three-tier level. The `(self)` qualifier cannot be seen by a generic tool, which reports plain human-reviewed |

The rule that the writer must emit **no** `human:` entries for a Machine-confirmed concept is required, because one such entry would make a generic tool report human-reviewed.

## Feeds

I-08 mapping confirmed as to tiers; one wording change is available but optional: `ci:<bot>` to `process:<bot>` for §7 alignment. Under SPEC criteria this is an SDD edit and a proposed-entry decision for the owner (P-10 is triggered only in this minor form). Specification text quoted by section, not reproduced.
