#!/usr/bin/env python3
"""Convert Markdown files from an input directory to PDF files in an output directory."""

import argparse
import subprocess
import sys
from pathlib import Path


def convert(input_dir: Path, output_dir: Path) -> None:
    md_files = list(input_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in '{input_dir}'.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    converted, failed = [], []

    for md_file in md_files:
        pdf_file = output_dir / md_file.with_suffix(".pdf").name
        result = subprocess.run(
            ["pandoc", str(md_file), "-o", str(pdf_file)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            converted.append(md_file.name)
        else:
            failed.append((md_file.name, result.stderr.strip()))

    print(f"Converted: {len(converted)}/{len(md_files)}")
    for name in converted:
        print(f"  OK  {name} -> {output_dir / Path(name).with_suffix('.pdf').name}")
    for name, err in failed:
        print(f"  FAIL {name}: {err}", file=sys.stderr)

    if failed:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF using pandoc.")
    parser.add_argument("--input-dir", default="markdown", help="Directory containing .md files (default: markdown)")
    parser.add_argument("--output-dir", default="pdf", help="Directory for output .pdf files (default: pdf)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"Error: input directory '{input_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    convert(input_dir, Path(args.output_dir))


if __name__ == "__main__":
    main()
