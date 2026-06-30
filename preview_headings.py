import json

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Show first 8 chunks: heading vs text start
for c in chunks[:8]:
    print(f"HEADING: {c['heading']}")
    print(f"TEXT:    {c['text'][:120]}")
    print()
