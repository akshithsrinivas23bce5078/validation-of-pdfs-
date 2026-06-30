import json
import re
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

fixed = 0
for c in chunks:
    text = c.get('text', '')
    if text:
        # Match trailing space followed by 1 to 4 digits at the end of the string
        # Also handle cases where there might be some trailing whitespace after the digits
        new_text = re.sub(r'\s+\d{1,4}\s*$', '', text)
        if new_text != text:
            c['text'] = new_text
            fixed += 1

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print(f"Fixed trailing page numbers in {fixed} chunks.")
