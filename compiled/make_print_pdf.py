#!/usr/bin/env python3
"""Build a 6x9 print-ready PDF (KDP trade paperback) from compiled/draft-006.md.

Pure-Python (fpdf2) so it needs no LaTeX / LibreOffice. Embeds Times New Roman
for the body and Nirmala UI as a fallback so the Devanagari (Hindi) fragments
render. Mirrored gutter margins, justified body, centered track headings,
page numbers in the footer (suppressed on the title page).
"""
import os
import re
from fpdf import FPDF

# ---- Geometry (mm). 6x9 in = 152.4 x 228.6 mm ----
PAGE_W, PAGE_H = 152.4, 228.6
INSIDE = 25.4 * 0.875 + 25.4 * 0.125   # 0.875" + 0.125" gutter = 1.0" binding side
OUTSIDE = 25.4 * 0.625                  # 0.625" outer
TOP = 25.4 * 0.75                       # 0.75"
BOTTOM = 25.4 * 0.7                     # 0.7" (room for page number)
BODY_PT = 11
LINE_H = 5.2                            # mm line height for 11pt (~1.3 leading)

FONT_DIR = "C:/Windows/Fonts"
NIRMALA = "compiled/fonts/NirmalaUI.ttf"

SRC = "compiled/draft-006.md"
OUT = "compiled/You_Probably_Think_This_Song_Is_About_You_Too_6x9_print.pdf"


def ensure_devanagari_font():
    """Extract Nirmala UI (face 0) from the Windows .ttc collection if the
    standalone TTF isn't present. Avoids committing the Microsoft font."""
    if os.path.exists(NIRMALA):
        return
    os.makedirs(os.path.dirname(NIRMALA), exist_ok=True)
    from fontTools.ttLib import TTFont
    ttc = os.path.join(FONT_DIR, "Nirmala.ttc")
    TTFont(ttc, fontNumber=0).save(NIRMALA)
    print(f"Extracted Devanagari fallback -> {NIRMALA}")


def md_inline(text):
    """Convert markdown emphasis to fpdf2's markdown dialect.
    fpdf2 markdown: **bold**, __italics__. Source uses *italics*."""
    # protect bold first
    text = text.replace("**", "\x00")
    # single *italic* -> __italic__
    text = re.sub(r"\*([^*\n]+)\*", r"__\1__", text)
    text = text.replace("\x00", "**")
    text = text.replace("&nbsp;", " ")
    return text


class Book(FPDF):
    def header(self):
        # Mirrored margins: gutter (inside) on the binding edge.
        if self.page_no() % 2 == 1:          # recto / odd -> gutter left
            self.set_margins(INSIDE, TOP, OUTSIDE)
        else:                                 # verso / even -> gutter right
            self.set_margins(OUTSIDE, TOP, INSIDE)

    FRONT_MATTER_PAGES = 2                     # title page + copyright page

    def footer(self):
        if self.page_no() <= self.FRONT_MATTER_PAGES:   # no number on front matter
            return
        self.set_y(-12)
        self.set_font("Body", "", 9)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, str(self.page_no() - self.FRONT_MATTER_PAGES), align="C")
        self.set_text_color(0, 0, 0)


