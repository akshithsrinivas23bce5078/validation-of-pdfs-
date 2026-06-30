import json

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Show current state
for c in chunks[:3]:
    print(f"doc_name: {c['doc_name']}")
    print(f"chapter: {c['chapter']}, page_number: {c['page_number']}")
    print()

# Also check a few from other chapters
for c in chunks:
    if str(c['chapter']) == '2' and c.get('para') == 1:
        print(f"Ch2 Para1 -> doc_name: {c['doc_name']}, page_number: {c['page_number']}")
    if str(c['chapter']) == '3' and c.get('para') == 1:
        print(f"Ch3 Para1 -> doc_name: {c['doc_name']}, page_number: {c['page_number']}")
    if str(c['chapter']) == '4' and c.get('para') == 1:
        print(f"Ch4 Para1 -> doc_name: {c['doc_name']}, page_number: {c['page_number']}")
