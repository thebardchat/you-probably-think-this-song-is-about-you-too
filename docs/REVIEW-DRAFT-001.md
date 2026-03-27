# REVIEW — draft-001.md (Complete Manuscript)
## 43,285 words | 3,835 lines | Read front to back March 27, 2026

---

## A. TTS PRONUNCIATION DICTIONARY

Every word that needs phonetic guidance for ElevenLabs. Build this into the audio script.

### Names (Characters)
| Word | Occurrences | Phonetic for TTS | Notes |
|------|-------------|------------------|-------|
| Pepe | 50+ | PEH-peh (not "peep") | Critical — entire ending depends on this landing |
| Brazelton | 2 | BRAZ-ul-ton (spell as "Brazzleton" in TTS) | Known fix from Vol 1 |
| Enzo Ferrara | 3 | EN-zoh feh-RAH-rah | |
| Sandro Luciano | 3 | SAHN-droh loo-CHAH-noh | |
| Luca Delvecchio | 5 | LOO-kah del-VEK-ee-oh | |
| Marco Ferretti | 4 | MAR-koh feh-RET-ee | |
| Tomás Aguilar | 4 | toh-MAHS ah-gee-LAR | Accent on á |
| Gianluca Parisi | 4 | jahn-LOO-kah pah-REE-see | |
| Rafael Mendes | 4 | hah-fah-EL MEN-dez | Brazilian Portuguese |
| Claudia | 4 | CLOW-dee-ah | |
| Davide | 2 | dah-VEE-deh | |
| Marta | 2 | MAR-tah | |
| Paulo | 3 | POW-loh | |
| Ciro | 1 (line 732) | CHEE-roh | |
| Gerald | 10+ | Standard English | Cat's name — fine as is |

### Places & Proper Nouns
| Word | Phonetic | Notes |
|------|----------|-------|
| San Siro | sahn SEE-roh | AC Milan's stadium |
| Villarreal | vee-yah-reh-AHL | Spanish football club |
| Salerno | sah-LAIR-noh | Italian city |
| Bari | BAH-ree | Italian city |
| Mayfair | Standard English | |
| São Paulo | sow POW-loh | Brazilian city |
| Napoli | NAH-poh-lee | Not "nah-POH-lee" |
| Pune | POO-neh (line 622) | Indian city, mentioned as comparison |
| Ibiza | ee-BEE-thah or ih-BEE-zah | Either acceptable |
| Valencia | vah-LEN-see-ah | |
| Antonio's | an-TOH-nee-ohs | The industry bar |
| CVS | See-Vee-Ess | Line 2740 — spoken as letters |

### Foreign Words & Phrases
| Word/Phrase | Language | Phonetic | Line |
|-------------|----------|----------|------|
| कोई क्या अपमान में मैं | Hindi | koy kyaa ap-MAAN mein main | 532, 3210 |
| आधा किया जी | Hindi | AAH-dhah kee-YAH jee | 534 |
| Muoviti | Italian | MWOH-vee-tee | 2052 |
| FRATELLO | Italian | frah-TEL-loh | 1740 |
| Aos irmãos. Aos que ficaram. Aos que voltaram. | Portuguese | owsh eer-MOWNS. owsh keh fee-KAH-rong. owsh keh vol-TAH-rong. | 1802, 1894 |
| irmão | Portuguese | eer-MOWNG | 1768 |
| grazie, Mamma | Italian | GRAH-tsee-eh, MAH-mah | 1820 |
| senhora | Portuguese | sen-YOR-ah | 1826 |
| limoncello | Italian | lee-mon-CHEL-loh | 2306+ |
| trattoria | Italian | trah-toh-REE-ah | 1744 |
| Pelé | Portuguese | peh-LEH | 1768 |

### English Words That May Mispronounce
| Word | Issue | Fix |
|------|-------|-----|
| Uber (14 occurrences) | TTS may say "uh-ber" or add emphasis on brand name | Consider replacing with "ride-share car" or "hired car" in some instances. Keep "Uber" where it's used as shorthand but verify ElevenLabs pronunciation |
| EGGUGH (line 179) | Nonsense word — TTS will not know what to do | Replace with phonetic description or recorded vocal sample. For TTS: try "EH-guh" or describe it as "a sound the mouth makes" |
| SIDE_A // END_OF_PLAYBACK (line 470) | TTS will read literally | Replace with: "Side A. End of playback." or just a long pause |
| panopticon (lines 2358, 2430) | May mispronounce | pan-OP-tih-kon |
| epistemology (line 2566) | May stumble | eh-PIST-eh-MOL-oh-jee |
| jigger (lines 2292, 2444) | Bartending tool — may mispronounce | JIG-er (standard) |

