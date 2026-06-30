import json

count_empty = 0
with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        if c['chapter'] in ['8', '21']:
            print(f"Ch {c['chapter']} | Req {c['heading']} | text_len={len(c['text'])}")
            if len(c['text']) < 30 and not c.get('has_table'):
                count_empty += 1
                
print(f"Total empty in 8 and 21: {count_empty}")
