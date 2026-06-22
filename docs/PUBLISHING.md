# Publishing Playbook — You Probably Think This Song Is About You Too

This document defines the standard operating procedure (SOP) for publishing Volume Two: *You Probably Think This Song Is About You Too* (Part Too). This playbook aligns formatting, platforms, and assets to match the publication standard established in Volume One.

---

## 1. Metadata and Listings

### 1.1 Book Specifications
* **Title:** You Probably Think This Song Is About You Too
* **Subtitle:** A Noir Song Cycle (Vol. 2)
* **Author:** Shane Brazelton
* **Collaborator:** Claude (Anthropic)
* **Description:**
  > A dark, heavy, and stylized noir detective thriller written by a dump truck dispatcher on a Raspberry Pi in a closet in Alabama. Co-built with AI. 
  > 
  > Volume Two picks up where the movie ends and the record starts playing. The detective has been ripped out of his own body and dropped into a European diner, living one second over and over from nine different perspectives, trying to change a tragic outcome he can never avert. All of it happening on a therapist's couch — though you won't realize it until the needle drops on the bonus track.
  > 
  > It is the second side of the same record. He is everyone and no one at the same time. That's not a riddle. That's the whole album.
* **Primary Category:** Fiction > Noir / Thrillers > Psychological
* **Secondary Category:** Fiction > Alternative History / Tech

### 1.2 Keywords (KDP & Gumroad)
`noir fiction`, `indie author`, `AI writing`, `psychological thriller`, `raspberry pi`, `speculative fiction`, `build in public`

---

## 2. Platform Delivery Sequences

### 2.1 Amazon KDP (Kindle & Paperback)
1. **Kindle eBook:**
   * Upload the compiled EPUB: [You_Probably_Think_This_Song_Is_About_You_Too.epub](file:///c:/Users/Hubby/you-probably-think-this-song-is-about-you-too/you-probably-think-this-song-is-about-you-too/compiled/You_Probably_Think_This_Song_Is_About_You_Too.epub).
   * Upload eBook cover: `cover-ebook.png` (or `.jpg`).
   * Set price matching Volume One ($2.99 or similar promotional price).
2. **Paperback:**
   * Open the compiled Word document: [You_Probably_Think_This_Song_Is_About_You_Too.docx](file:///c:/Users/Hubby/you-probably-think-this-song-is-about-you-too/you-probably-think-this-song-is-about-you-too/compiled/You_Probably_Think_This_Song_Is_About_You_Too.docx) in Microsoft Word.
   * **Formatting Checklist for Print PDF:**
     - Set page size to **6" x 9"** (standard trade paperback).
     - Set margins: **Top 1", Bottom 1", Left 1" (Gutter 0.125"), Right 0.875"** (adjust Gutter depending on page count, ~75 pages is standard).
     - Select a premium serif font (e.g., *Georgia* or *Palatino Linotype*) at **11pt** with **1.2x line spacing**.
     - Center the Scene headings (e.g. `### Track 001 — The Commute`) and ensure `&nbsp;` spaces translate to clean page breaks or line breaks.
     - Add page numbering in the footer (suppress on title/credits pages).
     - Save as a print-ready **PDF**.
   * Upload the PDF manuscript to KDP.
   * Upload the paperback cover PDF matching the spine width template (KDP spine calculator based on page count).

### 2.2 Gumroad (Digital Bundle)
Offer a digital-only premium bundle that includes:
1. **Manuscript formats:** EPUB, PDF, and DOCX.
2. **Audiobook tracks:** MP3/WAV files rendered via ElevenLabs using our clean scripts.
3. **Exclusive Extras:** Access code/link to the Director's Cut or interactive elements on the web portal.

---

## 3. Audiobook Production (ElevenLabs)

Our audio assets are managed via script generators in `compiled/`:
* **Text script with pronunciation dictionary applied:** [audio_script_clean.txt](file:///c:/Users/Hubby/you-probably-think-this-song-is-about-you-too/you-probably-think-this-song-is-about-you-too/compiled/audio_script_clean.txt) — use this for copying/pasting sections into the ElevenLabs reader.
* **SSML script with timed breaks and rate controls:** [audio_script.ssml](file:///c:/Users/Hubby/you-probably-think-this-song-is-about-you-too/you-probably-think-this-song-is-about-you-too/compiled/audio_script.ssml) — use this for direct SSML input to ensure dramatic pacing.

### 3.1 Audio Specifications
* **Narrator Voice:** ElevenLabs standard detective/noir voice (matching Volume One).
* **Speed/Prosody:**
  - Standard passages: default.
  - Pepe's name loop in the hidden track: set prosody speed to **50%** and pitch to **-2st** to make it sound labored, slow, and struggling.
* **Transitions:**
  - `---` translates to a **1.5-second pause**.
  - `&nbsp;` transitions between scenes translate to a **2.5-second pause**.
  - Pre-hidden track gap: **15-second silence** to create the classic CD hidden-track effect.

---

## 4. Director's Cut Hidden Door

To preserve the mystery, the Director's Cut (which contains all ~43,000 words, detailed character backstories, and uncut vignettes) lives behind a digital "hidden door" on our public portal:
* **QR Code:** Placed in the back of the print book.
* **Access URL:** Points to our custom web reader.
* **Discord Integration:** Grants access to the private `#the-diner` community channel.
