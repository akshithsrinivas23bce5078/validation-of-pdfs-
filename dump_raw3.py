import json

texts = []
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        ch = str(c.get('chapter', '')).strip()
        if ch in ['21', '22'] or 'RDSO' in str(c.get('title', '')) or 'E-Office' in str(c.get('title', '')) or 'Research Designs and Standards Organization' in str(c.get('title', '')):
            t = c.get('text', '')
            try:
                t = t.encode('utf-8').decode('unicode_escape')
            except:
                pass
            texts.append(t)

with open('raw_text_21_22.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n---CHUNK---\n\n'.join(texts))
