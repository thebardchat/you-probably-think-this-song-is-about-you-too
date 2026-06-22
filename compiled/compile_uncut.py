import os
import re

TRACK_LIST = [
    # (filepath, title_override, prefix)
    ("tracks/drafts/track-000.md", "### Track 000 — The Groove", "## SIDE A\n\n---\n\n"),
    ("tracks/drafts/track-001.md", "### Track 001 — The Commute", ""),
    ("tracks/drafts/track-002.md", "### Track 002 — The Diner", ""),
    ("tracks/interludes/sidetrack.md", "### Sidetrack", ""),
    ("tracks/drafts/track-003.md", "### Track 003 — The Landing", "## SIDE B\n\n---\n\n"),
    ("tracks/drafts/track-004.md", "### Track 004 — Substrate Firing", ""),
    ("tracks/drafts/track-005.md", "### Track 005 — The Wrong Reflection", ""),
    ("tracks/drafts/track-006.md", "### Track 006 — One Second", ""),
    ("tracks/drafts/track-007.md", "### Track 007 — Lipstick and Red Dress", ""),
    ("tracks/drafts/track-008.md", "### Track 008 — The Asking", ""),
    ("tracks/drafts/track-009.md", "### Track 009 — The Tip", ""),
    ("tracks/drafts/track-010.md", "### Track 010 — The Entrance", ""),
    ("tracks/drafts/track-011.md", "### Track 011 — The Shift", ""),
    ("tracks/drafts/track-012.md", "### Track 012 — The Pour", ""),
    ("tracks/drafts/track-013.md", "### Track 013 — The Third Thing", ""),
    ("tracks/drafts/track-014.md", "### Track 014 — The Twist", ""),
    ("tracks/drafts/track-0321.md", "### Dr. Seen Returns", "## BONUS TRACK\n\n---\n\n"),
    ("tracks/drafts/track-hidden.md", "", "") # Hidden track has no heading
]

def extract_lyrics(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Locate ## Lyrics
    lyrics_match = re.search(r'^## Lyrics\s*$', content, re.MULTILINE | re.IGNORECASE)
    if not lyrics_match:
        raise ValueError(f"Could not find '## Lyrics' in {filepath}")
    
    start_idx = lyrics_match.end()
    
    # Locate ## Liner Notes
    liner_notes_match = re.search(r'^## Liner Notes\s*$', content, re.MULTILINE | re.IGNORECASE)
    if liner_notes_match:
        end_idx = liner_notes_match.start()
    else:
        end_idx = len(content)
        
    lyrics_content = content[start_idx:end_idx]
    
    # Clean up whitespace and empty lines
    lines = [line.rstrip() for line in lyrics_content.split('\n')]
    
    # Strip leading/trailing empty lines
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
        
    # If the last line is just '---', strip it
    if lines and lines[-1] == '---':
        lines.pop()
        
    while lines and not lines[-1]:
        lines.pop()
        
    return '\n'.join(lines)

def main():
    output_lines = [
        "# You Probably Think This Song Is About You Too",
        "",
        "*Written by Shane Brazelton*",
        "*Co-built with Claude (Anthropic)*",
        "",
        "---",
        "",
        "&nbsp;",
        "",
        "*He is everyone and no one at the same time. That's not a riddle. That's the whole album.*",
        "",
        "&nbsp;",
        "",
        "---",
        ""
    ]
    
    for i, (filepath, title_override, prefix) in enumerate(TRACK_LIST):
        print(f"Parsing {filepath}...")
        lyrics = extract_lyrics(filepath)
        
        # Add Side prefix if any
        if prefix:
            output_lines.append(prefix)
            
        # Add Track Title
        if title_override:
            output_lines.append(title_override)
            output_lines.append("")
            output_lines.append("")
            
        output_lines.append(lyrics)
        
        # Add transition markers between tracks (but not after the last track)
        if i < len(TRACK_LIST) - 1:
            output_lines.append("")
            output_lines.append("&nbsp;")
            output_lines.append("")
            output_lines.append("---")
            output_lines.append("")
            
    # Add Credit section at the end of the manuscript
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("## Credit")
    output_lines.append("")
    output_lines.append("Written by Shane Brazelton.")
    output_lines.append("Co-built with Claude (Anthropic).")
    output_lines.append("Built on Raspberry Pi 5 + Pironman 5-MAX.")
    output_lines.append("")
    
    output_content = '\n'.join(output_lines)
    
    os.makedirs("compiled", exist_ok=True)
    with open("compiled/draft-006.md", "w", encoding='utf-8') as f:
        f.write(output_content)
        
    print("Compilation complete: compiled/draft-006.md")
    
    # Run pandoc conversions automatically
    import subprocess
    
    pandoc_paths = [
        os.path.join("compiled", "pandoc-bin", "pandoc-3.1.12.3", "pandoc.exe"),
        "pandoc"  # Fallback to system path
    ]
    
    pandoc_bin = None
    for path in pandoc_paths:
        try:
            subprocess.run([path, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            pandoc_bin = path
            break
        except Exception:
            continue
            
    if pandoc_bin:
        print(f"Using pandoc at: {pandoc_bin}")
        epub_out = "compiled/You_Probably_Think_This_Song_Is_About_You_Too.epub"
        docx_out = "compiled/You_Probably_Think_This_Song_Is_About_You_Too.docx"
        
        metadata_opts = [
            "--metadata", "title=You Probably Think This Song Is About You Too",
            "--metadata", "author=Shane Brazelton"
        ]
        
        try:
            print(f"Compiling EPUB: {epub_out}...")
            subprocess.run([pandoc_bin, "compiled/draft-006.md", "-o", epub_out] + metadata_opts, check=True)
            print("EPUB compilation successful.")
        except Exception as e:
            print(f"Failed to compile EPUB: {e}")
            
        try:
            print(f"Compiling DOCX: {docx_out}...")
            subprocess.run([pandoc_bin, "compiled/draft-006.md", "-o", docx_out] + metadata_opts, check=True)
            print("DOCX compilation successful.")
        except Exception as e:
            print(f"Failed to compile DOCX: {e}")
    else:
        print("Pandoc not found. Skipping EPUB/DOCX compilation.")

if __name__ == "__main__":
    main()
