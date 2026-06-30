import json
import re

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

lines = open(file_path, 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    data = json.loads(line)
    text = data.get('text', '')
    p = data.get('para', 0)
    
    # Check if text contains the para number followed by some uppercase text
    # e.g., '27. REMISSION ON ACCOUNT OF'
    m = re.search(r'\b' + str(p) + r'\.\s+([A-Z][A-Z0-9\s\-]+)', text[:200])
    if m:
        title = m.group(1).strip()
        if len(title) > 5:
            print(f'Para {p} (line {i}): text contains heading -> {title!r}')
            print(f'   Current heading: {data.get("heading")}')
