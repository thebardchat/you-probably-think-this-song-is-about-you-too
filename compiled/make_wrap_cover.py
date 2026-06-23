#!/usr/bin/env python3
"""Build a basic KDP full-wrap paperback cover TEMPLATE (front+spine+back+bleed).

Sized for a 6x9 trim at PAGES pages on white paper. Draws trim/fold/safe guides,
a barcode keep-out zone, spine text, the back-cover blurb, and places the eBook
art as a front preview. The cyan guide lines are layout aids — REMOVE them (or
regenerate with GUIDES=False) before uploading the final cover to KDP.

Run: python compiled/make_wrap_cover.py
"""
import os
from fpdf import FPDF

IN = 25.4                       # mm per inch
TRIM_W, TRIM_H = 6 * IN, 9 * IN
BLEED = 0.125 * IN
SAFE = 0.25 * IN                # keep text this far inside trim
PAGES = 161
PAPER_PER_PAGE = 0.002252       # KDP white paper, inches/page
SPINE = round(PAGES * PAPER_PER_PAGE, 4) * IN

FULL_W = 2 * BLEED + 2 * TRIM_W + SPINE
FULL_H = TRIM_H + 2 * BLEED

# X fold/trim boundaries (mm, from left edge of the flat cover)
BACK_X0 = BLEED
BACK_X1 = BLEED + TRIM_W                 # back trim / left spine fold
SPINE_X1 = BACK_X1 + SPINE               # right spine fold
FRONT_X1 = SPINE_X1 + TRIM_W             # front trim
TOP_Y = BLEED
BOT_Y = BLEED + TRIM_H

FONT_DIR = "C:/Windows/Fonts"
NIRMALA = "compiled/fonts/NirmalaUI.ttf"
COVER_ART = "cover-ebook.jpg"
OUT = "compiled/wrap-cover-6x9-template.pdf"
GUIDES = True

BLURB = (
    "A dark, stylized noir thriller written by a dump-truck dispatcher on a "
    "Raspberry Pi in a closet in Alabama. Co-built with AI.\n\n"
    "Volume Two picks up where the movie ends and the record starts playing. "
    "The detective has been ripped out of his own body and dropped into a "
    "European diner, living one second over and over from nine perspectives, "
    "trying to change a tragic outcome he can never avert. All of it happening "
    "on a therapist's couch — though you won't realize it until the needle "
    "drops on the bonus track.\n\n"
    "It is the second side of the same record. He is everyone and no one at the "
    "same time. That's not a riddle. That's the whole album."
)


def fit_font(pdf, text, max_w, start=28, lo=6):
    """Largest integer pt size at which `text` fits within max_w mm."""
    for size in range(start, lo - 1, -1):
        pdf.set_font_size(size)
        if pdf.get_string_width(text) <= max_w:
            return size
    return lo


