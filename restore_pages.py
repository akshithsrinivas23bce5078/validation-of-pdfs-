import json
import re

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

toc_path = r'parsed_toc.json'
with open(toc_path, 'r', encoding='utf-8') as f:
    toc = json.load(f)

def get_para_num(heading):
    m = re.match(r'Para\s+(\d+)', heading, re.IGNORECASE)
    if m: return int(m.group(1))
    return 0

for c in chunks:
    ch = str(c['chapter'])
    num = get_para_num(c['heading'])
    
    # Find page from toc
    page = 0
    if ch in toc:
        for p in toc[ch]:
            if p['para'] == num:
                page = p['page']
                break
                
    if page != 0:
        c['page_number'] = page

errors = 0
for i, c in enumerate(chunks):
    if not isinstance(c.get('page_number'), int) or c.get('page_number') <= 0:
        print(f"Chunk {i} STILL has invalid page_number: {c.get('page_number')}")
        errors += 1

if errors == 0:
    print("SUCCESS: All page numbers restored perfectly.")
    
with open(path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
