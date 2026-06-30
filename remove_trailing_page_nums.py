import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

count = 0
for c in chunks:
    text = c.get('text', '')
    m = re.search(r'\s+(\d{1,4})\s*$', text)
    if m:
        c['text'] = re.sub(r'\s+\d{1,4}\s*$', '', text)
        print(f"Removed trailing number {m.group(1)} from Para {c.get('para')}")
        count += 1

print(f"Removed {count} trailing page numbers.")

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
