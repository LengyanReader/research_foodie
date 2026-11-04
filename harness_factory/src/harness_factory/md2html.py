"""Minimal Markdown → HTML converter (P65-ext, stdlib only).

Handles the subset of Markdown used in ``review/`` documents: headers,
bold/italic, inline code, fenced code blocks, pipe tables, unordered and
ordered lists, blockquotes, horizontal rules, links, and paragraphs.
No images, footnotes, or HTML passthrough — the review corpus doesn't use them.
"""

from __future__ import annotations

import re
from typing import List, Tuple

# ---------------------------------------------------------------- inline

def _inline(text: str) -> str:
    """Convert inline Markdown (bold, italic, code, links) to HTML."""
    # inline code first (protect from other replacements)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # italic
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    # links [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


# ---------------------------------------------------------------- block level

def convert(md: str) -> str:
    """Convert Markdown text to an HTML fragment (no <html>/<body> wrapper)."""
    lines = md.splitlines()
    out: List[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # --- fenced code block ---
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

        # --- table ---
        if line.strip().startswith("|") and i + 1 < n and _is_table_sep(lines[i + 1]):
            out.append('<table class="mdtable">')
            # header row
            cells = _split_row(line)
            out.append("<thead><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells) + "</tr></thead>")
            i += 2  # skip separator
            out.append("<tbody>")
            while i < n and lines[i].strip().startswith("|"):
                cells = _split_row(lines[i])
                out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        # --- headings ---
        hm = re.match(r"^(#{1,6})\s+(.*)", line)
        if hm:
            level = len(hm.group(1))
            out.append(f"<h{level}>{_inline(hm.group(2))}</h{level}>")
            i += 1
            continue

        # --- horizontal rule ---
        if re.match(r"^-{3,}\s*$", line) or re.match(r"^\*{3,}\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # --- blockquote ---
        if line.strip().startswith(">"):
            out.append("<blockquote>")
            while i < n and lines[i].strip().startswith(">"):
                out.append(f"<p>{_inline(lines[i].lstrip('> ').strip())}</p>")
                i += 1
            out.append("</blockquote>")
            continue

        # --- unordered list ---
        if re.match(r"^\s*[-*]\s+", line):
            out.append("<ul>")
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i])
                out.append(f"<li>{_inline(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        # --- ordered list ---
        if re.match(r"^\s*\d+\.\s+", line):
            out.append("<ol>")
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                out.append(f"<li>{_inline(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        # --- blank line ---
        if not line.strip():
            i += 1
            continue

        # --- paragraph (accumulate until blank line or block start) ---
        para: List[str] = []
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("#", "```", "|", ">", "-", "*")) \
                and not re.match(r"^\s*\d+\.\s+", lines[i]) and not re.match(r"^-{3,}\s*$", lines[i]):
            para.append(lines[i])
            i += 1
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
        else:
            i += 1  # safety: skip unrecognized line

    return "\n".join(out)


# ---------------------------------------------------------------- helpers

def _esc_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|[\s:|-]+\|\s*$", line))


def _split_row(line: str) -> List[str]:
    parts = line.strip().strip("|").split("|")
    return [c.strip() for c in parts]


# ---------------------------------------------------------------- page wrapper

_CSS = """
:root{--ink:#16202b;--mut:#65788f;--line:#e4eaf1;--bg:#f6f8fb;--card:#fff;--brand:#0b5cad}
*{box-sizing:border-box}
body{font-family:system-ui,'Segoe UI','Helvetica Neue','Noto Sans SC',sans-serif;margin:0;color:var(--ink);background:var(--bg);line-height:1.65}
.wrap{max-width:860px;margin:0 auto;padding:28px 20px 64px}
h1{font-size:22px;border-bottom:2px solid var(--brand);padding-bottom:10px;margin:24px 0 16px}
h2{font-size:17px;margin:28px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line)}
h3{font-size:15px;margin:20px 0 6px}
p{margin:8px 0}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
code{background:#eef2f7;border-radius:4px;padding:1px 5px;font-size:0.9em;font-family:'Cascadia Code',monospace}
pre{background:#1a2332;color:#d4d4d4;border-radius:8px;padding:14px 16px;overflow-x:auto;line-height:1.45}
pre code{background:none;padding:0;color:inherit}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13.5px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f0f4f8;font-weight:600}
blockquote{border-left:3px solid var(--brand);margin:12px 0;padding:6px 16px;background:#f0f4f8;border-radius:0 8px 8px 0}
blockquote p{margin:4px 0}
hr{border:none;border-top:1px solid var(--line);margin:24px 0}
ul,ol{padding-left:24px;margin:8px 0}
li{margin:4px 0}
.nav{display:flex;gap:14px;padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:20px;flex-wrap:wrap}
.nav a{font-size:13px;color:var(--brand);text-decoration:none}
.nav a:hover{text-decoration:underline}
.meta{font-size:12px;color:var(--mut);margin-bottom:16px}
"""


def render_page(title: str, body_html: str, nav_links: List[Tuple[str, str]] | None = None) -> str:
    """Wrap converted body HTML in a styled standalone page."""
    nav = ""
    if nav_links:
        items = "".join(f'<a href="{href}">{label}</a>' for label, href in nav_links)
        nav = f'<nav class="nav">{items}</nav>'
    return f'''<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale-1">
<title>{title}</title><style>{_CSS}</style></head><body>
<div class="wrap">{nav}<div class="meta">Generated by harness-factory · docs/ · self-contained · <b>SSOT: review/ 的 .md 文件是唯一可编辑源；本页面为派生视图，请勿直接编辑。更新流程：编辑 .md → harness pages --write → 本页自动重生成。</b></div>
{body_html}
</div></body></html>'''