### Markdown Artifacts to Strip for Audio Script
| Artifact | Lines | Fix |
|----------|-------|-----|
| `&nbsp;` | 8, 12, 3153, 3507-3518, 3802-3824 | Remove — replace with timed silence (2-3 seconds) |
| `**bold text**` | 283-303, 470, 3816-3818 | Strip asterisks — TTS reads them |
| `### section headers` | 269, 281, 310, 324, 356, 430, 456, 1960, 2086, 2130 | Strip hashes — replace with 3-second pause |
| `---` horizontal rules | Throughout (~200 occurrences) | Replace with 1.5-second pause |
| `*italicized text*` | Throughout | Strip single asterisks — TTS may read them. ElevenLabs usually handles these OK but verify |
| `## SIDE A`, `## SIDE B`, `## BONUS TRACK` | 16, 483, 3157 | Read as spoken text with dramatic pause before |

---

## B. CONTINUITY ISSUES

### B1. Track 002 → Track 003 Echo (Lines 464-490)
**Track 002 ends:** "He came back down. He always comes back down."
**Track 003 opens:** "He came back down. Always comes back down."

This is intentional echo — confirmed. But in continuous reading/listening it may feel like a repeat error. **Decision needed:** Is this the effect you want? If yes, the TTS pause between tracks will help separate them. If the audiobook has chapter markers, the listener will understand.

### B2. Track 002 Section V — Dark Room Monologue (Lines 366-420)
This is raw-voice-adjacent material. Some lines are transcription artifacts that read oddly:
- Line 410: *"What I loan to be anywhere else puts back in with you"* — unclear meaning. Was this what Shane said? Does it land?
- Line 384: *"I feel this red count"* vs Line 386: *"I feel the dead count"* — intentional? Or transcription confusion?
- Line 400: *"you were missing a connection and finding it an obsession"* — powerful line, lands well
- **Overall:** The fragmented, almost-broken quality of this monologue is its strength. It sounds like a man talking to someone who can't hear him. The question is whether the unclear lines add to that or pull the listener out.

### B3. The "Seven" vs "Eight" Count
- Track 002 introduces "The Simultaneous Seven" but lists EIGHT groups (couple, beggar, waiter, waitress+bartender, solitary man, Uber arrival, four screens)
- The waitress and bartender are counted as one unit in the header ("The Waitress and the Bartender")
- Track 006 says "Seven people in a frame"
- Track 014 reveals the detective as "the eighth figure. The one nobody counted."
- **This works.** The seven is the diner cast. The detective is the uncounted eighth. The four screens couple doesn't get inhabited and fades from later tracks. Continuity holds.

### B4. Track 004 — "Pune" Reference (Line 622)
"Beautiful the way Pune is beautiful — soft, specific, not asking for anything."
- This is from the solitary man's inhabitation. The reference to Pune (Indian city) is unexpected. Is this a raw voice artifact from Shane's dump, or was it shaped? If raw, keep it — it's the solitary man's mind, not the detective's. If shaped, it could be a reach that breaks the European setting for a moment.

### B5. Track 009 — "Volume One" Direct Reference (Line 1544)
"The kind of armor the doctor in Volume One would recognize: *sophisticated, also armor, the armor has good taste.*"
- This breaks the fourth wall. The text says "Volume One" explicitly. In an audiobook, this will land as the narrator acknowledging this is a book. **Is this intentional meta-commentary?** If so, it's effective. If not, change to "the kind of armor the doctor would recognize" (remove "in Volume One").

### B6. Track 011 — "the same album track" (Line 2138)
"none of them knowing that they were inside the same second, the same groove, the same album track"
- Another meta-reference. The characters are described as being inside an "album track." This is consistent with the album-as-structure conceit but could break immersion in audio. **Shane's call.**

### B7. Track 013 — "CVS" Reference (Line 2740)
"a man was recording while walking and driving and buying things at CVS"
- This breaks the noir European setting by referencing an American store chain. It works because it's the dream track and it's meta — the detective is inside a story inside a stapler inside a dream. But in audio, "CVS" might pull the listener out of the European diner world. **Shane's call — it's very Shane, which may be exactly why it stays.**

### B8. Hidden Track → Bonus Track Ordering
In the compiled manuscript, the Bonus Track (Dr. Seen Returns) comes BEFORE the hidden track. This means Dr. Seen examines the detective, then the hidden track reveals the detective inside Dr. Seen. The reader gets the clinical assessment first, then the experiential version.
- **This works narratively** — you hear the doctor's professional analysis, then you FEEL what it's like to be the doctor looking at this man on the couch. The bonus track sets up the hidden track's gut punch.
- **But:** The bonus track mentions the detective walking out and checking his hands (lines 3462-3470). Then the hidden track shows another session where he does the same thing. This could feel repetitive. **Consider:** Does the reader understand these are different Wednesdays? The hidden track says "months of Wednesdays" (line 3570) which clarifies it's an ongoing pattern, not a repeat of the same day.

---

## C. PROSE ISSUES — LINE BY LINE

### C1. Line 1144 — "shewing"
"And the waiter was shewing the beggar."
- "Shewing" is archaic for "shooing." TTS will pronounce it "SHOO-ing" or "SHEW-ing." **Replace with "shooing"** unless the archaic spelling is intentional.

