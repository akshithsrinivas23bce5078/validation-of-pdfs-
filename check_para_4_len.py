import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        if c.get('para') == 4 and str(c['chapter']) == '1':
            print(f"Para 4 length: {len(c['text'])}")
            print(c['text'][:100])
