"""Report how a symlink entry looks in GitHub's tag archives. Usage: inspect_archives.py <tar.gz> <zip> <path-in-repo>"""
import sys, tarfile, zipfile, stat
tgz, zp, rel = sys.argv[1:4]
with tarfile.open(tgz) as t:
    for m in t.getmembers():
        if m.name.endswith(rel):
            print(f"tar.gz: {m.name} type={'symlink' if m.issym() else 'file' if m.isfile() else 'dir' if m.isdir() else m.type!r} linkname={m.linkname!r} mode={oct(m.mode)}")
with zipfile.ZipFile(zp) as z:
    for i in z.infolist():
        if i.filename.endswith(rel):
            mode = i.external_attr >> 16
            print(f"zip: {i.filename} unix_mode={oct(mode)} is_symlink={stat.S_ISLNK(mode)} size={i.file_size} content={z.read(i).decode()[:60]!r}")
