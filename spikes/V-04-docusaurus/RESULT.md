# V-04 Docusaurus in `detect` mode: result

Date: 2026-10-27. Labels: **[Test]** observed here. Fixture: `fixtures/bundle/knowledge` (synthetic; 8 concepts plus indexes, vocabulary and glossary, not just three). Config: `docusaurus.config.js` and `package.json` in this folder (`markdown.format: 'detect'`, `routeBasePath: '/'`, `onBrokenLinks: 'throw'`, broken markdown links `throw`).

Versions: `@docusaurus/core` and `preset-classic` **3.10.2** (npm, 2026-10-23), React 18.3.1, Node 24.22.0, npm 11.19.1, Windows. Build ran once, on Python-independent Node 24 only; not repeated on other Node versions.

## Outcome

**Passes five of the six FR8.2 checks. Fails check 5: the reserved frontmatter key `slug` moved a page to a different URL.** The build succeeded with broken-link errors set to throw. It adds a Node toolchain of 1,274 packages and several licences not on the allowlist.

## Six FR8.2 checks

| Check | Result | Evidence |
| --- | --- | --- |
| 1 `index.md` is the folder landing page | pass | `/example-group/example-category/` built from `index.md` |
| 2 `/`-rooted links resolve | pass | `/example-group/example-category/example-item.md` and `/glossary.md#soiling-loss` became `/glossary#soiling-loss` and a doc route; the build would throw on a broken one |
| 3 non-standard frontmatter keys ignored | pass | `custom_unknown_key` neither leaked nor warned |
| 4 anchors match GitHub's | pass | explicit `<a id>` kept; heading ids `soiling-loss`, `derate`, `module-degradation`, `überschuss` equal GitHub's slugs (Docusaurus uses a GitHub-style slugger, unlike Python-Markdown's `uberschuss`); non-ASCII link is percent-encoded `#%C3%BCberschuss` and matches; duplicate explicit and automatic ids are both emitted |
| 5 reserved keys harmless; colon tags valid | **fail** (keys), pass (tags) | `slug: reserved-slug-test` in the example item moved it to `/example-group/example-category/reserved-slug-test` and `/example-item` no longer exists; `id` is also reserved by Docusaurus. Colon tags became `/tags/group-example-group` (colon to hyphen), valid pages |
| 6 angle brackets, braces, footnotes | pass | `<title>` in a code span, `{brace}`, escaped `<word>` unchanged; footnote ids `user-content-fn-a` work; `<!-- Maintained by CI -->` caused no error (the comment is not in the output) |

Nested lists: both two-space and four-space nesting rendered as nested lists (3 nested lists, depth 2) **[Test]**; feeds V-02.

Other observations: a file named `file with spaces.md` builds at a URL containing literal spaces (`/…/file with spaces`); the example item's revision line and footnote rendered; build time 11 s for the fixture, install 71 s.

## Footprint

- Direct dependencies: 4. Installed packages: 1,274; `node_modules` 259 MB.
- Licences (package.json fields): mostly MIT, ISC, BSD, Apache-2.0, 0BSD. Not on the `constraints.md` allowlist: `caniuse-lite` CC-BY-4.0, `mdn-data` CC0-1.0, `sax` BlueOak-1.0.0, `opener` and `path-is-inside` (WTFPL OR MIT), `type-fest` (MIT OR CC0-1.0), `require-like` (no licence field). No GPL, LGPL, AGPL or MPL package seen. These may be reached as dual-licensed choices, which the allowlist rules would need to say.
- Using Docusaurus adds Node and npm to a Python-only repository (AD-03 reasons; supply-chain exposure) and a second lock file.

## Feeds

SPEC criterion 3: C needs all six checks, so with `slug` and `id` a profile would have to forbid those keys (a profile rule, not configuration) before C is eligible. It also needs an ADR for the Node toolchain and licence exceptions.
