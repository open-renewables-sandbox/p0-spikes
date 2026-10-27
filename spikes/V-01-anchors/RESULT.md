# V-01 Anchors on GitHub: result

Date: 2026-10-27. Labels: **[Test]** observed on github.com in the built-in browser (file view of `anchors.md` and `linker.md` in this repository, signed out), **[Inf]** inferred. Fixtures: `anchors.md` (nine cases, each section pushed below the first screen by filler), `linker.md` (links to each), and `fixtures/bundle/knowledge/glossary.md`.

## Outcome

**AD-14 holds.** GitHub keeps explicit `<a id>` anchors placed before or inside a heading, accepts them beside its automatic heading anchor with the same id, and generates the slugs AD-14 assumes. One refinement: GitHub lower-cases explicit ids, so ids must be lower case.

## Cases **[Test]**

| Case | Rendered result |
| --- | --- |
| 1 `<a id="alpha-term"></a>` on its own line before `## Alpha term` | kept as `<a id="user-content-alpha-term">` in a paragraph above the heading |
| 2 `## <a id="beta-term"></a>Beta term` | kept inside the `h2` as `user-content-beta-term` |
| 3 explicit id equals the automatic slug (`gamma-term`) | **two elements with the same id** (explicit `<a>` and GitHub's `a.anchor`); the fragment link works |
| 4 explicit `delta-old` before `## Delta renamed` | both `#delta-old` (stable) and `#delta-renamed` (automatic) exist: the explicit id survives a renamed heading, which is the point of AD-14 |
| 5 non-ASCII `überschuss` / `## Überschuss` | automatic slug keeps and lower-cases the non-ASCII letter (`überschuss`); a link with `#%C3%BCberschuss` finds it |
| 6 `## Soiling (loss)` | automatic slug `soiling-loss`; parentheses dropped |
| 7 automatic slug only (`## Zeta term`) | `zeta-term`, present as `a.anchor` |
| 8 `<a id="Eta-Term">` with capitals | GitHub **lower-cases** it to `user-content-eta-term`; no element has the capitalised id; `#Eta-Term` still reaches the lower-case id |
| 9 `## Theta term {#theta-id}` | no id created; the braces stay in the heading text. `{#id}` is therefore unusable on GitHub, as AD-14 says |

All ids on GitHub carry the prefix `user-content-`; GitHub's script maps `#x` to `user-content-x`, so a plain `#x` link works there but the DOM id is not `x`.

## Scrolling **[Test, partial]**

Loading `…anchors.md#<fragment>` scrolled the target to the top of the view for `alpha-term`, `gamma-term`, `delta-old`, `delta-renamed`, `soiling-loss` (screenshot) and `eta-term`. For `beta-term`, `überschuss` and `zeta-term` the scroll did not occur in this automated pane, although the ids exist; scrolling in the pane was inconsistent (it also scrolled on some loads and not on repeats), so this is recorded as unconfirmed rather than failed. A person opening three links in `linker.md` on github.com would close it.

## Other builders (from V-03 and V-04)

MkDocs and Zensical keep explicit anchors but build the automatic slug without non-ASCII letters (`uberschuss`); Docusaurus produces `überschuss` like GitHub. So FR8.2 check 4 depends on explicit anchors for non-ASCII terms in MkDocs and Zensical.

## Feeds

AD-14 confirmed; **P-3 is not triggered**. For the P1 validator (`OKF4xx` anchor check): compare ids case-insensitively or require lower case; a duplicate explicit and automatic id is expected, not an error.
