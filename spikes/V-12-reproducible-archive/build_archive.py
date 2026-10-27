"""V-12 prototype of the I-12 reproducible archive. Throwaway; not the template's build_bundle.py.

Builds <out>.tar.gz from the tree objects of a git tag (never the working tree), with entries sorted by path,
modes normalised, uid/gid 0, empty names, mtime set to the tagged commit's timestamp, and gzip written with no
file name and a zero timestamp.

Usage: build_archive.py <tag> <prefix> [<prefix> ...] --out DIR [--json FILE]
Prints one JSON object with SHA-256 digests for several tar formats and compression levels.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import platform
import subprocess
import sys
import tarfile
import zlib


def git(*args: str) -> bytes:
    return subprocess.run(["git", *args], check=True, capture_output=True).stdout


def entries(tag: str, prefixes: list[str]) -> list[tuple[str, int, bytes]]:
    out = []
    for rec in git("ls-tree", "-r", "-z", "--full-tree", tag).split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, kind, sha = meta.decode().split()
        name = path.decode("utf-8")
        if kind != "blob" or not any(name.startswith(p) for p in prefixes):
            continue
        out.append((name, 0o755 if mode == "100755" else 0o644, git("cat-file", "blob", sha)))
    return sorted(out, key=lambda e: e[0].encode("utf-8"))


def build_tar(items: list[tuple[str, int, bytes]], mtime: int, fmt: int) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=fmt) as tf:
        for name, mode, data in items:
            ti = tarfile.TarInfo(name)
            ti.size, ti.mode, ti.mtime = len(data), mode, mtime
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ""
            tf.addfile(ti, io.BytesIO(data))
    return buf.getvalue()


def gz(data: bytes, level: int) -> bytes:
    raw = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=level) as g:
        g.write(data)
    return raw.getvalue()


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag")
    ap.add_argument("prefix", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    mtime = int(git("log", "-1", "--format=%ct", f"{a.tag}^{{commit}}").decode())
    items = entries(a.tag, a.prefix)
    formats = {"ustar": tarfile.USTAR_FORMAT, "gnu": tarfile.GNU_FORMAT, "pax": tarfile.PAX_FORMAT}
    res = {
        "python": platform.python_version(),
        "system": platform.system(),
        "machine": platform.machine(),
        "tarfile_default_format": {tarfile.USTAR_FORMAT: "ustar", tarfile.GNU_FORMAT: "gnu",
                                   tarfile.PAX_FORMAT: "pax"}[tarfile.DEFAULT_FORMAT],
        "zlib_compile": zlib.ZLIB_VERSION,
        "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION,
        "entries": len(items),
        "mtime": mtime,
        "tar_sha256": {},
        "targz_sha256": {},
    }
    for fname, fmt in formats.items():
        try:
            tar = build_tar(items, mtime, fmt)
        except (ValueError, tarfile.TarError) as exc:
            res["tar_sha256"][fname] = f"error: {exc}"
            continue
        res["tar_sha256"][fname] = sha(tar)
        for level in (6, 9):
            res["targz_sha256"][f"{fname}-L{level}"] = sha(gz(tar, level))
    text = json.dumps(res, indent=2, sort_keys=True)
    if a.json:
        open(a.json, "w", encoding="utf-8", newline="\n").write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
