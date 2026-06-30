import json
import re
import fitz

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
PDF_FILE = r'assigned pdfs\RAM 2022 Sixth Edition.pdf'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

doc = fitz.open(PDF_FILE)
total_pages = len(doc)
full_text = ""
for pg in range(total_pages):
    full_text += doc[pg].get_text() + '\n'

def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

targets = [
    (18, '3', '2.'), (225, '9', '5.'), (234, '9', '7.'), (250, '10', '4.'),
    (303, '11', '8.12'), (306, '12', '1.1'), (345, '12', '7.25'), (389, '15', '2.3'), (503, '21', '8.19')
]

for idx, ch, heading_prefix in targets:
    # First find the chapter to narrow the search space
    ch_marker = f"CHAPTER {ch}"
    ch_idx = full_text.find(ch_marker)
    if ch_idx == -1:
        ch_idx = full_text.find(f"Chapter {ch}")
    
    if ch_idx != -1:
        search_area = full_text[ch_idx:ch_idx+30000] # Search next 30k chars
    else:
        search_area = full_text
        
    escaped = re.escape(heading_prefix)
    
    # Try finding the exact heading line
    heading_line = chunks[idx].get('heading', '')
    if len(heading_line) > 5:
        m = re.search(re.escape(heading_line[:20]), search_area, re.IGNORECASE)
    else:
        m = None
        
    if not m:
        m = re.search(r'(?:^|\n)\s*' + escaped + r'[.\s]+[A-Z]', search_area)
        
    if m:
        m2 = re.search(r'\n\s*\d+(?:\.\d+)*\.\s+[A-Z]', search_area[m.end():])
        if m2:
            extracted = search_area[m.start():m.end()+m2.start()].strip()
        else:
            extracted = search_area[m.start():m.start()+2000].strip()
            
        if len(extracted) > 50:
            chunks[idx]['text'] = clean_text(extracted)
            print(f"Fixed Ch {ch} - Index {idx} (new length: {len(extracted)})")
        else:
            print(f"Warning: Extracted text still short for Ch {ch} - Index {idx}: {extracted}")
    else:
        print(f"Could not find heading {heading_prefix} in PDF for Ch {ch} - Index {idx}")

doc.close()

with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
