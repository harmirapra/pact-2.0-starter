#!/usr/bin/env python3
"""Convert a documented subset of Markdown to a self-contained HTML file.

Zero external dependencies — Python 3 standard library only.

Anything the converter does not understand is reported on stderr instead of
being silently mangled. See SUPPORTED / NOT SUPPORTED in the skill's SKILL.md.
"""

import argparse
import html
import os
import re
import sys
from datetime import date

MARKERS = {
    "NEW": ("new", "NOVÝ TEXT"),
    "UPDATE": ("updated", "AKTUALIZOVÁNO"),
    "DELETE": ("deleted", "SMAZÁNO"),
    "NOTE": ("note", "POZNÁMKA"),
    "ORIGINAL": ("original", "PŮVODNÍ TEXT"),
}

BLOCK_MARKER_RE = re.compile(
    r"^[ \t]*\{(" + "|".join(MARKERS) + r")\}[ \t]*\n?(.*?)\n?[ \t]*\{/\1\}[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
INLINE_MARKER_RE = re.compile(r"\{(" + "|".join(MARKERS) + r")\}(.*?)\{/\1\}")

SETEXT_RE = re.compile(r"^(=+|-+)\s*$")
REF_LINK_RE = re.compile(r"\[[^\]]+\]\[[^\]]*\]")
FOOTNOTE_RE = re.compile(r"\[\^[^\]]+\]")
RAW_HTML_RE = re.compile(r"^\s*<[a-zA-Z/!][^>]*>")


class Warnings:
    """Collects everything the converter could not handle."""

    def __init__(self):
        self.items = []

    def add(self, line_no, text, detail):
        self.items.append((line_no, text.strip()[:70], detail))

    def report(self, stream=sys.stderr):
        if not self.items:
            return
        stream.write("\nNepřevedeno nebo převedeno doslovně:\n")
        for line_no, text, detail in self.items:
            stream.write("  řádek %-5d %-28s %s\n" % (line_no, detail, text))
        stream.write(
            "\nCelkem %d míst. Zkontroluj je ve výstupu.\n" % len(self.items)
        )


# --------------------------------------------------------------------------
# Inline
# --------------------------------------------------------------------------

def inline(text, warns, line_no):
    """Convert inline Markdown inside an already-selected block of text."""
    if REF_LINK_RE.search(text):
        warns.add(line_no, text, "odkaz přes referenci")
    if FOOTNOTE_RE.search(text):
        warns.add(line_no, text, "poznámka pod čarou")

    code_spans = []

    def stash_code(match):
        code_spans.append(html.escape(match.group(1)))
        return "\x00CODE%d\x00" % (len(code_spans) - 1)

    text = re.sub(r"`([^`]+)`", stash_code, text)
    text = html.escape(text)

    def image(match):
        alt, src = match.group(1), match.group(2)
        if not src.startswith("data:"):
            warns.add(line_no, src, "externí obrázek")
        return '<img src="%s" alt="%s">' % (src, alt)

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_([^_\n]+?)_(?![\w_])", r"<em>\1</em>", text)
    text = re.sub(r"~~(.+?)~~", r"<del>\1</del>", text)

    def inline_marker(match):
        css, label = MARKERS[match.group(1)]
        return '<span class="i-%s" title="%s">%s</span>' % (css, label, match.group(2))

    text = INLINE_MARKER_RE.sub(inline_marker, text)

    for index, code in enumerate(code_spans):
        text = text.replace("\x00CODE%d\x00" % index, "<code>%s</code>" % code)
    return text


# --------------------------------------------------------------------------
# Blocks
# --------------------------------------------------------------------------

def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^a-z0-9à-ſ]+", "-", text)
    return text.strip("-") or "sekce"


