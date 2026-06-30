import json

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        if str(c['chapter']) == '3':
            text = c.get('text', '')
            para = c.get('para')
            title = c.get('heading')
            print(f"[{para}] {title}")
            print(f"START: {text[:80]}")
            print(f"END: {text[-80:]}")
            print("-" * 50)
