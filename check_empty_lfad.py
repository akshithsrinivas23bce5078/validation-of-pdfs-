import json

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i, c in enumerate(chunks):
    text = c.get('text', '').strip()
    if len(text) < 50:
        print(f"Chunk {i} ({c.get('heading')}): len={len(text)} | text: {repr(text)}")
