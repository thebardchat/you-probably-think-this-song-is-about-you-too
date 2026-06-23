# Cover Candidates

All covers are AI noir art (HuggingFace Z-Image-Turbo, 2:3) with typography
composited on top by `make_front_cover.py` (title in Cambria Bold, subtitle/author
in Bahnschrift, gradient scrims hide the model's stray sign text).

## ★ CHOSEN — Turntable

- **Source art:** `art/art-turntable_seed11.webp` (seed 11)
- **Composite:** `front-cover.jpg`
- **Live as:** `../cover-ebook.jpg` (eBook cover + embedded in the EPUB + front of the paperback wrap)
- Scene: vinyl record on a turntable, smoke rising into the title. Chosen for the
  "song cycle / album" concept (Side A/Side B, the needle drops).
- `make_front_cover.py` defaults to this art, so a no-arg run reproduces the live cover.

## Runner-up candidates (kept for reference, not live)

| Scene | Source art | Composite | Seed |
|-------|-----------|-----------|------|
| Empty diner booth (coffee, rainy neon) | `art/art-booth_seed23.webp` | `cover-candidate-booth.jpg` | 23 |
| Wet alley, lone figure under lamp | `art/art-alley_seed31.webp` | `cover-candidate-alley.jpg` | 31 |
| Figure at rain-streaked diner window | `art/art-diner-window_seed7.webp` | `cover-candidate-diner-window.jpg` | 7 |

## To switch the live cover to a runner-up

```bash
# 1. point the generator at the chosen art (edit ART in make_front_cover.py), or one-off:
python compiled/make_front_cover.py compiled/art/art-booth_seed23.webp compiled/front-cover.jpg
# 2. promote it and rebuild everything:
cp compiled/front-cover.jpg cover-ebook.jpg
python compiled/compile_uncut.py        # rebuild EPUB (embeds cover) + DOCX
python compiled/make_wrap_cover.py      # rebuild paperback wrap with new front
```