def build():
    pdf = FPDF(orientation="P", unit="mm", format=(FULL_W, FULL_H))
    pdf.set_auto_page_break(False)
    pdf.set_title("Wrap cover template")
    for style, fn in [("", "times.ttf"), ("B", "timesbd.ttf"), ("I", "timesi.ttf")]:
        pdf.add_font("Body", style, os.path.join(FONT_DIR, fn))
    pdf.add_page()

    # --- Black background, full bleed ---
    pdf.set_fill_color(8, 8, 10)
    pdf.rect(0, 0, FULL_W, FULL_H, style="F")

    # --- Front cover art preview (fills front panel + outer bleed) ---
    if os.path.exists(COVER_ART):
        pdf.image(COVER_ART, x=SPINE_X1, y=0, w=FULL_W - SPINE_X1, h=FULL_H)

    # --- Back cover blurb (white, inside safe zone) ---
    pdf.set_text_color(225, 225, 225)
    pdf.set_xy(BACK_X0 + SAFE, TOP_Y + SAFE + 6)
    pdf.set_font("Body", "I", 12)
    pdf.multi_cell(TRIM_W - 2 * SAFE, 6.2, BLURB, align="L",
                   new_x="LMARGIN", new_y="NEXT")

    # --- Barcode keep-out (white box, lower-right of back cover) ---
    bc_w, bc_h = 2 * IN, 1.2 * IN
    bc_x = BACK_X1 - SAFE - bc_w
    bc_y = BOT_Y - SAFE - bc_h
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(bc_x, bc_y, bc_w, bc_h, style="F")
    pdf.set_text_color(120, 120, 120)
    pdf.set_font("Body", "", 7)
    pdf.set_xy(bc_x, bc_y + bc_h / 2 - 3)
    pdf.multi_cell(bc_w, 3.4, "ISBN / BARCODE\n(leave clear — KDP adds it)",
                   align="C", new_x="LMARGIN", new_y="NEXT")

    # --- Spine text (rotated, top-to-bottom), only if spine is wide enough ---
    if SPINE >= 0.0625 * IN:
        cx = (BACK_X1 + SPINE_X1) / 2
        cy = FULL_H / 2
        spine_txt = "YOU PROBABLY THINK THIS SONG IS ABOUT YOU TOO    ·    SHANE BRAZELTON"
        pdf.set_text_color(235, 235, 235)
        pdf.set_font("Body", "B", 10)
        size = fit_font(pdf, spine_txt, FULL_H - 2 * SAFE, start=11, lo=6)
        pdf.set_font("Body", "B", size)
        w = pdf.get_string_width(spine_txt)
        with pdf.rotation(-90, cx, cy):
            pdf.set_xy(cx - w / 2, cy - size * 0.35)
            pdf.cell(w, size * 0.7, spine_txt, align="C")

    # --- Guides (remove for final upload) ---
    if GUIDES:
        pdf.set_draw_color(0, 200, 210)
        pdf.set_line_width(0.2)
        pdf.set_dash_pattern(dash=1.5, gap=1.5)
        for x in (BACK_X1, SPINE_X1):                       # spine folds
            pdf.line(x, 0, x, FULL_H)
        pdf.rect(BLEED, TOP_Y, 2 * TRIM_W + SPINE, TRIM_H)  # trim box
        pdf.set_draw_color(0, 130, 140)                     # safe margins
        for x0, x1 in ((BACK_X0, BACK_X1), (SPINE_X1, FRONT_X1)):
            pdf.rect(x0 + SAFE, TOP_Y + SAFE,
                     (x1 - x0) - 2 * SAFE, TRIM_H - 2 * SAFE)
        pdf.set_dash_pattern()                              # solid for labels
        pdf.set_text_color(0, 210, 220)
        pdf.set_font("Body", "B", 8)
        for label, xc in (("BACK COVER", (BACK_X0 + BACK_X1) / 2),
                          ("FRONT COVER", (SPINE_X1 + FRONT_X1) / 2)):
            pdf.set_xy(xc - 30, TOP_Y + 2)
            pdf.cell(60, 4, label, align="C")
        cap = (f"Full wrap {FULL_W/IN:.3f} x {FULL_H/IN:.3f} in  |  "
               f"trim 6x9  |  spine {SPINE/IN:.3f} in @ {PAGES} pp white paper  |  "
               f"bleed 0.125 in  |  guides = cyan (remove before upload)")
        pdf.set_xy(BLEED, FULL_H - 4.5)
        pdf.set_font("Body", "", 6)
        pdf.cell(2 * TRIM_W + SPINE, 3, cap, align="C")

    pdf.output(OUT)
    print(f"Wrap cover template: {OUT}")
    print(f"Full size: {FULL_W/IN:.3f} x {FULL_H/IN:.3f} in "
          f"({FULL_W:.1f} x {FULL_H:.1f} mm)")
    print(f"Spine: {SPINE/IN:.3f} in ({SPINE:.2f} mm) for {PAGES} pages")
    print(f"Size on disk: {os.path.getsize(OUT)/1024:.0f} KB")


if __name__ == "__main__":
    build()
