import json
import fitz
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i, c in enumerate(chunks):
    if i in [150, 151, 152, 153]:
        print(f"Para {c['para']} - {c['title']} (Expected Page: {c.get('page', 'Unknown')})")
