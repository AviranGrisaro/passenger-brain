#!/usr/bin/env python3
"""Convert Passenger PRD/TRD markdown files to standalone, readable HTML.
No external CDN deps -- CSS is inlined. Safe to open as a local file.
"""
import html
import os
import re
import sys

import markdown

# This script lives at passenger-brain/prds/md2html.py — resolve ROOT from its
# own location rather than hardcoding a workspace path (workspace root differs
# per founder; see passenger-brain/CLAUDE.md).
ROOT = os.path.dirname(os.path.abspath(__file__))

# (relative-to-ROOT path) for every PRD / TRD to convert.
FILES = [
    "hood-dataset/hood-dataset.md",
    "hood-dataset/TRD.md",
    "hood-place-detail/hood-place-detail.md",
    "hood-place-detail/TRD.md",
    "live-events-overlay/live-events-overlay.md",
    "live-events-pipeline/live-events-pipeline.md",
    "live-events-pipeline/TRD.md",
    "map-hoods-heat/map-hoods-heat.md",
    "map-hoods-heat/TRD.md",
    "passport/passport.md",
    "places-been-saved/places-been-saved.md",
    "places-dataset/places-dataset.md",
    "places-dataset/TRD.md",
    "search-quick-filters/search-quick-filters.md",
    "time-slider/time-slider.md",
    "time-slider/TRD.md",
    "tourist-trap-flag/tourist-trap-flag.md",
]

# Build the set of markdown paths (absolute, normalized) we are converting,
# so we can rewrite cross-references between them to point at the new .html.
ABS_MD = {os.path.normpath(os.path.join(ROOT, f)) for f in FILES}


def strikethrough(text):
    return re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)


def checkbox_lists(text):
    # Render GitHub-style task list markers as real glyphs.
    text = re.sub(r"(?m)^(\s*[-*]\s+)\[ \]\s+", r"\1☐ ", text)
    text = re.sub(r"(?m)^(\s*[-*]\s+)\[[xX]\]\s+", r"\1☑ ", text)
    return text


LINK_RE = re.compile(r'(href="([^"#]+?)(#[^"]*)?")')


def rewrite_links(html_body, src_abs_path):
    """Rewrite hrefs that point at another PRD/TRD .md we've converted so they
    point at the sibling .html instead. Leaves every other link untouched."""

    src_dir = os.path.dirname(src_abs_path)

    def _sub(m):
        whole, target, anchor = m.group(1), m.group(2), m.group(3) or ""
        if not target.endswith(".md"):
            return whole
        if target.startswith("http://") or target.startswith("https://"):
            return whole
        candidate = os.path.normpath(os.path.join(src_dir, target))
        if candidate in ABS_MD:
            new_target = target[: -len(".md")] + ".html"
            return f'href="{new_target}{anchor}"'
        return whole

    return LINK_RE.sub(_sub, html_body)


CSS = """
:root {
  color-scheme: light dark;
  --bg: #ffffff;
  --fg: #1b1f23;
  --muted: #57606a;
  --border: #d0d7de;
  --code-bg: #f6f8fa;
  --link: #0969da;
  --accent: #f6f8fa;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117;
    --fg: #e6edf3;
    --muted: #9198a1;
    --border: #30363d;
    --code-bg: #161b22;
    --link: #4493f8;
    --accent: #161b22;
  }
}
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--fg);
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.6;
  font-size: 16px;
  padding: 2.5rem 1.25rem 5rem;
}
.doc {
  max-width: 780px;
  margin: 0 auto;
}
.source-note {
  font-size: 0.8rem;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}
.source-note code {
  background: var(--code-bg);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
}
h1, h2, h3, h4 { line-height: 1.3; }
h1 { font-size: 1.85rem; margin-top: 0; }
h2 {
  font-size: 1.4rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.3rem;
  margin-top: 2.2rem;
}
h3 { font-size: 1.15rem; margin-top: 1.6rem; }
h4 { font-size: 1rem; margin-top: 1.2rem; }
p, ul, ol, table { margin-top: 0.6rem; margin-bottom: 0.9rem; }
ul, ol { padding-left: 1.5rem; }
li { margin: 0.25rem 0; }
li > ul, li > ol { margin: 0.25rem 0; }
a { color: var(--link); }
code {
  background: var(--code-bg);
  padding: 0.1rem 0.35rem;
  border-radius: 4px;
  font-size: 0.9em;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
pre {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.9rem 1rem;
  overflow-x: auto;
}
pre code { background: none; padding: 0; }
blockquote {
  margin: 0.9rem 0;
  padding: 0.2rem 1rem;
  border-left: 3px solid var(--border);
  color: var(--muted);
}
table {
  border-collapse: collapse;
  width: 100%;
  display: block;
  overflow-x: auto;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.7rem;
  text-align: left;
  vertical-align: top;
}
th { background: var(--accent); }
hr { border: none; border-top: 1px solid var(--border); margin: 2rem 0; }
del { color: var(--muted); }
strong { font-weight: 600; }
"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="doc">
<div class="source-note">Rendered from <code>{relpath}</code> — source of truth is the markdown file; this HTML copy is generated for easy reading.</div>
{body}
</div>
</body>
</html>
"""


def first_h1(md_text):
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Passenger doc"


def convert(relpath):
    src_abs = os.path.normpath(os.path.join(ROOT, relpath))
    with open(src_abs, "r", encoding="utf-8") as f:
        raw = f.read()

    title = first_h1(raw)
    text = strikethrough(raw)
    text = checkbox_lists(text)

    body_html = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"],
    )
    body_html = rewrite_links(body_html, src_abs)

    out_html = TEMPLATE.format(
        title=html.escape(title),
        css=CSS,
        relpath=relpath,
        body=body_html,
    )

    out_path = src_abs[: -len(".md")] + ".html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out_html)
    return out_path


def main():
    written = []
    for rel in FILES:
        out = convert(rel)
        written.append(out)
        print(out)
    print(f"\n{len(written)} files written.")


if __name__ == "__main__":
    main()
