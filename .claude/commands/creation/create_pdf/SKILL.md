# Create PDF

Convert all Markdown files from a source directory into PDF files stored in an output directory.

Uses `pandoc` for conversion. Make sure it is installed (`pandoc --version`).

## Steps

1. Run the converter:
   ```bash
   python .claude/commands/creation/create_pdf/scripts/md_to_pdf.py $ARGUMENTS
   ```
   Supported arguments:
   - `--input-dir PATH`  Directory containing `.md` files (default: `markdown`)
   - `--output-dir PATH` Directory where `.pdf` files will be written (default: `pdf`)

2. List the generated PDF files:
   ```bash
   ls -lh <output-dir>/
   ```
   Replace `<output-dir>` with the value passed to `--output-dir` (or `pdf` by default).

3. Summarize the results to the user:
   - How many files were converted successfully
   - Which files failed (if any) and why