### C2. Line 189 — "The procrastinators used the procrastinators"
"The farmers used it as an excuse not to plant. The procrastinators used the procrastinators as an excuse not to plant."
- This reads like a typo. Should the second use be "The procrastinators used *it*" or is this intentional wordplay (procrastinators using other procrastinators as their excuse)? If intentional, it's clever. If typo, fix.

### C3. Lines 2790-2796 — Double Exhale
"The detective exhaled. South of the lungs. --- He exhaled too. The big sigh."
- "He exhaled too" after "The detective exhaled" reads like two different people exhaling, but it's the same person. The "too" implies he's exhaling alongside the planet. This works but may confuse on first listen. **Consider:** "He exhaled. The big sigh." (remove "too")

### C4. Track 014 — "Let's Twist Again" (Lines 3130-3146)
- This references the Chubby Checker song. **Copyright consideration:** The phrase "Let's twist again, like we did last summer" is a song lyric. Using it in a published book/audiobook may require licensing or attribution. **Check before publication.** If it's a problem, the passage can be rewritten to evoke without quoting.

---

## D. STRUCTURAL OBSERVATIONS

### D1. Album Length
43,285 words / 4h21m audio. This is the length of a full novel. Volume One was 12,800 words / 78 minutes. Volume Two is 3.4x the length. **Is this the right length?** Some tracks could be tightened without losing impact. Tracks 009 (The Tip), 011 (The Shift), and 012 (The Pour) are the longest and most detailed. They're also some of the best writing in the album. But for audiobook pacing, consider whether the listener stays locked in for 4+ hours.

### D2. The Four Screens
The "Four Screens" group from Track 002's Simultaneous Seven disappears entirely after Track 002. They're never inhabited. They don't appear in the "none of it happened" recaps. They're the only member of the seven that gets dropped. **Is this intentional?** If so, it works — they were always the background noise. If it should be addressed, a brief mention in Track 008's "none of it happened" litany could include them.

### D3. Sidetrack Placement
The Sidetrack interlude sits between Track 000 and Track 001. In Volume One, interludes sat between acts. The Sidetrack's current placement works well as an album intro — it's the "grand entrance through the side door." But consider: in audio, does the listener want two preambles (000 + Sidetrack) before the first real track? Or does the combined effect of 000 → Sidetrack → 001 create the right slow build?

---

## E. AUDIO SCRIPT RECOMMENDATIONS

For the ElevenLabs script:

1. **Create a pronunciation dictionary file** — map every foreign word and proper noun to phonetic spelling
2. **Replace all markdown** — strip headers, bold, italic markers, horizontal rules
3. **Convert `---` to `<break time="1.5s"/>` or equivalent SSML**
4. **Convert `&nbsp;` sections to `<break time="3s"/>`**
5. **Add chapter markers** between tracks for audiobook navigation
6. **SIDE_A // END_OF_PLAYBACK** — replace with a spoken "End of Side A" with 5-second silence, or just a long pause
7. **Hindi text (lines 532, 534, 3210)** — either:
   - Use SSML language switching if ElevenLabs supports it
   - Pre-record the Hindi lines separately and splice in
   - Use romanized phonetic in the script
8. **"Pep. Pep. Pep. Pepe."** — this needs to be slow, labored, struggling. Add SSML rate/prosody tags to slow the delivery
9. **Track 013 (The Dream)** — consider a slightly different vocal quality or reverb to signal the dream state
10. **Hidden Track** — add 10-15 seconds of silence before it begins

---

## F. DECISIONS NEEDED FROM SHANE

1. **Line 410** — Dark Room: "What I loan to be anywhere else puts back in with you" — keep or clarify?
2. **Line 189** — "procrastinators used the procrastinators" — typo or wordplay?
3. **Line 1144** — "shewing" → "shooing"?
4. **Line 1544** — "Volume One" reference — keep meta or remove?
5. **Line 2138** — "album track" reference — keep meta or remove?
6. **Line 2740** — "CVS" reference — keep or change?
7. **Lines 3130-3146** — "Let's Twist Again" — copyright check needed?
8. **Uber pronunciation** — replace with "hired car" in some spots or keep all as "Uber"?
9. **EGGUGH** — how should TTS handle this? Phonetic? Description? Skip?
10. **Album length** — 4h21m at current length. Trim or keep?
11. **Four Screens** — address their disappearance or let them fade?
12. **B2/B8** — any Dark Room lines or bonus→hidden overlap that need adjustment?

---

## G. VERDICT

The prose is strong. The structure is sound. The calm place breadcrumbs build perfectly — from whisper to full reveal. The hidden track lands like a hammer. Pepe in the alley is devastating. The "It's never too late to be Seen" sign-off ties both volumes together with a punch.

The main work before ElevenLabs is:
1. Build the TTS pronunciation dictionary
2. Strip markdown for audio script
3. Shane answers the 12 decisions above
4. Generate the audio with proper SSML markup

This hits.
