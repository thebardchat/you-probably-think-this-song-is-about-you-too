import os
import re

TRACK_LIST = [
    # (filepath, spoken_title, prefix)
    ("tracks/drafts/track-000.md", "Side A. Track Zero: The Groove.", ""),
    ("tracks/interludes/sidetrack.md", "Sidetrack.", ""),
    ("tracks/drafts/track-001.md", "Track One: The Commute.", ""),
    ("tracks/drafts/track-002.md", "Track Two: The Diner.", ""),
    ("tracks/drafts/track-003.md", "Side B. Track Three: The Landing.", ""),
    ("tracks/drafts/track-004.md", "Track Four: Substrate Firing.", ""),
    ("tracks/drafts/track-005.md", "Track Five: The Wrong Reflection.", ""),
    ("tracks/drafts/track-006.md", "Track Six: One Second.", ""),
    ("tracks/drafts/track-007.md", "Track Seven: Lipstick and Red Dress.", ""),
    ("tracks/drafts/track-008.md", "Track Eight: The Asking.", ""),
    ("tracks/drafts/track-009.md", "Track Nine: The Tip.", ""),
    ("tracks/drafts/track-010.md", "Track Ten: The Entrance.", ""),
    ("tracks/drafts/track-011.md", "Track Eleven: The Shift.", ""),
    ("tracks/drafts/track-012.md", "Track Twelve: The Pour.", ""),
    ("tracks/drafts/track-013.md", "Track Thirteen: The Third Thing.", ""),
    ("tracks/drafts/track-014.md", "Track Fourteen: The Twist.", ""),
    ("tracks/drafts/track-0321.md", "Bonus Track. Doctor Seen Returns.", ""),
    ("tracks/drafts/track-hidden.md", "Hidden Track.", "hidden") # hidden prefix signals 15s silence
]

PHONETIC_REPLACEMENTS = {
    # Characters
    "Pepe": "PEH-peh",
    "Brazelton": "Brazzleton",
    "Enzo Ferrara": "EN-zoh feh-RAH-rah",
    "Sandro Luciano": "SAHN-droh loo-CHAH-noh",
    "Luca Delvecchio": "LOO-kah del-VEK-ee-oh",
    "Marco Ferretti": "MAR-koh feh-RET-ee",
    "Tomás Aguilar": "toh-MAHS ah-gee-LAR",
    "Gianluca Parisi": "jahn-LOO-kah pah-REE-see",
    "Rafael Mendes": "hah-fah-EL MEN-dez",
    "Claudia": "CLOW-dee-ah",
    "Davide": "dah-VEE-deh",
    "Marta": "MAR-tah",
    "Paulo": "POW-loh",
    "Ciro": "CHEE-roh",
    
    # Places / Nouns
    "San Siro": "sahn SEE-roh",
    "Villarreal": "vee-yah-reh-AHL",
    "Salerno": "sah-LAIR-noh",
    "Bari": "BAH-ree",
    "São Paulo": "sow POW-loh",
    "Napoli": "NAH-poh-lee",
    "Pune": "POO-neh",
    "Ibiza": "ee-BEE-thah",
    "Valencia": "vah-LEN-see-ah",
    "Antonio's": "an-TOH-nee-ohs",
    
    # Foreign Words
    "कोई क्या अपमान में मैं": "koy kyaa ap-MAAN mein main",
    "आधा किया जी": "AAH-dhah kee-YAH jee",
    "Muoviti": "MWOH-vee-tee",
    "FRATELLO": "frah-TEL-loh",
    "Aos irmãos. Aos que ficaram. Aos que voltaram.": "owsh eer-MOWNS. owsh keh fee-KAH-rong. owsh keh vol-TAH-rong.",
    "irmão": "eer-MOWNG",
    "grazie, Mamma": "GRAH-tsee-eh, MAH-mah",
    "senhora": "sen-YOR-ah",
    "limoncello": "lee-mon-CHEL-loh",
    "trattoria": "trah-toh-REE-ah",
    "Pelé": "peh-LEH",
    
    # Difficult English
    "panopticon": "pan-OP-tih-kon",
    "epistemology": "eh-PIST-eh-MOL-oh-jee",
    "jigger": "JIG-er"
}

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

