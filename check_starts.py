import json

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i in range(207, 216):
    text = chunks[i].get('text', '')
    print(f"Chunk {i} (Para {chunks[i]['para']}) starts with: {repr(text[:50])}")
