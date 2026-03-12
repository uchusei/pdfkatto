#!/usr/bin/env python3

"""
pdfkatto

Small utility script for common PDF page operations.

This script provides three commands:

1. trim
   Trim pages to the PDF TrimBox.
   Useful for print-layout PDFs exported from InDesign or similar tools
   where crop marks and bleed exist outside the final page.

2. crop
   Automatically remove white margins using the external tool
   `pdf-crop-margins`.

3. split
   Split each page vertically into two pages (left and right).
   Useful for PDFs that contain spreads instead of individual pages.

Example usage:

    python3 pdfkatto.py trim book.pdf
    python3 pdfkatto.py crop document.pdf
    python3 pdfkatto.py split spreads.pdf

Output files are saved next to the input file with suffixes:
    *_trim.pdf
    *_crop.pdf
    *_split.pdf
"""

import argparse
from pathlib import Path
import subprocess
import shutil
import fitz  # PyMuPDF


def trim(pdf):
    """
    Trim pages to the PDF TrimBox.

    Many print PDFs contain crop marks and bleed outside the final
    page area. The TrimBox defines the final intended page size.

    This function sets each page's MediaBox to the existing TrimBox.
    That preserves the original page coordinates, which is important
    for InDesign / print-layout PDFs.
    """

    doc = fitz.open(pdf)

    for page in doc:
        # Use the existing TrimBox exactly as it is.
        # Do not normalize it to (0, 0), because that can shift content.
        page.set_mediabox(page.trimbox)

    out = Path(pdf).with_name(Path(pdf).stem + "_trim.pdf")
    doc.save(out)

    print("Saved:", out)


def crop(pdf):
    """
    Remove margins automatically using the external tool pdf-crop-margins.

    This is useful for scanned documents or PDFs without proper TrimBox
    information.

    The script calls the command-line program `pdf-crop-margins`.
    """

    exe = shutil.which("pdf-crop-margins")

    if not exe:
        raise RuntimeError("pdf-crop-margins not installed")

    out = Path(pdf).with_name(Path(pdf).stem + "_crop.pdf")

    # Call pdf-crop-margins with parameters
    subprocess.run([
        exe,
        "-v",          # verbose output
        "-x", "0",     # horizontal margin offset
        "-y", "0",     # vertical margin offset
        "-s",          # same cropping for all pages
        pdf,
        "-o", str(out)
    ])


def split(pdf):
    """
    Split each page vertically into two pages.

    This is useful when a PDF contains spreads (two pages side-by-side)
    instead of individual pages.

    The function:
    1. Reads each page
    2. Tries to use TrimBox for more accurate splitting
       (important for print PDFs with bleed / crop marks)
    3. Falls back to the visible page rectangle if needed
    4. Creates two new pages (left and right)
    """

    src = fitz.open(pdf)
    out = fitz.open()

    for page in src:
        # Prefer TrimBox when available because it represents the final
        # intended page area after trimming. This avoids splitting based
        # on bleed or crop marks.
        trim = page.trimbox
        rect = page.rect

        # If TrimBox has a valid size, use it. Otherwise fall back to page.rect.
        if trim.width > 0 and trim.height > 0:
            split_rect = trim
        else:
            split_rect = rect

        # Calculate midpoint using the chosen rectangle.
        # This is more accurate for print PDFs than splitting page.rect directly.
        mid_x = split_rect.x0 + (split_rect.width / 2)

        # Define left and right halves of the page.
        left = fitz.Rect(split_rect.x0, split_rect.y0, mid_x, split_rect.y1)
        right = fitz.Rect(mid_x, split_rect.y0, split_rect.x1, split_rect.y1)

        # Create a new page for the left half and place the clipped content onto it.
        left_page = out.new_page(width=left.width, height=left.height)
        left_page.show_pdf_page(left_page.rect, src, page.number, clip=left)

        # Create a new page for the right half and place the clipped content onto it.
        right_page = out.new_page(width=right.width, height=right.height)
        right_page.show_pdf_page(right_page.rect, src, page.number, clip=right)

    outfile = Path(pdf).with_name(Path(pdf).stem + "_split.pdf")

    out.save(outfile)

    print("Saved:", outfile)


def main():
    """
    CLI entry point.

    Parses command line arguments and calls the correct function.
    """

    parser = argparse.ArgumentParser(prog="pdfkatto")

    sub = parser.add_subparsers(dest="cmd", required=True)

    # trim command
    trim_cmd = sub.add_parser("trim", help="Trim pages to TrimBox")
    trim_cmd.add_argument("file")

    # crop command
    crop_cmd = sub.add_parser("crop", help="Remove margins automatically")
    crop_cmd.add_argument("file")

    # split command
    split_cmd = sub.add_parser("split", help="Split spreads into pages")
    split_cmd.add_argument("file")

    args = parser.parse_args()

    if args.cmd == "trim":
        trim(args.file)

    elif args.cmd == "crop":
        crop(args.file)

    elif args.cmd == "split":
        split(args.file)


if __name__ == "__main__":
    main()