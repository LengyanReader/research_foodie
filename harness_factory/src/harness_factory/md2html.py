"""Minimal Markdown → HTML converter + documentation page renderer (P65-ext).

Handles the Markdown subset used in ``review/`` documents. The page template
follows a documentation-site layout: TOC sidebar on desktop, collapsible on
mobile, with prev/next navigation, proper typography, and clean tables.
"""

from __future__ import annotations

import re
from typing import List, Tuple


def _inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _esc_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff-]", "-", text.strip().lower()).strip("-")[:64] or "sec"


def convert(md: str) -> Tuple[str, List[Tuple[int, str, str]]]:
    """Convert Markdown → (HTML fragment, TOC entries [(level, slug, title)])."""
    lines = md.splitlines()
    out: List[str] = []
    toc: List[Tuple[int, str, str]] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            out.append("<pre><code>" if not lang else f'<pre><code class="lang-{lang}">')
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                out.append(_esc_html(lines[i]))
                i += 1
            out.append("</code></pre>")
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < n and _is_sep(lines[i + 1]):
            out.append('<div class="tblwrap"><table>')
            cells = _cells(line)
            out.append("<thead><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells) + "</tr></thead>")
            i += 2
            out.append("<tbody>")
            while i < n and lines[i].strip().startswith("|"):
                cells = _cells(lines[i])
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table></div>")
            continue
        hm = re.match(r"^(#{1,4})\s+(.*)", line)
        if hm:
            level = len(hm.group(1))
            title = hm.group(2).strip()
            if level >= 2:
                slug = _slug(title)
                toc.append((level, slug, title))
                out.append(f'<h{level} id="{slug}">{_inline(title)}</h{level}>')
            else:
                out.append(f"<h1>{_inline(title)}</h1>")
            i += 1
            continue
        if re.match(r"^-{3,}\s*$", line) or re.match(r"^\*{3,}\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.strip().startswith(">"):
            out.append("<blockquote>")
            while i < n and lines[i].strip().startswith(">"):
                txt = lines[i].lstrip("> ").strip()
                if txt:
                    out.append(f"<p>{_inline(txt)}</p>")
                i += 1
            out.append("</blockquote>")
            continue
        if re.match(r"^\s*[-*]\s+", line):
            out.append("<ul>")
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i])
                out.append(f"<li>{_inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            out.append("<ol>")
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                out.append(f"<li>{_inline(item)}</li>")
                i += 1
            out.append("</ol>")
            continue
        if not line.strip():
            i += 1
            continue
        para: List[str] = []
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("#", "```", "|", ">", "-", "*")) \
                and not re.match(r"^\s*\d+\.\s+", lines[i]) and not re.match(r"^-{3,}\s*$", lines[i]):
            para.append(lines[i])
            i += 1
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
        else:
            i += 1
    return "\n".join(out), toc


def _is_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", line))


