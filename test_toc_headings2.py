import fitz
import re
import json
import os

doc = fitz.open(r'assigned pdfs\RAM 2022 Sixth Edition.pdf')
text = '\n'.join(doc[i].get_text() for i in range(1, 30))
lines = text.split('\n')

toc = {}
current_chapter = None
pending_num = None

for l in lines:
    l = l.strip()
    if not l: continue
    
    chap_match = re.search(r'CHAPTER\s+(\d+)|CHAPTER-(\d+)|CHAPTER\s+-\s+(\d+)', l, re.IGNORECASE)
    if chap_match:
        current_chapter = next(g for g in chap_match.groups() if g)
        if current_chapter not in toc:
            toc[current_chapter] = {}
        continue
    
    m_num_only = re.match(r'^(\d+(?:\.\d+)*\.?)$', l)
    if m_num_only:
        pending_num = m_num_only.group(1).rstrip('.')
        continue
        
    if pending_num:
        title = l.split('........')[0].strip()
        if current_chapter:
            toc[current_chapter][pending_num] = title
        pending_num = None
        continue
        
    m_same_line = re.match(r'^(\d+(?:\.\d+)*\.?)\s+(.*?)(?:\.{5,}\s*\d+)?$', l)
    if m_same_line:
        num = m_same_line.group(1).rstrip('.')
        title = m_same_line.group(2).split('........')[0].strip()
        if current_chapter:
            if current_chapter not in toc:
                toc[current_chapter] = {}
            toc[current_chapter][num] = title
        continue

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

matched = 0
not_matched = []

for i, c in enumerate(chunks):
    ch = c['chapter']
    h = c['heading']
    
    m = re.match(r'^(\d+(?:\.\d+)*\.?)\s*(.*)', h.strip())
    if m:
        num = m.group(1).rstrip('.')
        if ch in toc and num in toc[ch]:
            toc_title = toc[ch][num]
            c['heading'] = f"{num}. {toc_title}"
            matched += 1
        else:
            not_matched.append((i, ch, num, h))
    else:
        not_matched.append((i, ch, "NoNum", h))

print(f"Matched {matched} out of {len(chunks)} chunks.")
if not_matched:
    print(f"Could not match {len(not_matched)} chunks:")
    for i, ch, num, h in not_matched:
        print(f"  Chunk {i} | Ch {ch} | Num '{num}' | Orig: {h}")

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)

print("Updated file with TOC headings!")
