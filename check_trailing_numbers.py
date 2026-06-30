import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i, c in enumerate(chunks):
    text = c.get('text', '')
    if re.search(r'\s+\d{1,3}\s*$', text):
        print(f"Chunk {i}: ends with {repr(text[-20:])}")
