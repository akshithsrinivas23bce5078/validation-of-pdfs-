import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    vc_list = [json.loads(line) for line in f if str(json.loads(line)['chapter']) == '2' and json.loads(line).get('para') in [59,60,61,62,63]]
for c in vc_list:
    print(f"Para {c.get('para')} length: {len(c['text'])}")
