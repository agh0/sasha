#!/usr/bin/env python3
"""Convert a Markdown file to a minimal HTML5 document.

Output uses a strict tag whitelist with no CSS, classes, ids, scripts or
wrapper divs. Designed for Google Docs Markdown exports.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import markdown  # type: ignore
    import bleach  # type: ignore
except ImportError as exc:
    sys.stderr.write(
        f"missing dependency: {exc.name}\n"
        "install with: pip install markdown bleach\n"
    )
    sys.exit(2)


ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p",
    "strong", "em", "code",
    "a", "img",
    "ul", "ol", "li",
    "blockquote",
    "pre",
    "hr",
    "table", "thead", "tbody", "tr", "th", "td",
    "br",
]

ALLOWED_ATTRS = {
    "a": ["href"],
    "img": ["src", "alt"],
}


def detect_lang(text: str) -> str:
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return "en"
    cyrillic = sum(1 for c in letters if "Ѐ" <= c <= "ӿ")
    return "ru" if cyrillic / len(letters) > 0.3 else "en"


def extract_title(html: str, fallback: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    if not match:
        return fallback
    text = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return text or fallback


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def convert(md_text: str, title_fallback: str) -> str:
    body_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code"],
        output_format="html5",
    )
    sanitized = bleach.clean(
        body_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
        strip_comments=True,
    )
    title = extract_title(sanitized, title_fallback)
    lang = detect_lang(md_text)
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{lang}">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{html_escape(title)}</title>\n"
        "</head>\n"
        "<body>\n"
        f"{sanitized}\n"
        "</body>\n"
        "</html>\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown to minimal HTML5")
    parser.add_argument("input", nargs="?", help="path to .md file")
    parser.add_argument("output", nargs="?", help="path to .html file (optional)")
    parser.add_argument("--stdin", action="store_true", help="read Markdown from stdin, print HTML to stdout")
    args = parser.parse_args()

    if args.stdin:
        md_text = sys.stdin.read()
        sys.stdout.write(convert(md_text, title_fallback="document"))
        return 0

    if not args.input:
        parser.error("input file is required (or use --stdin)")

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.is_file():
        sys.stderr.write(f"input file not found: {in_path}\n")
        return 1

    md_text = in_path.read_text(encoding="utf-8")
    html = convert(md_text, title_fallback=in_path.stem)

    out_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else in_path.with_suffix(".html")
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
