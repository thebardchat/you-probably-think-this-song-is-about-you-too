import os
import re
import sys

def main():
    try:
        import win32com.client
    except ImportError:
        print("Error: pywin32 is required to run Windows SAPI speech synthesis.")
        print("Please run: pip install pywin32")
        sys.exit(1)

    clean_script_path = "compiled/audio_script_clean.txt"
    output_wav_path = "compiled/BOOK-PREVIEW.wav"

    if not os.path.exists(clean_script_path):
        print(f"Error: Clean script not found at {clean_script_path}. Run generate_audio_script.py first.")
        sys.exit(1)

    print(f"Reading {clean_script_path}...")
    with open(clean_script_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Convert text to SAPI XML format
    print("Preparing SAPI XML text...")
    
    # Escape special characters that would break XML parser
    escaped_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 1. Clean up brackets like [slow and labored] or [Pause: X.Xs]
    # We translate [Pause: X.Xs] to SAPI XML silence tag
    def pause_repl(match):
        seconds = float(match.group(1))
        msec = int(seconds * 1000)
        return f'<silence msec="{msec}"/>'

    xml_text = re.sub(r'\[Pause:\s*([\d\.]+)s\]', pause_repl, escaped_text)
    
    # Replace the 15-second silence note with a silence tag
    xml_text = re.sub(r'\[A long fifteen second silence\..*?\]', '<silence msec="15000"/>', xml_text)
    
    # Strip out any remaining bracketed actor instructions
    xml_text = re.sub(r'\[.*?\]', '', xml_text)
    
    # Wrap track headings in SAPI silence tags for breathing room
    def header_repl(match):
        header_text = match.group(1).strip()
        return f'<silence msec="1500"/>{header_text}<silence msec="1500"/>'
        
    xml_text = re.sub(r'^###\s+(.+)$', header_repl, xml_text, flags=re.MULTILINE)

    # Wrap the entire text in a standard SAPI speech tag
    xml_content = f"<speech>{xml_text}</speech>"

    print(f"Initializing SAPI voice...")
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        
        # Select voice (standard Microsoft voices like David or Zira)
        # We can find available voices if needed
        voices = speaker.GetVoices()
        print(f"Available voices:")
        for idx, voice in enumerate(voices):
            description = voice.GetDescription()
            print(f"  [{idx}] {description}")
            
        # Select the first voice by default
        if len(voices) > 0:
            speaker.Voice = voices[0]
            print(f"Selected voice: {voices[0].GetDescription()}")
            
        # Setup file stream for writing to WAV
        print(f"Rendering audio to {output_wav_path} (this may take a few minutes)...")
        filestream = win32com.client.Dispatch("SAPI.SpFileStream")
        
        # 3 = SSFMCreateForWrite
        filestream.Open(output_wav_path, 3, False)
        speaker.AudioOutputStream = filestream
        
        # 8 = SPF_IS_XML
        speaker.Speak(xml_content, 8)
        
        filestream.Close()
        print("Rendering complete!")
        print(f"File saved successfully at: {os.path.abspath(output_wav_path)}")
        
    except Exception as e:
        print(f"Error occurred during TTS rendering: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
