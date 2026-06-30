import json
import codecs

def decode_unicode(text):
    return text.encode('utf-8').decode('unicode_escape')

out = []
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        # Fix unicode
        for k in ['text', 'heading', 'title']:
            if c.get(k):
                try:
                    c[k] = c[k].encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
                except:
                    pass
        
        ch = str(c.get('chapter', '')).strip()
        if ch in ['21', '22'] or 'RDSO' in str(c.get('title', '')) or 'E-Office' in str(c.get('title', '')):
            out.append(c)

with open('debug_ch21_22.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
