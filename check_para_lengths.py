import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    vc_list = [json.loads(line) for line in f if str(json.loads(line)['chapter']) == '1']
for c in vc_list:
    if c.get('para') in [3, 4, 5]:
        print(f"Para {c.get('para')}: {len(c['text'])} chars")
