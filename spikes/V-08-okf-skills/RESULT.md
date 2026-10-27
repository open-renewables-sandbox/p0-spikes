# V-08 okf-skills validator: result

Date: 2026-10-27. Labels: **[Test]** observed here. Source: `scaccogatto/okf-skills` at `a8b96420de90d102c43cda1693d01ec4f925f2ab` (tag `okf--v0.10.3`, commit date 2026-10-13), cloned into git-ignored `.work/v08/`. Script: `skills/validate/scripts/okf_validate.py` (600 lines). Cases: `run_cases.py` in this folder. Python 3.11, 3.12 and 3.14 each run the script via `uv run --with pyyaml`; the JSON report is byte-identical on the fixture.

## Outcome

AD-08's integration holds: the Action runs exactly this script (`action.yml` calls `uv run "$GITHUB_ACTION_PATH/skills/validate/scripts/okf_validate.py"`), so the vendored copy gives the same result locally and in CI. Three things change how `okfprofile` must use it: findings have **no codes**, only two rules are **errors**, and the script **tolerates** the datetime shapes FR1.2 forbids.

## Vendoring

- One file; its only dependency is `pyyaml>=6,<7` (PEP 723 header). `validate(bundle)` and `Report` are importable with no side effects; `main()` adds `--strict`, `--max-warnings N`, `--migrate`, `--json`.
- Licences: repository MIT (Marco Boffo); `NOTICE` records that the vendored OKF v0.2 specification text is Apache-2.0, Google LLC. Carry both licence texts if the script is vendored. PyYAML is MIT.
- PyYAML parses YAML 1.1, so it enters the validation dependency set beside ruamel.yaml (`constraints.md`: validation set "plus the vendored okf-skills validator and their dependencies" already allows this).

## Findings and a proposed mapping to `OKF1xx`

The report is `{errors: [str], warnings: [str], counts}`. Each string starts `<path>: §<spec section> <text>`; there are no codes and no line numbers. Mapping therefore keys on the section marker and text prefix, which couples `okfprofile` to message wording (risk R below).

| okf-skills message (section) | Level | Proposed code slot (I-09 `OKF1xx`) |
| --- | --- | --- |
| §11.1 no parseable YAML frontmatter block (also fires when a blank line precedes `---`) | error | OKF101 |
| §11.1 frontmatter is not valid YAML | error | OKF102 |
| §11.1 frontmatter must be a YAML mapping | error | OKF103 |
| §11.2 missing or empty `type` | error | OKF104 |
| §4.1 recommended field `title`, `description` or `tags` absent | warning | OKF110 (profile schema, check 2, covers this) |
| §5.2 `generated` or `verified` shape; `by` missing | warning | OKF12x |
| §7 actor near-miss of `human:` or `process:` | warning | OKF13x |
| §5.2 `verified[].at`, §5.5 `stale_after` not RFC 3339 / ISO 8601 | warning | OKF14x |
| §5.4 unknown `status` | warning | OKF15x (profile status list is stricter) |
| §8 index with frontmatter; §12 root index extra key or other `okf_version`; §9 log date heading | warning | OKF16x |
| §5.1 `sources` shape | warning | OKF17x |
| cross-link target not found (§6.1, tolerated) | warning | not mapped: check 4 owns links |

Numbers are slots, not decisions; I-09 assigns them.

## Behaviour that matters

| Case | Result |
| --- | --- |
| Fixture bundle (9 concepts, 4 indexes) | conformant, exit 0; 10 warnings: nine "recommended `generated` absent", one cross-link |
| Generated `index.md` files (no frontmatter; root with `okf_version: "0.2"`) | accepted. Frontmatter on a non-root index, an extra root key, `okf_version` other than 0.2 and a non-ISO `log.md` heading each give a **warning**, never an error |
| `stale_after` without an offset, and as a bare date | **silent**: no warning. FR1.2's datetime-offset rule must stay in `okfprofile` (AD-08 already says so) |
| `stale_after: next week` | warning |
| `verified.by` = `human:alice`, `process:ci-bot` | accepted. `Human:alice` gives a near-miss warning |
| `verified.by` = `ci:bot` | **accepted silently**: the prefix family is open |
| `[^1]` footnote with no `sources` key | no warning (the check runs only when `sources` is present) |
| Link `file%20with%20spaces.md` in an index | **false warning** "target not found": the script does not percent-decode. Relevant to V-10 |
| `--strict` | turns every warning into a failure; with the nine `generated` warnings it fails the fixture, so the profile validator must run it without `--strict` and apply its own levels |

## Risks and feeds

- R: wording coupling, since there is no structured output. Mitigation to propose: pin the commit (already AD-08), test the mapping against the pinned messages, or patch the vendored copy to emit codes and record the patch.
- Feeds: I-09 `OKF1xx` table; AD-08 confirmed with the notes above (proposed entry P-7 is **not** triggered: the validator vendors and runs outside the Action). The `generated` warning noise and `%20` false warning are recorded for P1.
