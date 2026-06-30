import json
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TNPSC_AF_Rule_2022_chunks.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# We drop the first chunk (Gazette Notification) and the last two chunks (Appendix forms)
# So we only keep chunks[1], chunks[2], chunks[3]
valid_chunks = chunks[1:4]

out_chunks = []
headings = [
    "1. Short Title",
    "2. Definitions",
    "3. Form of Requisition"
]

text_prefixes = [
    "1. Short title.- ",
    "2. Definitions.- ",
    "3. Form of Requisition.- "
]

for i, c in enumerate(valid_chunks):
    chunk = {
        "DOC_NAME": "TNPSC_AF_Rule_2022",
        "doc_id": "TNPSC-C989A22522",
        "chapter": "1",
        "title": "Tamil Nadu Public Service Commission (Additional Functions) Rule, 2022",
        "heading": headings[i],
        "text": text_prefixes[i] + c.get('text', ''),
        "page.no": c.get('page.no', '(1-1)'),
        "has_table": False,
        "table_html": "{}"
    }
    out_chunks.append(chunk)

out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TNPSC_AF_Rule_2022_validated.jsonl'
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as f:
    for c in out_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(out_chunks)} chunks in {out_path}")
