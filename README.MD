![katto](assets/katto-readme-promo.svg)

# katto

Small Python CLI utility for common PDF page operations. Designed for simple workflows when working with print PDFs, scans, or page spreads.

## Features

- **trim** — trim pages to the PDF TrimBox (ideal for InDesign / print PDFs)
- **crop** — remove whitespace using `pdf-crop-margins`
- **split** — split spreads into two pages

## Requirements

- Python 3
- PyMuPDF (`fitz`)
- `pdf-crop-margins` (only needed for **crop**)

## Usage

Place your PDF in the same folder as `katto.py`.


**1. Trim a print PDF to its TrimBox:**

```
python3 katto.py trim doc.pdf
```

**2. Remove whitespace margins:**

```
python3 katto.py crop doc.pdf
```

**3. Split spreads into individual pages:**

```
python3 katto.py split doc.pdf
```

Output files are saved next to the input file:
- doc_trim.pdf
- doc_crop.pdf
- doc_split.pdf

## When to use what

**trim**

Use for print-layout PDFs exported from tools like InDesign.  
Removes bleed and crop marks using the PDF's TrimBox.

**crop**

Use for scanned PDFs or documents with large white margins.

**split**

Use when a PDF contains page spreads instead of individual pages.
