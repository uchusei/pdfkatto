# pdfkatto

Small Python CLI utility for common PDF page operations.

Designed for simple workflows when working with print PDFs, scans, or page spreads.

## Features

- **trim** — trim pages to the PDF TrimBox (ideal for InDesign / print PDFs)
- **crop** — remove whitespace using `pdf-crop-margins`
- **split** — split spreads into two pages

## Requirements

- Python 3
- PyMuPDF (`fitz`)
- `pdf-crop-margins` (only needed for `crop`)

## Usage

Place your PDF in the same folder as `pdfkatto.py`.

Trim a print PDF to its TrimBox:

python3 pdfkatto.py trim file.pdf

Remove whitespace margins:

python3 pdfkatto.py crop file.pdf

Split spreads into individual pages:

python3 pdfkatto.py split file.pdf

Output files are saved next to the input file:

file_trim.pdf
file_crop.pdf
file_split.pdf

## When to use what

**trim**

Use for print-layout PDFs exported from tools like InDesign.  
Removes bleed and crop marks using the PDF's TrimBox.

**crop**

Use for scanned PDFs or documents with large white margins.

**split**

Use when a PDF contains page spreads instead of individual pages.