class Converter:
    def __init__(self, warns):
        self.warns = warns
        self.toc = []

    def convert(self, text):
        text, marker_blocks = self._extract_block_markers(text)
        body = self._blocks(text.split("\n"), offset=0)
        for token, (kind, inner) in marker_blocks.items():
            css, label = MARKERS[kind]
            sub = Converter(self.warns)
            rendered = sub.convert(inner)[0]
            body = body.replace(
                "<p>%s</p>" % token,
                '<div class="%s"><span class="tag">%s</span>\n%s</div>'
                % (css, label, rendered),
            )
        return body, self.toc

    def _extract_block_markers(self, text):
        found = {}

        def replace(match):
            token = "\x00MARK%d\x00" % len(found)
            found[token] = (match.group(1), match.group(2))
            return "\n%s\n" % token

        return BLOCK_MARKER_RE.sub(replace, text), found

    # -- main block loop ---------------------------------------------------

    def _blocks(self, lines, offset):
        out = []
        i = 0
        while i < len(lines):
            raw = lines[i]
            line_no = offset + i + 1
            stripped = raw.strip()

            if not stripped:
                i += 1
                continue

            if stripped.startswith("```") or stripped.startswith("~~~"):
                i = self._code_fence(lines, i, out)
                continue

            if re.match(r"^(\*\s*){3,}$|^(-\s*){3,}$|^(_\s*){3,}$", stripped):
                out.append("<hr>")
                i += 1
                continue

            heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
            if heading:
                level = len(heading.group(1))
                content = inline(heading.group(2).strip(), self.warns, line_no)
                anchor = slugify(content)
                if level <= 3:
                    self.toc.append((level, anchor, content))
                out.append('<h%d id="%s">%s</h%d>' % (level, anchor, content, level))
                i += 1
                continue

            if (
                i + 1 < len(lines)
                and SETEXT_RE.match(lines[i + 1].strip())
                and not stripped.startswith(">")
            ):
                self.warns.add(line_no, raw, "podtržený nadpis")

            if stripped.startswith(">"):
                i = self._quote(lines, i, out, offset)
                continue

            if "|" in stripped and self._is_table(lines, i):
                i = self._table(lines, i, out, offset)
                continue

            if re.match(r"^([-*+]|\d+[.)])\s+", stripped):
                i = self._list(lines, i, out, offset)
                continue

            if RAW_HTML_RE.match(raw):
                self.warns.add(line_no, raw, "vložené HTML")
                out.append(raw)
                i += 1
                continue

            i = self._paragraph(lines, i, out, offset)
        return "\n".join(out)

    def _code_fence(self, lines, i, out):
        fence = lines[i].strip()[:3]
        lang = lines[i].strip()[3:].strip()
        body = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith(fence):
            body.append(lines[i])
            i += 1
        i += 1  # closing fence
        cls = ' class="lang-%s"' % html.escape(lang) if lang else ""
        out.append(
            "<pre><code%s>%s</code></pre>" % (cls, html.escape("\n".join(body)))
        )
        return i

    def _quote(self, lines, i, out, offset):
        body = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            body.append(re.sub(r"^\s*>\s?", "", lines[i]))
            i += 1
        sub = Converter(self.warns)
        out.append("<blockquote>%s</blockquote>" % sub._blocks(body, offset + i))
        return i

    def _is_table(self, lines, i):
        return (
            i + 1 < len(lines)
            and "|" in lines[i]
            and re.match(r"^[\s|:\-]+$", lines[i + 1].strip())
            and "-" in lines[i + 1]
        )

    def _table(self, lines, i, out, offset):
        def cells(row):
            row = row.strip()
            if row.startswith("|"):
                row = row[1:]
            if row.endswith("|"):
                row = row[:-1]
            return [c.strip() for c in row.split("|")]

        header = cells(lines[i])
        aligns = []
        for spec in cells(lines[i + 1]):
            left, right = spec.startswith(":"), spec.endswith(":")
            aligns.append(
                "center" if left and right else "right" if right else "left"
            )
        i += 2

        rows = []
        while i < len(lines) and "|" in lines[i] and lines[i].strip():
            rows.append(cells(lines[i]))
            i += 1

        def cell(tag, value, index):
            align = aligns[index] if index < len(aligns) else "left"
            return '<%s style="text-align:%s">%s</%s>' % (
                tag,
                align,
                inline(value, self.warns, offset + i),
                tag,
            )

        parts = ['<div class="table-wrap"><table>', "<thead><tr>"]
        parts += [cell("th", value, n) for n, value in enumerate(header)]
        parts.append("</tr></thead><tbody>")
        for row in rows:
            parts.append("<tr>")
            parts += [cell("td", value, n) for n, value in enumerate(row)]
            parts.append("</tr>")
        parts.append("</tbody></table></div>")
        out.append("".join(parts))
        return i

    def _list(self, lines, i, out, offset):
        items = []  # (indent, ordered, html)
        while i < len(lines):
            raw = lines[i]
            if not raw.strip():
                if i + 1 < len(lines) and re.match(
                    r"^\s*([-*+]|\d+[.)])\s+", lines[i + 1]
                ):
                    i += 1
                    continue
                break
            match = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", raw)
            if not match:
                if items:
                    items[-1] = (
                        items[-1][0],
                        items[-1][1],
                        items[-1][2] + " " + inline(raw.strip(), self.warns, offset + i),
                    )
                    i += 1
                    continue
                break
            indent = len(match.group(1).expandtabs(4))
            ordered = not match.group(2) in ("-", "*", "+")
            content = match.group(3)
            task = re.match(r"^\[([ xX])\]\s+(.*)$", content)
            if task:
                checked = " checked" if task.group(1).lower() == "x" else ""
                content = (
                    '<input type="checkbox" disabled%s> %s'
                    % (checked, inline(task.group(2), self.warns, offset + i))
                )
            else:
                content = inline(content, self.warns, offset + i)
            items.append((indent, ordered, content))
            i += 1

        # A blank line may separate two lists of different kinds; render each.
        index = 0
        while index < len(items):
            rendered, index = self._render_list(items, index, items[index][0])
            out.append(rendered)
        return i

    def _render_list(self, items, index, indent):
        """Render items[index:] as one list; returns (html, next index)."""
        ordered = items[index][1]
        parts = ["<ol>" if ordered else "<ul>"]
        has_item = False
        while index < len(items):
            item_indent, item_ordered, content = items[index]
            if item_indent < indent:
                break
            if item_indent > indent:
                nested, index = self._render_list(items, index, item_indent)
                if has_item:
                    parts[-1] = parts[-1][: -len("</li>")] + nested + "</li>"
                else:
                    parts.append("<li>%s</li>" % nested)
                    has_item = True
                continue
            if item_ordered != ordered:
                break
            parts.append("<li>%s</li>" % content)
            has_item = True
            index += 1
        parts.append("</ol>" if ordered else "</ul>")
        return "".join(parts), index

    def _paragraph(self, lines, i, out, offset):
        body = []
        start = i
        while i < len(lines) and lines[i].strip():
            stripped = lines[i].strip()
            if i > start and (
                stripped.startswith("#")
                or stripped.startswith(">")
                or stripped.startswith("```")
                or re.match(r"^([-*+]|\d+[.)])\s+", stripped)
            ):
                break
            body.append(stripped)
            i += 1
        text = " ".join(body)
        if text.startswith("\x00MARK"):
            out.append("<p>%s</p>" % text)
        else:
            out.append("<p>%s</p>" % inline(text, self.warns, offset + start + 1))
        return i


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------

