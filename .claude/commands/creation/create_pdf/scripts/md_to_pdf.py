#!/usr/bin/env python3
"""Convert Markdown files to PDF using LibreOffice headless (no external pip deps required)."""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


# ---------------------------------------------------------------------------
# Minimal Markdown → HTML converter (handles common constructs)
# ---------------------------------------------------------------------------

def md_to_html(text: str) -> str:
    lines = text.split("\n")
    html_lines = []
    in_code_block = False
    in_ul = False
    in_ol = False
    in_table = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    def close_table():
        nonlocal in_table
        if in_table:
            html_lines.append("</tbody></table>")
            in_table = False

    def inline(s: str) -> str:
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
        return s

    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if line.strip().startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                close_lists()
                close_table()
                html_lines.append("<pre><code>")
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            html_lines.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            i += 1
            continue

        # Table rows (lines starting with |)
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # Separator row (e.g. |---|---|)
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                i += 1
                continue
            if not in_table:
                close_lists()
                html_lines.append('<table border="1" cellpadding="4" cellspacing="0">')
                html_lines.append("<tbody>")
                in_table = True
            tag = "th" if not in_table or html_lines[-3:] == [] else "td"
            # Use th for first row, td for rest — detect by checking previous row existence
            row_html = "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>"
            html_lines.append(row_html)
            i += 1
            continue
        else:
            close_table()

        # ATX headings
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            close_lists()
            level = len(m.group(1))
            html_lines.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Unordered list
        m = re.match(r"^[-*+]\s+(.*)", line)
        if m:
            if not in_ul:
                close_lists()
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        # Ordered list
        m = re.match(r"^\d+\.\s+(.*)", line)
        if m:
            if not in_ol:
                close_lists()
                html_lines.append("<ol>")
                in_ol = True
            html_lines.append(f"<li>{inline(m.group(1))}</li>")
            i += 1
            continue

        # Blank line
        if line.strip() == "":
            close_lists()
            html_lines.append("")
            i += 1
            continue

        # Plain paragraph
        close_lists()
        html_lines.append(f"<p>{inline(line)}</p>")
        i += 1

    close_lists()
    close_table()

    body = "\n".join(html_lines)
    return (
        "<!DOCTYPE html><html><head>"
        '<meta charset="utf-8">'
        "<style>"
        "body{font-family:sans-serif;max-width:800px;margin:40px auto;font-size:14px;line-height:1.6}"
        "h1,h2,h3{border-bottom:1px solid #ccc;padding-bottom:4px}"
        "pre{background:#f4f4f4;padding:12px;border-radius:4px;overflow-x:auto}"
        "code{background:#f4f4f4;padding:2px 4px;border-radius:3px}"
        "table{border-collapse:collapse;width:100%}"
        "td,th{border:1px solid #ccc;padding:6px 10px}"
        "</style>"
        f"</head><body>{body}</body></html>"
    )


# ---------------------------------------------------------------------------
# Conversion pipeline
# ---------------------------------------------------------------------------

def convert(input_dir: Path, output_dir: Path) -> None:
    md_files = list(input_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in '{input_dir}'.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    converted, failed = [], []

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for md_file in md_files:
            html_file = tmp_path / md_file.with_suffix(".html").name
            html_file.write_text(md_to_html(md_file.read_text(encoding="utf-8")), encoding="utf-8")

            result = subprocess.run(
                [
                    "libreoffice", "--headless", "--convert-to", "pdf",
                    "--outdir", str(output_dir), str(html_file),
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                converted.append(md_file.name)
            else:
                failed.append((md_file.name, result.stderr.strip() or result.stdout.strip()))

    print(f"Converted: {len(converted)}/{len(md_files)}")
    for name in converted:
        pdf_name = Path(name).with_suffix(".pdf").name
        print(f"  OK   {name} -> {output_dir / pdf_name}")
    for name, err in failed:
        print(f"  FAIL {name}: {err}", file=sys.stderr)

    if failed:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF via LibreOffice.")
    parser.add_argument("--input-dir", default="markdown", help="Directory with .md files (default: markdown)")
    parser.add_argument("--output-dir", default="pdf", help="Output directory for .pdf files (default: pdf)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"Error: input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    convert(input_dir, Path(args.output_dir))


if __name__ == "__main__":
    main()
