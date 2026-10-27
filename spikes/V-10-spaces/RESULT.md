# V-10 Spaces in file names: result

Date: 2026-10-27. Labels: **[Test]** observed. Sessions: V-10a, a fresh Claude Code session with `okf-library-template` as working directory (branch `docs/p0-verification-plan`, read-only); V-10b, a fresh session in p0-spikes with `CLAUDE.md` probes in `docs-probe/` (round 1). Link forms viewed on github.com and built with MkDocs 1.6.1 and Zensical 0.0.73. Round 2 of V-10b (real-name patterns) is pending; see the end.

## Outcome

**The four `@` imports in the template's `CLAUDE.md` do not load.** All four target files exist at the stated paths; the text of none reached the session's context, while the two space-free imports (`@AGENTS.md`, `@docs/development/AGENTS.md`) did. In round 1, of six import forms for names with spaces, **only the backslash-escaped form loaded**.

## V-10a (template repository) **[Test]**

| Import in `CLAUDE.md` | Loaded |
| --- | --- |
| `@docs/development/requirements/OKF Library Template - Software Requirements Spec.md` | no |
| `@docs/development/architecture/OKF Library Template - Software Design Document.md` | no |
| `@docs/development/adr/OKF Library Template - Design Decision Record.md` | no |
| `@docs/development/architecture/OKF library technology stack options.md` | no |

So the check SDD §15 names ("ask for a summary of the SRS") fails as the files are written.

## V-10b round 1: import forms **[Test]**

| Form | Example | Loaded |
| --- | --- | --- |
| raw spaces | `@docs-probe/A raw spaces.md` | no |
| backslash-escaped spaces | `@docs-probe/B\ escaped\ spaces.md` | **yes** |
| double-quoted | `@"docs-probe/C quoted spaces.md"` | no |
| percent-encoded | `@docs-probe/D%20percent%20encoded.md` | no |
| angle brackets | `@<docs-probe/E angle brackets.md>` | no |
| hyphenated file name (control) | `@docs-probe/f-hyphenated.md` | yes |
| quoted, nested folder with a space | `@"docs-probe/sub folder/G nested.md"` | no |

## Markdown link forms from a subfolder **[Test]**

| Form | GitHub | MkDocs | Zensical |
| --- | --- | --- | --- |
| `[x](../A raw spaces.md)` (raw spaces) | **not a link** (shown as text) | link, resolves | resolves; href keeps the spaces |
| `[x](../A%20raw%20spaces.md)` | link, resolves | resolves | resolves |
| `[x](<../A raw spaces.md>)` | link, resolves | resolves | resolves; href keeps the spaces |
| `[x](/A%20raw%20spaces.md)` (root-relative) | resolves **from the repository root** | resolves | **fails** (as in V-03) |
| `[x](</A raw spaces.md>)` | same as above | resolves | fails |

okf-skills also warns "cross-link target not found" for a `%20` link, because it does not decode (V-08), though it tolerates the link.

## Additional finding: root-relative links on GitHub

On github.com a `/`-rooted link resolves from the **repository root**, not from the bundle root. In the fixture (`fixtures/bundle/knowledge/…`) `/glossary.md#soiling-loss` rendered as `…/blob/main/glossary.md#soiling-loss`, a path that does not exist, since the file is at `…/fixtures/bundle/knowledge/glossary.md` (the live request was rate-limited, so the 404 is inferred from the path). I-01 allows "bundle-root-relative (`/path/to/concept.md#anchor`) or relative" links, and the template's bundle is under `knowledge/`; such links work on the MkDocs site but break on GitHub and on Zensical. Relative links resolve on all of them.

## Feeds

- **P-9 is triggered, in a smaller form than renaming:** the file names can stay (QA-36, QA-67, AD-21) if `CLAUDE.md` uses the escaped form (`@docs/development/requirements/OKF\ Library\ Template\ -\ Software\ Requirements\ Spec.md` style). Round 2 checks that with hyphens and nesting before it is proposed.
- **A new proposed entry, P-15:** I-01's root-relative link rule against GitHub's behaviour. A relative-links-only rule would also remove the Zensical check 2 failure (V-03). I-01, FR2.10 and W-04 check 4 are affected; FR2.10 says links must resolve on the hosting platform, so this is a requirement-level concern for the owner.
- The link form for names with spaces: `%20` or angle brackets work everywhere tested; raw spaces fail on GitHub.

## Pending: round 2

`CLAUDE.md` in p0-spikes now holds three escaped-form imports with real-name patterns (hyphens, a folder `sub folder`, and an import inside an imported file), expecting tokens CANARY-F, H, I and J. It needs one more fresh session in p0-spikes; one could not be started automatically in this turn.