def apply_phonetics(text):
    # Perform substitutions from longest keys first to avoid partial matching issues
    sorted_keys = sorted(PHONETIC_REPLACEMENTS.keys(), key=len, reverse=True)
    for key in sorted_keys:
        val = PHONETIC_REPLACEMENTS[key]
        # Use simple replace for literal text (including foreign phrases)
        text = text.replace(key, val)
    return text

def clean_markdown_and_html(text):
    # Remove HTML space markers
    text = text.replace("&nbsp;", "")
    
    # Remove bold markers
    text = text.replace("**", "")
    
    # Remove italic markers
    text = text.replace("*", "")
    
    return text

def convert_headers(text, is_ssml=False):
    # Match headers like "### I. THE FRAME"
    def repl(match):
        header_text = match.group(1).strip()
        
        # Translate roman numerals to spoken text
        header_text = re.sub(r'^I\.\s+', "Section One: ", header_text)
        header_text = re.sub(r'^II\.\s+', "Section Two: ", header_text)
        header_text = re.sub(r'^III\.\s+', "Section Three: ", header_text)
        header_text = re.sub(r'^IV\.\s+', "Section Four: ", header_text)
        header_text = re.sub(r'^V\.\s+', "Section Five: ", header_text)
        header_text = re.sub(r'^VI\.\s+', "Section Six: ", header_text)
        header_text = re.sub(r'^VII\.\s+', "Section Seven: ", header_text)
        
        if is_ssml:
            return f"\n{header_text}.\n<break time=\"2.0s\"/>\n"
        else:
            return f"\n{header_text}.\n[Pause: 2.0s]\n"
            
    return re.sub(r'^###\s+(.+)$', repl, text, flags=re.MULTILINE)