def _cells(line: str) -> List[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


_CSS = r"""
:root{--ink:#1a2332;--mut:#65788f;--line:#dde4ec;--bg:#f6f8fb;--card:#fff;--brand:#0b5cad;--accent:#7b5ea7;--code-bg:#f0f4f8;--pre-bg:#1a2332;--pre-fg:#d4d4d4;--sidebar-w:260px}
*{box-sizing:border-box}
body{font-family:system-ui,'Segoe UI','Helvetica Neue','Noto Sans SC',sans-serif;margin:0;color:var(--ink);background:var(--bg);line-height:1.75;font-size:15.5px}
.wrap{display:flex;max-width:1200px;margin:0 auto;min-height:100vh}
.sidebar{width:var(--sidebar-w);min-width:var(--sidebar-w);background:var(--sidebar-bg);border-right:1px solid var(--line);padding:24px 16px;position:sticky;top:0;height:100vh;overflow-y:auto;font-size:13px}
.sidebar h3{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:16px 0 6px}
.sidebar a{display:block;color:var(--ink);text-decoration:none;padding:3px 8px;border-radius:4px;margin:1px 0;line-height:1.4}
.sidebar a:hover{background:#eef2f7;color:var(--brand)}
.sidebar a.lvl3{padding-left:20px;font-size:12.5px;color:var(--mut)}
.sidebar a.active{color:var(--brand);font-weight:600;background:#e8f0fa}
.content{flex:1;padding:32px 40px 64px;max-width:780px;min-width:0}
.doc-header{border-bottom:2px solid var(--brand);padding-bottom:14px;margin-bottom:24px}
.doc-header h1{font-size:22px;margin:0 0 4px;line-height:1.3}
.doc-header .meta{font-size:12px;color:var(--mut);margin-top:4px}
.back-nav{display:flex;gap:14px;padding:10px 0;margin-bottom:16px;flex-wrap:wrap;border-bottom:1px solid var(--line)}
.back-nav a{font-size:13px;color:var(--brand);text-decoration:none}
.back-nav a:hover{text-decoration:underline}
h1{font-size:22px;line-height:1.3;margin:20px 0 12px}
h2{font-size:18px;margin:32px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:15.5px;margin:20px 0 6px}
p{margin:10px 0}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
code{background:var(--code-bg);border-radius:4px;padding:1px 5px;font-size:.88em;font-family:'Cascadia Code','SF Mono',monospace}
pre{background:var(--pre-bg);color:var(--pre-fg);border-radius:8px;padding:16px 18px;overflow-x:auto;line-height:1.5;font-size:13.5px;margin:14px 0}
pre code{background:none;padding:0;color:inherit}
.tblwrap{overflow-x:auto;margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{border:1px solid var(--line);padding:8px 12px;text-align:left;vertical-align:top}
th{background:#f0f4f8;font-weight:600}
tbody tr:nth-child(even){background:#fafbfc}
blockquote{border-left:3px solid var(--brand);margin:14px 0;padding:10px 18px;background:#f0f4f8;border-radius:0 8px 8px 0}
blockquote p{margin:6px 0}
hr{border:none;border-top:1px solid var(--line);margin:28px 0}
ul,ol{padding-left:24px;margin:10px 0}
li{margin:5px 0}
.prevnext{display:flex;justify-content:space-between;gap:12px;margin-top:40px;padding-top:16px;border-top:1px solid var(--line)}
.prevnext a{font-size:13px;color:var(--brand);text-decoration:none;padding:8px 14px;background:var(--card);border:1px solid var(--line);border-radius:8px}
.prevnext a:hover{background:#eef2f7}
@media(max-width:900px){.sidebar{display:none}.content{padding:20px 16px 48px}}
"""


def _build_toc(toc: List[Tuple[int, str, str]]) -> str:
    if not toc:
        return ""
    items = []
    for level, slug, title in toc:
        cls = f"lvl{level}" if level > 2 else ""
        items.append(f'<a href="#{slug}" class="{cls}">{_esc_html(title)}</a>')
    return "\n".join(items)


def render_page(
    title: str,
    body_html: str,
    toc: List[Tuple[int, str, str]] | None = None,
    nav_links: List[Tuple[str, str]] | None = None,
) -> str:
    """Wrap converted body in a documentation-site page with TOC sidebar."""
    toc_html = _build_toc(toc or [])
    sidebar = f'<div class="sidebar"><h3>On this page</h3>{toc_html}</div>' if toc_html else ""
    nav = ""
    if nav_links:
        items = "".join(f'<a href="{href}">{label}</a>' for label, href in nav_links)
        nav = f'<nav class="back-nav">{items}</nav>'
    return f'''<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_esc_html(title)}</title><style>{_CSS}</style></head><body>
<div class="wrap">{sidebar}
<div class="content">
{nav}
<div class="doc-header"><h1>{_esc_html(title)}</h1><div class="meta">Generated by harness-factory · docs/ · <b>SSOT: review/ 的 .md 文件是唯一可编辑源；本页面为派生视图。</b></div></div>
{body_html}
</div></div></body></html>'''
