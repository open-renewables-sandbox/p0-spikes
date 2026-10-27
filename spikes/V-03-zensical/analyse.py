"""Print facts about a built site for the V-03 matrix. Usage: analyse.py <site_dir>"""
import re, sys, pathlib, json
site = pathlib.Path(sys.argv[1])
def rd(rel):
    p = site / rel
    return p.read_text(encoding="utf-8") if p.exists() else None
cat = "example-group/example-category"
pages = {
    "item": f"{cat}/example-item/index.html",
    "links": f"{cat}/links-and-anchors/index.html",
    "lists": f"{cat}/nested-lists/index.html",
    "prose": f"{cat}/prose-hazards/index.html",
    "glossary": "glossary/index.html",
    "spaces": f"{cat}/file with spaces/index.html",
    "spaces_enc": f"{cat}/file%20with%20spaces/index.html",
    "landing": f"{cat}/index.html",
    "root": "index.html",
}
h = {k: rd(v) for k, v in pages.items()}
print("pages present:", {k: (v is not None) for k, v in h.items()})
all_html = "".join(p.read_text(encoding="utf-8", errors="replace") for p in site.rglob("*.html"))
print("html files:", len(list(site.rglob("*.html"))))
g = h["glossary"] or ""
print("glossary ids:", re.findall(r'id="([^"]+)"', g.split("<article")[-1])[:20])
print("headerlinks (toc permalink):", len(re.findall(r'class="headerlink"', all_html)))
print("edit link present:", bool(re.search(r'edit/main/knowledge/', all_html)), "| sample:", (re.findall(r'href="([^"]*edit/main/knowledge/[^"]*)"', all_html) or [None])[0])
print("social issues link:", "issues/new/choose" in all_html)
print("status markup (md-status):", "md-status" in all_html, "| 'Draft' text:", "Draft" in all_html)
it = h["item"] or ""
print("tags rendered (md-tags/tag):", bool(re.search(r'md-tag', it)), re.findall(r'class="md-tag[^"]*"[^>]*>([^<]*)<', it)[:5])
print("tags index/json:", [p.name for p in site.rglob("tags*")])
print("footnote refs/defs in prose:", len(re.findall(r'class="footnote-ref"', h["prose"] or "")), len(re.findall(r'class="footnote"', h["prose"] or "")))
pr = h["prose"] or ""
print("prose: <title> literal kept in code:", "&lt;title&gt;" in pr, "| {brace} kept:", "{brace}" in pr, "| escaped <word> text:", "&lt;word&gt;" in pr)
print("html comment in output:", "Maintained by CI" in (h["item"] or ""))
print("unknown key leaked into page:", "kept-but-ignored" in it, "| reserved slug leaked:", "reserved-slug-test" in it)
li = h["lists"] or ""
print("nested ul depth markers (ul within li):", len(re.findall(r'<li>[^<]*\n?<ul>', li)), "| ol within li:", len(re.findall(r'<li>[^<]*\n?<ol>', li)))
print("nested lists raw:", re.sub(r'\s+', ' ', li.split("<article")[-1])[:0])
lk = h["links"] or ""
print("rooted links emitted verbatim (href starts '/' ending .md):", re.findall(r'href="(/[^"]*\.md[^"]*)"', lk))
print("landing page title:", re.findall(r'<h1[^>]*>([^<]*)<', h["landing"] or "")[:1], "| nav mentions example-category:", "example-category" in (h["root"] or ""))
print("spaces page built at:", [str(p.relative_to(site)) for p in site.rglob("*") if "spaces" in p.name][:3])
sp_link = re.findall(r'href="([^"]*spaces[^"]*)"', h["landing"] or "")
print("link to spaces page in landing:", sp_link)
