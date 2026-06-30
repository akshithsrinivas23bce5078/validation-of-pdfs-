import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    vc_list = [json.loads(line) for line in f if str(json.loads(line)['chapter']) == '1']
for i, c in enumerate(vc_list):
    print(f"[{i}] {c['heading']}: {len(c['text'])} chars")
