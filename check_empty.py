import json
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    vc_list = [json.loads(line) for line in f]
empty_count = 0
for c in vc_list:
    if len(c['text']) == 0:
        print(f"Chapter {c['chapter']} Para {c.get('para')} is empty!")
        empty_count += 1
if empty_count == 0:
    print("No empty chunks found! Everything is perfectly aligned!")