def stylesheet(style):
    font = (
        "Georgia, 'Iowan Old Style', 'Times New Roman', serif"
        if style == "book"
        else "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    )
    return """
:root {
  --bg: #ffffff; --fg: #1a1a1a; --muted: #666; --rule: #e0e0e0;
  --code-bg: #f5f5f5; --accent: #2563eb;
  --new-bg: #fce4ec; --new-fg: #c2185b;
  --upd-bg: #fff3e0; --upd-fg: #e65100;
  --note-bg: #e3f2fd; --note-fg: #1565c0;
  --del-bg: #f5f5f5; --del-fg: #9e9e9e;
  --orig-bg: #f5f5f5; --orig-fg: #666;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #17181a; --fg: #e6e6e6; --muted: #9aa0a6; --rule: #33363a;
    --code-bg: #232528; --accent: #7aa2f7;
    --new-bg: #3a1f2a; --new-fg: #f48fb1;
    --upd-bg: #3a2c17; --upd-fg: #ffb74d;
    --note-bg: #17293d; --note-fg: #82b1ff;
    --del-bg: #232528; --del-fg: #7c8085;
    --orig-bg: #232528; --orig-fg: #9aa0a6;
  }
}
* { box-sizing: border-box; }
body {
  font-family: %(font)s;
  line-height: 1.7; max-width: 46rem; margin: 0 auto; padding: 3rem 1.25rem 6rem;
  color: var(--fg); background: var(--bg);
  -webkit-text-size-adjust: 100%%;
}
header { border-bottom: 2px solid var(--rule); margin-bottom: 2.5rem; padding-bottom: 1rem; }
h1 { font-size: 2.1rem; line-height: 1.25; margin: 0 0 .5rem; }
h2 { font-size: 1.5rem; margin: 2.5rem 0 .75rem; padding-bottom: .3rem; border-bottom: 1px solid var(--rule); }
h3 { font-size: 1.2rem; margin: 2rem 0 .5rem; }
h4, h5, h6 { font-size: 1.05rem; margin: 1.5rem 0 .5rem; }
p { margin: 0 0 1.1rem; }
.meta { color: var(--muted); font-size: .9rem; }
a { color: var(--accent); }
img { max-width: 100%%; height: auto; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2.5rem 0; }
ul, ol { margin: 0 0 1.1rem; padding-left: 1.5rem; }
li { margin: .3rem 0; }
li > ul, li > ol { margin: .3rem 0; }
blockquote {
  margin: 1.2rem 0; padding: .1rem 1.1rem; border-left: 3px solid var(--rule);
  color: var(--muted);
}
code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .88em;
  background: var(--code-bg); padding: .12em .35em; border-radius: 3px;
}
pre {
  background: var(--code-bg); padding: 1rem; border-radius: 6px;
  overflow-x: auto; margin: 0 0 1.2rem;
}
pre code { background: none; padding: 0; font-size: .85rem; }
.table-wrap { overflow-x: auto; margin: 0 0 1.3rem; }
table { border-collapse: collapse; width: 100%%; font-size: .95rem; }
th, td { border: 1px solid var(--rule); padding: .5rem .7rem; vertical-align: top; }
th { background: var(--code-bg); font-weight: 600; }
nav.toc {
  background: var(--code-bg); border-radius: 6px; padding: 1rem 1.25rem; margin-bottom: 2.5rem;
  font-size: .92rem;
}
nav.toc p { font-weight: 600; margin: 0 0 .5rem; }
nav.toc ul { list-style: none; padding-left: 0; margin: 0; }
nav.toc li.lvl-2 { padding-left: 1rem; }
nav.toc li.lvl-3 { padding-left: 2rem; }
.new, .updated, .note, .deleted, .original {
  padding: .9rem 1.1rem; margin: 1.3rem 0; border-radius: 0 6px 6px 0;
  border-left: 4px solid;
}
.new     { background: var(--new-bg);  border-color: var(--new-fg); }
.updated { background: var(--upd-bg);  border-color: var(--upd-fg); }
.note    { background: var(--note-bg); border-color: var(--note-fg); font-style: italic; }
.deleted { background: var(--del-bg);  border-color: var(--del-fg); color: var(--del-fg); text-decoration: line-through; }
.original{ background: var(--orig-bg); border-color: var(--orig-fg); color: var(--orig-fg); font-size: .93rem; }
.tag { display: block; font-weight: 600; font-size: .74rem; letter-spacing: .06em; margin-bottom: .5rem; }
.new .tag { color: var(--new-fg); }
.updated .tag { color: var(--upd-fg); }
.note .tag { color: var(--note-fg); }
.deleted .tag, .original .tag { color: var(--del-fg); }
.new > :last-child, .updated > :last-child, .note > :last-child,
.deleted > :last-child, .original > :last-child { margin-bottom: 0; }
.i-new { background: var(--new-bg); }
.i-updated { background: var(--upd-bg); }
.i-note { background: var(--note-bg); }
.i-deleted { text-decoration: line-through; color: var(--del-fg); }
.i-original { color: var(--orig-fg); }
footer { margin-top: 4rem; padding-top: 1rem; border-top: 1px solid var(--rule);
         color: var(--muted); font-size: .85rem; }
@media print {
  body { max-width: none; padding: 0; color: #000; background: #fff; }
  nav.toc { break-inside: avoid; }
  .new, .updated, .note, .deleted, .original, pre, table { break-inside: avoid; }
  a { color: #000; text-decoration: underline; }
}
""" % {"font": font}


def render_toc(entries):
    if len(entries) < 3:
        return ""
    parts = ['<nav class="toc"><p>Obsah</p><ul>']
    for level, anchor, text in entries:
        parts.append('<li class="lvl-%d"><a href="#%s">%s</a></li>' % (level, anchor, text))
    parts.append("</ul></nav>")
    return "".join(parts)


def build_page(markdown_text, title, style, warns):
    converter = Converter(warns)
    body, toc = converter.convert(markdown_text)

    if not title:
        first = re.search(r"^#\s+(.+)$", markdown_text, re.MULTILINE)
        title = re.sub(r"[*_`]", "", first.group(1)).strip() if first else "Dokument"

    used = {css for css, _ in MARKERS.values() if 'class="%s"' % css in body}
    legend = ""
    if used:
        names = {
            "new": "nový text",
            "updated": "aktualizováno",
            "deleted": "smazáno",
            "note": "poznámka",
            "original": "původní text",
        }
        items = "".join(
            '<li><span class="tag %s">■</span> %s</li>' % (css, names[css])
            for css in ["new", "updated", "deleted", "note", "original"]
            if css in used
        )
        legend = (
            '<nav class="toc"><p>Vysvětlivky</p><ul style="list-style:none">%s</ul></nav>'
            % items
        )

    return (
        "<!DOCTYPE html>\n"
        '<html lang="cs">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>%(title)s</title>\n<style>%(css)s</style>\n</head>\n<body>\n"
        "<header><h1>%(title)s</h1>"
        '<div class="meta">%(date)s</div></header>\n'
        "%(legend)s%(toc)s\n<main>\n%(body)s\n</main>\n"
        '<footer>Vygenerováno z Markdownu nástrojem md2html.py.</footer>\n'
        "</body>\n</html>\n"
    ) % {
        "title": html.escape(title),
        "css": stylesheet(style),
        "date": date.today().isoformat(),
        "legend": legend,
        "toc": render_toc(toc),
        "body": body,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Převede Markdown na samostatný HTML soubor."
    )
    parser.add_argument("input", help="vstupní .md soubor (nebo - pro stdin)")
    parser.add_argument("-o", "--output", help="výstupní .html (výchozí: vedle vstupu)")
    parser.add_argument(
        "--style", choices=["modern", "book"], default="modern", help="vzhled"
    )
    parser.add_argument("--title", help="titulek stránky (jinak první nadpis H1)")
    args = parser.parse_args(argv)

    if args.input == "-":
        text = sys.stdin.read()
        default_out = "vystup.html"
    else:
        if not os.path.exists(args.input):
            sys.stderr.write("Vstupní soubor neexistuje: %s\n" % args.input)
            return 1
        with open(args.input, encoding="utf-8") as handle:
            text = handle.read()
        default_out = os.path.splitext(args.input)[0] + ".html"

    warns = Warnings()
    page = build_page(text, args.title, args.style, warns)

    output = args.output or default_out
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(page)

    sys.stderr.write("Hotovo: %s\n" % output)
    warns.report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
