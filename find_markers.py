import json
import re

output_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated.jsonl'
with open(output_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for ch in ['1']:
    c_chunks = [c for c in chunks if c['chapter'] == ch]
    print(f'--- Chapter {ch} ---')
    for c in c_chunks:
        h = c['heading']
        t = c['text']
        if re.search(r'Para\s*-?\s*\d+', h, re.IGNORECASE) or re.search(r'Para\s*-?\s*\d+', t[:50], re.IGNORECASE):
            print(f"ID: {c['chunk_id']} | H: {h[:40]} | T: {t[:40].replace(chr(10), ' ')}")
