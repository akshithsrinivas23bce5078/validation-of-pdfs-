import fitz
import re
import json

doc = fitz.open(r'assigned pdfs\RAM 2022 Sixth Edition.pdf')
text = '\n'.join(doc[i].get_text() for i in range(5, 30))
lines = text.split('\n')

toc_headings = []
current_chapter = "0"
for l in lines:
    chap_match = re.search(r'CHAPTER\s+(\d+)', l, re.IGNORECASE)
    if chap_match:
        current_chapter = chap_match.group(1)
        
    m = re.match(r'^(\d+(?:\.\d+)*)\s+(.*?)(?:\.{5,}\s*\d+)?$', l.strip())
    if m:
        num = m.group(1)
        title = m.group(2).strip().split('........')[0].strip()
        toc_headings.append((current_chapter, num, title))

print(f"Extracted {len(toc_headings)} headings from TOC")

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

matched = 0
for c in chunks:
    ch = c.get('chapter')
    h = c.get('heading', '')
    prefix_match = re.match(r'^(\d+(?:\.\d+)*)\s*(.*)', h)
    if prefix_match:
        num = prefix_match.group(1)
        # Find this number in the toc_headings for the same chapter
        for toc_ch, toc_num, toc_title in toc_headings:
            if toc_ch == ch and toc_num == num:
                c['heading'] = f"{num} {toc_title}"
                matched += 1
                break

print(f"Matched and corrected {matched} headings out of {len(chunks)}")
