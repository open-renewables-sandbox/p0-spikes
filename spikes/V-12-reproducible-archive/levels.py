"""Which gzip levels give equal bytes across zlib implementations? Prints sha12 per level for the pax tar of a tag."""
import sys, io, gzip, hashlib, tarfile, zlib, platform
sys.path.insert(0, __file__.rsplit("/", 1)[0].rsplit("\\", 1)[0])
import build_archive as b
tag, prefixes = sys.argv[1], sys.argv[2:]
items = b.entries(tag, prefixes); mt = int(b.git("log", "-1", "--format=%ct", f"{tag}^{{commit}}").decode())
tar = b.build_tar(items, mt, tarfile.PAX_FORMAT)
print(platform.python_version(), zlib.ZLIB_RUNTIME_VERSION, "tar", len(tar), "bytes")
for lvl in range(0, 10):
    g = b.gz(tar, lvl); print(f"  L{lvl}: {hashlib.sha256(g).hexdigest()[:12]} {len(g)} bytes")
