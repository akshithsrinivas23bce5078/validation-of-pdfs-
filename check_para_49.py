import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    vc_list = [json.loads(line) for line in f if str(json.loads(line)['chapter']) == '2' and json.loads(line).get('para') == 49]
for c in vc_list:
    print(f"Para 49 Length: {len(c['text'])}")
    print(c['text'][:150])
