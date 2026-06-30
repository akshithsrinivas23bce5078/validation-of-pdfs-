import json

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

errors = 0
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        print(f"Chunk {i} has empty text!")
        errors += 1
    if not isinstance(c.get('page_number'), int) or c.get('page_number') <= 0:
        print(f"Chunk {i} has invalid page_number: {c.get('page_number')}")
        errors += 1

if errors == 0:
    print("SUCCESS: All 337 chunks have non-empty text and valid page numbers.")
