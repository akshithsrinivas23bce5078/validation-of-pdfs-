import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    vc_list = [json.loads(line) for line in f if str(json.loads(line)['chapter']) == '1']
indices = [0]
for c in vc_list:
    indices.append(indices[-1] + len(c['text']))
for i, c in enumerate(vc_list):
    print(f"{c['para']}: idx {indices[i]}")
