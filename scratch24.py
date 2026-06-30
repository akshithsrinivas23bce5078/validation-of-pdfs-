import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

subject_paras = {
    23, 43, 44, 77, 131, 5, 16, 20, 60, 4, 8, 64, 71, 72, 76, 91, 110, 61, 62, 51, 27, 11, 33
}

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('Possible split headings:')
for l in lines:
    data = json.loads(l)
    p = data.get('para', 0)
    if p in subject_paras:
        continue
    t = data.get('text', '').strip()
    match = re.match(r'^([A-Z\s\’\'-]{15,})\b', t)
    if match:
        print(f"Para {p}: {t[:50]}...")
