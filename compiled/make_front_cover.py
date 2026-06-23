#!/usr/bin/env python3
"""Composite a designed front cover from AI noir art + real typography.

Scales the generated art to KDP's 1600x2560 eBook spec, lays gradient scrims
top/bottom (the top scrim hides the AI's gibberish sign), and sets the title,
subtitle, and author with proper letter-spacing and drop shadows.

Run: python compiled/make_front_cover.py
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2560
ART = "compiled/art/art-turntable_seed11.webp"   # CHOSEN cover: vinyl turntable + smoke (Z-Image seed 11)
OUT = "compiled/front-cover.jpg"
# Optional CLI override: python make_front_cover.py <art_in> <jpg_out>
if len(sys.argv) >= 3:
    ART, OUT = sys.argv[1], sys.argv[2]
FONT_DIR = "C:/Windows/Fonts"

TITLE_FONT = os.path.join(FONT_DIR, "cambriab.ttf")     # elegant serif
META_FONT = os.path.join(FONT_DIR, "Bahnschrift.ttf")   # modern condensed sans

TITLE_LINES = ["YOU PROBABLY THINK", "THIS SONG IS ABOUT", "YOU TOO"]
SUBTITLE = "A NOIR SONG CYCLE  ·  VOLUME TWO"
AUTHOR = "SHANE BRAZELTON"

CREAM = (250, 245, 236)
WARM_GRAY = (208, 198, 182)


def cover_crop(img, w, h):
    """Scale to fully cover w x h, then center-crop."""
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def scrims(base):
    """Darken top (hide AI sign) and bottom (seat the author line)."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    t_full, t_end, t_a = 940, 1260, 255       # fully opaque to 940px (hides AI sign), fade to 1260
    b_start, b_a = 1950, 232
    for y in range(H):
        a = t_a if y < t_full else (
            int(t_a * (1 - (y - t_full) / (t_end - t_full))) if y < t_end else 0)
        if y > b_start:
            a = max(a, int(b_a * ((y - b_start) / (H - b_start))))
        if a:
            d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    return Image.alpha_composite(base.convert("RGBA"), ov)


def tracked_width(draw, text, font, track):
    return sum(draw.textlength(c, font=font) for c in text) + track * (len(text) - 1)


def draw_tracked(draw, cx, top, text, font, fill, track, shadow=True):
    total = tracked_width(draw, text, font, track)
    x = cx - total / 2
    for c in text:
        if shadow:
            draw.text((x + 3, top + 4), c, font=font, fill=(0, 0, 0, 200), anchor="la")
        draw.text((x, top), c, font=font, fill=fill, anchor="la")
        x += draw.textlength(c, font=font) + track


def fit_size(path, text, track_frac, max_w, hi=200, lo=40):
    """Largest font size where letter-spaced `text` fits within max_w."""
    probe = Image.new("RGB", (10, 10))
    pd = ImageDraw.Draw(probe)
    for s in range(hi, lo - 1, -2):
        f = ImageFont.truetype(path, s)
        if tracked_width(pd, text, f, s * track_frac) <= max_w:
            return s
    return lo


def build():
    art = Image.open(ART)
    base = cover_crop(art, W, H)
    base = scrims(base)
    d = ImageDraw.Draw(base)
    cx = W / 2

    # ---- Title (uniform size set by the longest line) ----
    t_track_frac = 0.06
    longest = max(TITLE_LINES, key=len)
    t_size = fit_size(TITLE_FONT, longest, t_track_frac, W - 260, hi=150)
    tfont = ImageFont.truetype(TITLE_FONT, t_size)
    line_h = int(t_size * 1.16)
    y = 250
    for line in TITLE_LINES:
        draw_tracked(d, cx, y, line, tfont, CREAM, t_size * t_track_frac)
        y += line_h

    # ---- Thin divider + subtitle ----
    y += 18
    d.line([(cx - 150, y), (cx + 150, y)], fill=WARM_GRAY, width=2)
    y += 26
    s_size = fit_size(META_FONT, SUBTITLE, 0.18, W - 360, hi=58)
    sfont = ImageFont.truetype(META_FONT, s_size)
    draw_tracked(d, cx, y, SUBTITLE, sfont, WARM_GRAY, s_size * 0.18, shadow=False)

    # ---- Author (bottom) ----
    a_size = fit_size(META_FONT, AUTHOR, 0.22, W - 320, hi=88)
    afont = ImageFont.truetype(META_FONT, a_size)
    ay = H - 230
    d.line([(cx - 110, ay - 34), (cx + 110, ay - 34)], fill=WARM_GRAY, width=2)
    draw_tracked(d, cx, ay, AUTHOR, afont, CREAM, a_size * 0.22)

    base.convert("RGB").save(OUT, "JPEG", quality=92)
    print(f"Front cover: {OUT}  ({W}x{H})  {os.path.getsize(OUT)/1024:.0f} KB")
    print(f"Title size {t_size}px | subtitle {s_size}px | author {a_size}px")


if __name__ == "__main__":
    build()