def main():
    print("Generating audio scripts...")
    
    # We will accumulate elements in list format
    txt_script_parts = [
        "YOU PROBABLY THINK THIS SONG IS ABOUT YOU TOO\n",
        "Written by Shane Brazelton\n",
        "[Pause: 3.0s]\n",
        "He is everyone and no one at the same time. That's not a riddle. That's the whole album.\n",
        "[Pause: 4.0s]\n"
    ]
    
    ssml_script_parts = [
        "<speak>",
        "YOU PROBABLY THINK THIS SONG IS ABOUT YOU TOO\n",
        "Written by Shane Brazelton\n",
        "<break time=\"3.0s\"/>\n",
        "He is everyone and no one at the same time. That's not a riddle. That's the whole album.\n",
        "<break time=\"4.0s\"/>\n"
    ]
    
    for filepath, spoken_title, prefix in TRACK_LIST:
        print(f"Processing {filepath}...")
        lyrics = extract_lyrics(filepath)
        
        # 1. Clean markdown formatting
        lyrics = clean_markdown_and_html(lyrics)
        
        # 2. Handle specific track modifications
        
        # Side A End of Playback
        if "track-002" in filepath:
            lyrics = lyrics.replace(
                "SIDE_A // END_OF_PLAYBACK",
                "End of Side A. End of playback."
            )
            
        # 3. Apply phonetics to the plain text script only
        lyrics_txt = apply_phonetics(lyrics)
        lyrics_ssml = lyrics # Keep original spellings in SSML, we can apply SSML tags or let the engine handle it with standard dictionary
        
        # Pepe's labored name pronunciation in hidden track
        if "track-hidden" in filepath:
            # For SSML: wrap the struggling name parts in a slow rate prosody tag
            lyrics_ssml = lyrics_ssml.replace("Pep.", "<prosody rate=\"50%\" pitch=\"-2st\">Pep.</prosody>")
            lyrics_ssml = lyrics_ssml.replace("Pepe.", "<prosody rate=\"50%\" pitch=\"-2st\">PEH-peh.</prosody>")
            
            # For Text: add a hint to help the AI actor
            lyrics_txt = lyrics_txt.replace("Pep.", "Pep. [slow and labored]")
            # Ensure "Pepe" -> "PEH-peh" is also slowed down
            lyrics_txt = lyrics_txt.replace("PEH-peh.", "PEH-peh. [slow and labored]")
            
        # Convert subheaders inside lyrics
        lyrics_txt = convert_headers(lyrics_txt, is_ssml=False)
        lyrics_ssml = convert_headers(lyrics_ssml, is_ssml=True)
        
        # Convert dividers
        # Convert triple dashes to breaks
        lyrics_txt = re.sub(r'^---$', "[Pause: 1.5s]", lyrics_txt, flags=re.MULTILINE)
        lyrics_ssml = re.sub(r'^---$', "<break time=\"1.5s\"/>", lyrics_ssml, flags=re.MULTILINE)
        
        # Append to script lists
        if prefix == "hidden":
            # Add 15 second silence before hidden track
            txt_script_parts.append("\n[A long fifteen second silence. Then, the spoken words:]\n")
            txt_script_parts.append(f"### {spoken_title}\n[Pause: 3.0s]\n")
            txt_script_parts.append(lyrics_txt)
            txt_script_parts.append("\n[Pause: 4.0s]\n")
            
            ssml_script_parts.append("\n<break time=\"10.0s\"/>\n<break time=\"5.0s\"/>\n")
            ssml_script_parts.append(f"{spoken_title}\n<break time=\"3.0s\"/>\n")
            ssml_script_parts.append(lyrics_ssml)
            ssml_script_parts.append("\n<break time=\"4.0s\"/>\n")
        else:
            txt_script_parts.append(f"### {spoken_title}\n[Pause: 3.0s]\n")
            txt_script_parts.append(lyrics_txt)
            txt_script_parts.append("\n[Pause: 4.0s]\n")
            
            ssml_script_parts.append(f"{spoken_title}\n<break time=\"3.0s\"/>\n")
            ssml_script_parts.append(lyrics_ssml)
            ssml_script_parts.append("\n<break time=\"4.0s\"/>\n")
            
    # Add help lines and sign-off at the end
    signoff_txt = (
        "[Pause: 3.0s]\n"
        "It's never too late to be Seen.\n"
        "[Pause: 3.0s]\n"
        "988. Suicide and Crisis Lifeline. Call or text, 24/7.\n"
        "741741. Crisis Text Line. Text H O M E.\n"
        "1-800-662-4357. SAMHSA National Helpline.\n"
        "[Pause: 3.0s]\n"
        "The door has a handle on your side.\n"
    )
    txt_script_parts.append(signoff_txt)
    
    signoff_ssml = (
        "<break time=\"3.0s\"/>\n"
        "It's never too late to be Seen.\n"
        "<break time=\"3.0s\"/>\n"
        "9 8 8. Suicide and Crisis Lifeline. Call or text, 24/7.\n"
        "7 4 1 7 4 1. Crisis Text Line. Text H O M E.\n"
        "1-800-662-4357. S A M H S A National Helpline.\n"
        "<break time=\"3.0s\"/>\n"
        "The door has a handle on your side.\n"
    )
    ssml_script_parts.append(signoff_ssml)
    ssml_script_parts.append("</speak>")
    
    # Save scripts
    txt_content = '\n'.join(txt_script_parts)
    # Fix double empty lines
    txt_content = re.sub(r'\n{3,}', '\n\n', txt_content)
    with open("compiled/audio_script_clean.txt", "w", encoding="utf-8") as f:
        f.write(txt_content)
    print("Saved clean text script: compiled/audio_script_clean.txt")
    
    ssml_content = '\n'.join(ssml_script_parts)
    # Fix double empty lines
    ssml_content = re.sub(r'\n{3,}', '\n\n', ssml_content)
    with open("compiled/audio_script.ssml", "w", encoding="utf-8") as f:
        f.write(ssml_content)
    print("Saved SSML script: compiled/audio_script.ssml")
    
    print("Audio script generation complete!")

if __name__ == "__main__":
    main()
