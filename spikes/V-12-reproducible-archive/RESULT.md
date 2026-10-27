# V-12 Reproducible archive: result

Date: 2026-10-27. Labels: **[Test]**. Prototype: `build_archive.py` (not the template's `build_bundle.py`). Input: tag `v0.0.1-p0`, 18 files (the fixture bundle and `fixtures/archive-extra/`: an executable `run.sh`, an empty file, a binary, a non-ASCII name with spaces). Runs: GitHub Actions run [40451497123](https://github.com/open-renewables-sandbox/p0-spikes/actions/runs/40451497123) (ubuntu-latest, macos-latest arm64, windows-latest × Python 3.11 and 3.14: six jobs) plus this Windows machine (python.org-style builds, 3.11.15 and 3.14.0). Eight runs in all. Evidence: `evidence/compare-output.md`, `evidence/levels-output.txt`.

I-12 settings applied: entries from the tag's tree objects (never the working tree), sorted by path bytes, modes normalised to 0644/0755 from the git mode, uid and gid 0, empty names, mtime from the tagged commit, gzip with no file name and mtime 0. Directories are omitted.

## Outcome

**The uncompressed tar is byte-identical on all eight runs, for ustar, GNU and PAX formats. The `.tar.gz` is not: its SHA-256 differs between Python builds that use different zlib implementations.** Python 3.14 on Windows (both hosted and local) links **zlib-ng** (`1.3.1.zlib-ng`); every other build used classic zlib (1.2.11, 1.2.12, 1.3.1, 1.3.2) and all those agree at levels 6 and 9. So I-12's claim "rebuilding from the tag yields the same SHA-256" holds across Linux, macOS and Windows and across zlib versions, but **fails across zlib implementations**, which a Python version change can introduce.

| Variant | Distinct digests across 8 runs |
| --- | --- |
| tar (ustar, gnu, pax) | 1 each |
| tar.gz at level 6 or 9 (any format) | 2: {zlib builds} and {Windows Python 3.14, zlib-ng} |
| tar.gz at level 0 (stored) | 1: identical on zlib 1.3.2 and zlib-ng (the only level that matched in the 3.11 versus 3.14 comparison; 1 to 9 all differ) |

`tarfile.DEFAULT_FORMAT` is PAX on every build tested, so the default did not vary; the script sets the format explicitly anyway.

## Options (for the owner; none chosen here)

1. Record and verify the SHA-256 of the **uncompressed tar** as the canonical content hash, and treat the `.tar.gz` digest as valid only when rebuilt with the same compressor.
2. Write the archive at gzip level 0 (stored): reproducible everywhere tested, at about ten times the size here (30,743 bytes against about 2,600 for level 9).
3. Pin the interpreter build used for archives (for example by building only in CI with one stated Python), and say so in W-12 step 5.
4. Use a compressor with a specified output across implementations.

## Not tested

Real macOS or Linux hardware (hosted runners only; D-4 default); the effect of `core.autocrlf` on a working-tree-based build (the prototype never reads the working tree, which is the design point); symlink entries (V-09); archives larger than 30 KB; zlib-ng on Linux or macOS (those builds used classic zlib).

## Feeds

I-12, W-12 step 5, QA-61, FR6.6 and FR7.3 acceptance wording. **Proposed entry P-11 is triggered** (SPEC): the I-12 claim needs one of the options above.
