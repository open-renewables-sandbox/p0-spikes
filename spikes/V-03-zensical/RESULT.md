# V-03 Zensical: result

Date: 2026-10-27. Labels: **[Test]** observed here, **[Doc]** vendor documentation, **[Inf]** inferred.
Fixture: `fixtures/bundle/knowledge` (synthetic), I-13 baseline `mkdocs.yml`, `docs_dir: knowledge`. Analysis script: `analyse.py` (facts from generated HTML, not exit codes).

## Versions

| Tool | Version | Date |
| --- | --- | --- |
| mkdocs | 1.6.1 | |
| mkdocs-material | 9.7.7 | prints a MkDocs 2.0 warning banner at build |
| zensical | **0.0.73** (PyPI upload 2026-10-26; the SDD cites 0.0.72) | |
| Python | 3.11.15, 3.12.10, 3.14.0 | output facts identical on all three, both builders **[Test]** |

## Outcome

**Zensical 0.0.73 still fails FR8.2 check 2: it emits `/`-rooted links verbatim.** MkDocs rewrites them. No configuration key found changes this. Every other tested feature gave the same output in both builders.

## Feature matrix (judged on output)

| Feature | MkDocs 1.6.1 + Material | Zensical 0.0.73 |
| --- | --- | --- |
| `/`-rooted link `/glossary.md#soiling-loss` | rewritten to `../../../glossary/#soiling-loss` | **left as `/glossary.md#soiling-loss`** (dead link) |
| `validation.links.absolute_links` | honoured | **ignored** (not a Zensical key; its documented keys are `invalid_links`, `invalid_link_anchors` **[Doc]**) |
| `validation.links.anchors: warn` | warns on missing anchor | ignored; `invalid_link_anchors: true` warns instead |
| `strict: true` | build passes; aborts on a broken link or anchor | **honoured**: aborts with "5 issues found", one per `/`-rooted link (new since 18 Oct: it now detects them) |
| `site_url` set | n/a | no effect on rooted links |
| `extra.status` + page `status:` | status markup and "Draft" present | same |
| `extra.social` | issue-form link in footer | same |
| `content.action.edit` + `edit_uri` | edit link to `…/edit/main/knowledge/<file>` | same |
| footnotes | refs and definitions rendered | same |
| `attr_list`, `toc` permalinks | 37 header links | same |
| `tags` with colon tags | labels rendered; with a `<!-- material/tags -->` index page, ids `tag:groupexample-group` | same ids; no `tags.json` |
| Zensical-only `theme.variant: classic` | **tolerated**: strict build passes, no warning | n/a |
| File name with spaces | page built, links `file%20with%20spaces/` | same |

## Six FR8.2 checks

| Check | MkDocs | Zensical |
| --- | --- | --- |
| 1 `index.md` is the folder landing page | pass | pass |
| 2 `/`-rooted links resolve | pass | **fail** |
| 3 non-standard keys ignored, not leaked | pass | pass |
| 4 heading anchors match GitHub's | explicit anchors pass; automatic slug of `Überschuss` is `uberschuss`, GitHub's is `überschuss` | same; duplicate ids (explicit + automatic) emitted by both |
| 5 reserved keys and colon tags harmless | pass | pass |
| 6 angle brackets, braces, footnotes unchanged | pass | pass |

Check 4 supports AD-14: the non-ASCII case works only because of the explicit anchor in both builders. V-01 covers GitHub's side.

## Workarounds for check 2 (none config-only)

- Write links relative instead of root-relative (changes the I-01 link rule). **[Inf]**
- Rewrite `/` links to relative in a pre-build copy of `knowledge/` (a script; source untouched). **[Inf]**
- A custom Python-Markdown extension using the page path, which Zensical exposes to extensions (`zensical/extensions/context.py`). **[Inf]**, none tested.

## Licences (site group, `uv pip` metadata)

Both stacks contain **MPL-2.0** packages: `pathspec` 1.1.1 (in both), `certifi` 2026.10.23 (MkDocs stack). `constraints.md` allows MPL-2.0 only by a recorded exception. Zensical itself is MIT; mkdocs BSD-2-Clause; mkdocs-material MIT. `python-dateutil` reports "Dual License" (Apache-2.0/BSD) and `mergedeep` reports no licence in metadata (MIT per its repository **[Inf]**). Any choice therefore needs exceptions recorded or a check of how the licence check reads SPDX metadata.

## Feeds

SPEC criterion 1: option B (Zensical blocking) is **not eligible** at 0.0.73 because check 2 needs more than configuration. Option A remains eligible. Rerun once at the P0 exit on the then-latest release.
