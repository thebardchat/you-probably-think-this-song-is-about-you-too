import os
import re

TRACK_LIST = [
    # (filepath, title_override, prefix)
    ("tracks/drafts/track-000.md", "### Track 000 — The Groove", "## SIDE A\n\n---\n\n"),
    ("tracks/interludes/sidetrack.md", "### Sidetrack", ""),
    ("tracks/drafts/track-001.md", "### Track 001 — The Commute", ""),
    ("tracks/drafts/track-002.md", "### Track 002 — The Diner", ""),
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
    
    for filepath, title_override, prefix in TRACK_LIST:
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
        output_lines.append("")
        output_lines.append("---")
        output_lines.append("")
        
    # The last track ends with '---' which is followed by the sign-off, helplines, etc.
    # Let's check how the ending is constructed in draft-002.md
    # We will read the end of draft-002.md or just append it manually.
    # Let's see what is after the hidden track in draft-002.md
    # Actually, the ending contains the seen sign-off, suicide lifeline, and credits.
    # Let's write them.
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("It's never too late to be Seen.")
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("**988** — Suicide & Crisis Lifeline (call or text, 24/7)")
    output_lines.append("**741741** — Crisis Text Line (text HOME)")
    output_lines.append("**1-800-662-4357** — SAMHSA National Helpline")
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("*The door has a handle on your side.*")
    output_lines.append("")
    output_lines.append("&nbsp;")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")
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

if __name__ == "__main__":
    main()