def build():
    ensure_devanagari_font()
    pdf = Book(orientation="P", unit="mm", format=(PAGE_W, PAGE_H))
    pdf.set_title("You Probably Think This Song Is About You Too")
    pdf.set_author("Shane Brazelton")
    pdf.set_auto_page_break(True, margin=BOTTOM)

    for style, fn in [("", "times.ttf"), ("B", "timesbd.ttf"),
                      ("I", "timesi.ttf"), ("BI", "timesbi.ttf")]:
        pdf.add_font("Body", style, os.path.join(FONT_DIR, fn))
    # Nirmala UI has no italic/bold face; reuse the same file for every style
    # so the Devanagari fallback resolves inside italic/bold runs too.
    for style in ("", "B", "I", "BI"):
        pdf.add_font("Deva", style, NIRMALA)
    pdf.set_fallback_fonts(["Deva"])

    content = open(SRC, encoding="utf-8").read()

    # ---- Front matter vs body ----
    front, sep, rest = content.partition("\n## ")
    body = ("## " + rest) if sep else ""

    front_lines = [l.strip() for l in front.splitlines()]
    title = next((l[2:].strip() for l in front_lines if l.startswith("# ")), "")
    italics = [l.strip("*").strip() for l in front_lines
               if l.startswith("*") and l.endswith("*") and len(l) > 2]

    # ---- Title page ----
    pdf.add_page()
    pdf.set_y(70)
    pdf.set_font("Body", "B", 24)
    pdf.multi_cell(0, 11, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Body", "I", 12)
    for it in italics[:2]:                    # byline(s)
        pdf.multi_cell(0, 7, it, align="C", new_x="LMARGIN", new_y="NEXT")
    if len(italics) > 2:                      # epigraph
        pdf.ln(28)
        pdf.set_font("Body", "I", 12)
        pdf.multi_cell(0, 7, italics[2], align="C", new_x="LMARGIN", new_y="NEXT")

    # ---- Copyright / front matter page ----
    pdf.add_page()
    pdf.set_y(90)
    cp = [
        ("B", 11, "You Probably Think This Song Is About You Too"),
        ("I", 10, "A Noir Song Cycle — Volume Two"),
        ("", 10, ""),
        ("", 10, "Copyright © 2026 Shane Brazelton"),
        ("", 10, "All rights reserved."),
        ("", 10, ""),
        ("", 10, "Co-built with Claude (Anthropic)."),
        ("", 10, "Built on Raspberry Pi 5 + Pironman 5-MAX."),
        ("", 10, ""),
        ("I", 9, "This is a work of fiction. Names, characters, and incidents are "
                 "the product of the author's imagination."),
        ("", 10, ""),
        ("", 9, "This book deals with trauma, loss, and mental health. If you are struggling:"),
        ("", 9, "988 — Suicide & Crisis Lifeline (call or text, 24/7)"),
        ("", 9, "741741 — Crisis Text Line (text HOME)"),
        ("", 9, "1-800-662-4357 — SAMHSA National Helpline"),
        ("", 10, ""),
        ("", 9, "ISBN: [to be assigned]"),
        ("", 9, "First edition, 2026"),
    ]
    for style, size, line in cp:
        if line == "":
            pdf.ln(3)
            continue
        pdf.set_font("Body", style, size)
        pdf.multi_cell(0, 5, line, align="C", new_x="LMARGIN", new_y="NEXT")

    # ---- Body ----
    def flush(buf):
        if not buf:
            return
        para = md_inline(" ".join(buf).strip())
        if not para:
            return
        pdf.set_font("Body", "", BODY_PT)
        pdf.multi_cell(0, LINE_H, para, align="J", markdown=True,
                       new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    buf = []
    for raw in body.splitlines():
        s = raw.strip()
        if s == "":
            flush(buf); buf = []
            continue
        if s.startswith("### "):              # track heading -> new page
            flush(buf); buf = []
            pdf.add_page()
            pdf.set_font("Body", "B", 15)
            pdf.ln(4)
            pdf.multi_cell(0, 8, s[4:].strip(), align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(6)
        elif s.startswith("## "):             # SIDE / BONUS / Credit -> new page
            flush(buf); buf = []
            pdf.add_page()
            pdf.ln(10)
            pdf.set_font("Body", "B", 18)
            pdf.multi_cell(0, 10, s[3:].strip(), align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(8)
        elif s == "---":                      # scene separator
            flush(buf); buf = []
            pdf.ln(2)
            pdf.set_font("Body", "", BODY_PT)
            pdf.multi_cell(0, LINE_H, "*   *   *", align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif s == "&nbsp;":                   # blank-space marker
            flush(buf); buf = []
            pdf.ln(3)
        else:
            buf.append(s)
    flush(buf)

    pdf.output(OUT)
    pages = pdf.page_no()
    size = os.path.getsize(OUT) / 1024
    print(f"PDF written: {OUT}")
    print(f"Pages: {pages}  |  Size: {size:.0f} KB  |  Trim: 6 x 9 in")


if __name__ == "__main__":
    build()
