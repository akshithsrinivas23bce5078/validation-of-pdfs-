import json
import fitz
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i, c in enumerate(chunks):
    if str(c.get('chapter')) == '2' and str(c.get('para')) in ['1', '2', '3', '4', '5']:
        print(f"Para {c.get('para')}: len = {len(c.get('text', ''))}")
