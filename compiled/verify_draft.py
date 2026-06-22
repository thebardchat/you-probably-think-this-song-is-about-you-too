import os
import re

def verify_manuscript():
    manuscript_path = "compiled/draft-006.md"
    if not os.path.exists(manuscript_path):
        print(f"Error: Manuscript not found at {manuscript_path}. Run compile_uncut.py first.")
        return False
        
    print(f"Verifying {manuscript_path}...")
    with open(manuscript_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    words = content.split()
    word_count = len(words)
    print(f"-> Word count: {word_count} words")
    
    # Check headers
    tracks = re.findall(r"^### Track \d+ — .+$|^### Dr. Seen Returns$|^### Sidetrack$", content, re.MULTILINE)
    print(f"-> Found {len(tracks)} track headings in manuscript.")
    
    # Check for metadata leak
    leaks = []
    for line in content.split("\n"):
        if re.search(r"^## Lyrics|^## Liner Notes|^\*\*Status:\*\*|^\*\*Themes:\*\*|^\*\*Connects To:\*\*|^Status:|^Themes:", line, re.IGNORECASE):
            leaks.append(line)
            
    if leaks:
        print(f"Error: Found {len(leaks)} leaked metadata lines:")
        for leak in leaks[:10]:
            print(f"  {leak}")
        return False
    else:
        print("-> No metadata leaks found.")
        
    # Check helpline counts
    helpline_mentions = content.count("Suicide & Crisis Lifeline")
    print(f"-> Helpline printed {helpline_mentions} time(s).")
    if helpline_mentions != 1:
        print(f"Error: Helplines must appear exactly once. Found: {helpline_mentions}")
        return False
        
    # Check transitions
    # Transitions should be: \n&nbsp;\n\n---\n\n
    # Let's count standard dividers
    dividers = content.count("\n---\n")
    print(f"-> Found {dividers} horizontal dividers.")
    
    print("\nVerification successful! The manuscript structure is clean and correct.")
    return True

if __name__ == "__main__":
    verify_manuscript()
