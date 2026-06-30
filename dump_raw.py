import json

texts = []
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed_original_backup.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        if c.get('chapter') in ['21', '22']:
            texts.append(c.get('text', ''))

with open('raw_text_21_22.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n---CHUNK---\n\n'.join(texts))
