# V-02 Nested list indentation: result

Date: 2026-10-27. Fixture: `lists.md`. Script: `render.py`; output: `python-markdown-output.txt`. Python-Markdown 3.11.2 (the version installed by both MkDocs 1.6.1 and Zensical 0.0.73) on Python 3.12 and 3.14, extensions `footnotes`, `attr_list`, `toc`; repeated with `sane_lists`.

## Python-Markdown **[Test]**

| Case | Result |
| --- | --- |
| Two-space nested unordered items (`  - A1`) | **Not nested**: `A1` and `A2` render at the same depth as `A` |
| Two-space nested ordered items | Not nested |
| Check-format children at two spaces (`  - Pass: …`) | Not nested; "Pass" and "Fail" become siblings of "Gate" |
| Four-space nested unordered, ordered, and check-format children | **Nested** (depth 2) |
| Continuation paragraph and nested item at four spaces | Nested correctly |
| `sane_lists` added | No change for two-space nesting |

The built MkDocs and Zensical sites (V-03) show the same nesting on the `nested-lists` page; the Docusaurus build (V-04, CommonMark) nests both two-space and four-space items.

## GitHub **[Test]**

`lists.md` viewed on github.com (rendered DOM, list depth per item):

| Case | GitHub |
| --- | --- |
| Two-space nested **unordered** items | **Nested** (differs from Python-Markdown, which flattens them) |
| Two-space nested **ordered** items | Not nested (CommonMark needs the content offset, 3 spaces for `1. `) |
| Four-space nested unordered, ordered, check-format children | Nested (depth 2) |
| Continuation paragraph and nested item at four spaces | Nested correctly |

## Comparison

| Case | GitHub | Python-Markdown (MkDocs, Zensical) | Docusaurus (CommonMark) |
| --- | --- | --- | --- |
| Two-space unordered | nested | **flat** | nested |
| Two-space ordered | flat | flat | not recorded separately |
| Four-space (all forms) | nested | nested | nested |

## Outcome

**I-01's rule holds: four-space indentation nests identically on GitHub, Python-Markdown and Docusaurus.** Two-space indentation is not safe: it nests on GitHub and Docusaurus but not on MkDocs or Zensical, so a two-space "Checks" sub-list would render differently on the site and on GitHub. `sane_lists` does not change this. The validator should flag two-space nesting in sections whose format has children (I-04), a P1 input. **P-4 is not triggered.**
