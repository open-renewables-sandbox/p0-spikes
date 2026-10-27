"""Render lists.md with Python-Markdown under several extension sets; print list tree. Usage: render.py"""
import markdown, re, pathlib, sys
src = pathlib.Path(__file__).with_name("lists.md").read_text(encoding="utf-8")
def tree(html):
    """Return 'depth:text' for each list item's own text (depth = number of enclosing ul/ol)."""
    out, depth = [], 0
    for m in re.finditer(r"<(/?)(\w+)[^>]*>|([^<]+)", html):
        if m.group(2):
            if m.group(2) in ("ul", "ol"):
                depth += -1 if m.group(1) else 1
        elif m.group(3).strip() and depth:
            out.append(f"{depth}:{m.group(3).strip()}")
    return out
for name, exts, cfg in [
  ("site set (footnotes, attr_list, toc)", ["footnotes", "attr_list", "toc"], {}),
  ("site set + sane_lists", ["footnotes", "attr_list", "toc", "sane_lists"], {}),
]:
    html = markdown.markdown(src, extensions=exts, extension_configs=cfg)
    print("==", name, "| Markdown", markdown.__version__)
    print("  ", " | ".join(tree(html)))
