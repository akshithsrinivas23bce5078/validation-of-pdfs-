import json
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

replacements = {
    '\uf0b7': '- ',
    '\uf0fc': '- ',
    '\uf0e0': '- ',
    '\u2713': '- ',
    '\u201f': '"',
    '\u2026': '...',
    '\xe0': 'a'
}

fixed = 0
for c in chunks:
    text = c.get('text', '')
    if text:
        new_text = text
        for old, new in replacements.items():
            new_text = new_text.replace(old, new)
        
        if new_text != text:
            c['text'] = new_text
            fixed += 1

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print(f"Normalized unicode characters in {fixed} chunks.")
