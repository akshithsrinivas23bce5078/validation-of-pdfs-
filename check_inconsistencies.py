import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
REPORT_FILE = r'inconsistencies_report.md'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

incomplete_endings = []
short_chunks = []
abnormal_chars = []

# Known valid special characters like Rupee (₹), n-dash, m-dash, smart quotes
valid_special_chars = r'\x00-\x7F\u2013\u2014\u2018\u2019\u201C\u201D\u20A8\u00A0\u20B9'

for i, c in enumerate(chunks):
    text = c.get('text', '').strip()
    ch = c.get('chapter', '?')
    h = c.get('heading', '?')
    
    # 1. Short chunks (less than 50 chars)
    if len(text) < 50:
        short_chunks.append((i, ch, h, len(text), text))
        
    # 2. Incomplete endings (doesn't end with proper punctuation)
    if text and not re.search(r'[.!?\"\')\]]$', text[-10:].strip()):
        incomplete_endings.append((i, ch, h, text[-50:]))
        
    # 3. Abnormal characters (excluding the standard ones)
    if re.search(f'[^{valid_special_chars}]', text):
        bad_chars = set(re.findall(f'[^{valid_special_chars}]', text))
        abnormal_chars.append((i, ch, h, list(bad_chars)))

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    f.write("# RAM 2022 JSONL Inconsistencies Report\n\n")
    f.write(f"Total chunks checked: {len(chunks)}\n\n")
    
    f.write(f"## 1. Short Chunks (< 50 chars) ({len(short_chunks)})\n")
    f.write("Chunks with very little content that might indicate missing extraction.\n\n")
    for idx, ch, h, length, t in short_chunks:
        f.write(f"- **Ch {ch}** - {h} (Index {idx}, {length} chars): `{t}`\n")
        
    f.write(f"\n## 2. Incomplete / Abrupt Endings ({len(incomplete_endings)})\n")
    f.write("Chunks whose text does not end with a standard punctuation mark (e.g., . ! ?).\n\n")
    for idx, ch, h, t_end in incomplete_endings:
        # replace newlines in t_end for display
        t_end = t_end.replace('\n', ' ')
        f.write(f"- **Ch {ch}** - {h} (Index {idx}): `...{t_end}`\n")
        
    f.write(f"\n## 3. Abnormal/Special Unicode Characters ({len(abnormal_chars)})\n")
    f.write("Chunks containing non-standard ASCII/Unicode characters (e.g., OCR artifacts, bullets).\n\n")
    for idx, ch, h, chars in abnormal_chars:
        # Represent the chars in a readable format using unicode escape
        char_list = [c.encode('unicode_escape').decode('utf-8') for c in chars]
        f.write(f"- **Ch {ch}** - {h} (Index {idx}): `{char_list}`\n")

print(f"Report written to {REPORT_FILE}")
