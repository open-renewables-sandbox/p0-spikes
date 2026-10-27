# V-02 Nested list indentation: result (Python-Markdown part; GitHub part pending)

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

## Interim conclusion

The I-01 rule "indent nested list items four spaces" is **necessary** for MkDocs and Zensical (same parser), not just a preference; `sane_lists` does not remove the need. Whether GitHub renders the four-space form the same (as I-01 states "every candidate parser reads the same way") is the GitHub part, run in Wave 2 against the pushed fixture.
