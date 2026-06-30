import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# We use a targeted approach to avoid merging legitimate words.
# We look for common OCR split suffixes that are capitalized.
patterns = [
    (re.compile(r'([a-zA-Z]+)\s+Tion\b'), r'\1tion'),
    (re.compile(r'([a-zA-Z]+)\s+Ise\b'), r'\1ise'),
    (re.compile(r'([a-zA-Z]+)\s+Ion\b'), r'\1ion'),
    (re.compile(r'([a-zA-Z]+)\s+Ing\b'), r'\1ing'),
    (re.compile(r'([a-zA-Z]+)\s+Nt\b'), r'\1nt'),
    (re.compile(r'([a-zA-Z]+)\s+Iage\b'), r'\1iage'),
    (re.compile(r'([a-zA-Z]+)\s+N\b'), r'\1n'),
    (re.compile(r'([a-zA-Z]+)\s+Ment\b'), r'\1ment'),
    (re.compile(r'([a-zA-Z]+)\s+Ly\b'), r'\1ly'),
    (re.compile(r'([a-zA-Z]+)\s+Ies\b'), r'\1ies'),
    (re.compile(r'([a-zA-Z]+)\s+Ed\b'), r'\1ed'),
    (re.compile(r'([a-zA-Z]+)\s+Er\b'), r'\1er'),
    (re.compile(r'([a-zA-Z]+)\s+Al\b'), r'\1al'),
]

fixed_count = 0
for c in chunks:
    for field in ['heading', 'text']:
        text = c.get(field, '')
        if text:
            new_text = text
            for pattern, repl in patterns:
                # We need to ensure we don't match things like "a N" or "I N"
                # We will only replace if the first group is > 2 characters.
                def replace_func(m):
                    if len(m.group(1)) >= 3:
                        return m.group(1) + repl.replace(r'\1', '')
                    return m.group(0)
                new_text = pattern.sub(replace_func, new_text)
            
            if new_text != text:
                print(f"Fixed in {field}: '{text}' -> '{new_text}'")
                c[field] = new_text
                fixed_count += 1

import os
with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print(f"Fixed split words in {fixed_count} places.")
