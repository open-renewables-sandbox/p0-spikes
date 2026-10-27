# p0-spikes

Throwaway verification spikes for build phase P0 of the OKF library template (V-01 to V-13). Nothing here ships. Content is synthetic; the repository is public.

| ID | Result | Outcome |
| --- | --- | --- |
| V-01 | [spikes/V-01-anchors](spikes/V-01-anchors/RESULT.md) | AD-14 holds; GitHub lower-cases explicit ids; scroll partly unconfirmed |
| V-02 | [spikes/V-02-nested-lists](spikes/V-02-nested-lists/RESULT.md) | Four-space nests everywhere; two-space differs (GitHub nests, MkDocs and Zensical do not) |
| V-03 | [spikes/V-03-zensical](spikes/V-03-zensical/RESULT.md) | Zensical 0.0.73 fails check 2 (rooted links); other checks equal |
| V-04 | [spikes/V-04-docusaurus](spikes/V-04-docusaurus/RESULT.md) | Docusaurus 3.10.2 passes 5 of 6; check 5 fails on reserved `slug`/`id` |
| V-08 | [spikes/V-08-okf-skills](spikes/V-08-okf-skills/RESULT.md) | Vendorable, same script as Action; no finding codes; tolerates offset-less datetimes |
| V-11 | [spikes/V-11-verified-tier](spikes/V-11-verified-tier/RESULT.md) | Tier from any `human:` entry; `ci:` accepted but §7 prefers `process:` |
| V-12 | [spikes/V-12-reproducible-archive](spikes/V-12-reproducible-archive/RESULT.md) | tar identical on 8 runs; tar.gz differs under zlib-ng (Python 3.14 on Windows) |
| V-13 | [spikes/V-13-poe-tasks](spikes/V-13-poe-tasks/RESULT.md) | Passed on ubuntu, macOS, Windows × 3.11, 3.14; bare `poe` exits 1 |
