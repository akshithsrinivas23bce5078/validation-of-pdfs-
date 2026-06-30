import json
import re
import fitz
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
PDF_FILE = r'assigned pdfs\RAM 2022 Sixth Edition.pdf'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

doc = fitz.open(PDF_FILE)
total_pages = len(doc)
full_text = ""
for pg in range(30, total_pages):
    full_text += doc[pg].get_text() + '\n'

def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    t = re.sub(r'\s+\d{1,4}\s*$', '', t)
    return t

fixed = 0
not_found = []

for i, c in enumerate(chunks):
    if int(c['chapter']) > 20:
        continue
        
    heading = c['heading']
    clean_heading = re.sub(r'\s+', ' ', heading).strip()
    
    # Specific edge cases for heading matching
    heading_pattern = r'\s+'.join(map(re.escape, clean_heading.split()))
    if clean_heading == "8.1 Carriage": heading_pattern = r'8\.1\s*Carr\s*iage|8\.1\s*Carriage'
    
    m = re.search(r'(?:^|\n)\s*' + heading_pattern + r'\s', full_text, re.IGNORECASE)
    
    if not m:
        prefix_match = re.match(r'^(\d+(?:\.\d+)*\.?)?\s*(.*)', clean_heading)
        if prefix_match and prefix_match.group(1):
            prefix = prefix_match.group(1)
            escaped_prefix = re.escape(prefix)
            m = re.search(r'(?:^|\n)\s*' + escaped_prefix + r'[.\s]+[A-Z]', full_text, re.IGNORECASE)
            if not m:
                m = re.search(r'(?:^|\n)\s*' + escaped_prefix + r'\s', full_text, re.IGNORECASE)
    
    if m:
        m2 = re.search(r'\n\s*\d+(?:\.\d+)*\.?\s+[A-Z]', full_text[m.end():])
        m_chap = re.search(r'\n\s*CHAPTER\s+\d+', full_text[m.end():])
        
        end_idx = 4000
        if m2 and m_chap:
            end_idx = min(m2.start(), m_chap.start())
        elif m2:
            end_idx = m2.start()
        elif m_chap:
            end_idx = m_chap.start()
            
        extracted = full_text[m.end():m.end()+end_idx].strip()
        
        if "....................." in extracted:
            extracted = extracted.split(".....................")[0].strip()
            
        # Update text regardless of length! This clears out corrupted text from empty parent headings.
        c['text'] = clean_text(extracted)
        fixed += 1
    else:
        not_found.append((i, heading))

doc.close()

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)

print(f"Re-extracted text for {fixed} chunks.")
if not_found:
    print(f"Could not fix {len(not_found)} chunks:")
    for i, h in not_found:
        print(f"Index {i} | No match | {h}")
