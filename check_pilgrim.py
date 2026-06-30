import json

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

found = False
for c in chunks:
    if 'Pilgrim tax' in c['text'] or 'Pilgrim Tax' in c['text']:
        print(f"Found Pilgrim Tax inside heading: {c['heading']}")
        found = True

if not found:
    print("Pilgrim Tax text not found in ANY chunk!")
