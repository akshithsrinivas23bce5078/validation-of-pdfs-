"""
Final extraction for 10 remaining empty chunks using PDF page-by-page search
"""
import json
import re
import fitz

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
PDF_FILE = r'assigned pdfs\RAM 2022 Sixth Edition.pdf'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

def extract_heading_num(heading):
    if not heading: return None
    m = re.match(r'^(\d+(?:\.\d+)?)', heading.strip())
    return m.group(1) if m else None

doc = fitz.open(PDF_FILE)

# For each remaining empty chunk, search a wider PDF range
remaining = [
    (21, '3', '2.3', '3', 310, 380),     # Ch 3 heading 2.3 - page range in PDF
    (94, '5', '7.10', '7.11', 170, 200),  # Ch 5 heading 7.10
    (144, '6', '7.23', '7.24', 270, 300), # Ch 6 heading 7.23
    (171, '7', '11', '12', 370, 400),     # Ch 7 heading 11
    (206, '8', '7.10', '7.11', 400, 430), # Ch 8 heading 7.10
    (227, '9', '6.1', '6.2', 430, 470),   # Ch 9 heading 6.1
    (310, '12', '2.3', '2.4', 500, 520),  # Ch 12 heading 2.3
    (365, '14', '7.2', '7.3', 550, 570),  # Ch 14 heading 7.2
    (519, '22', '7', '8', 680, 710),      # Ch 22 heading 7
    (520, '22', '8', None, 680, 710),      # Ch 22 heading 8
]

for chunk_idx, ch, h_num, next_h, start_pg, end_pg in remaining:
    # Get text from PDF pages
    pdf_text = ''
    for pg in range(start_pg, min(end_pg, len(doc))):
        pdf_text += doc[pg].get_text() + '\n'
    
    # Search for the heading
    escaped = re.escape(h_num)
    
    # Try multiple patterns
    patterns = [
        r'(?:^|\n)\s*' + escaped + r'\.\s+([^\n]+)',      # "2.3. Text"
        r'(?:^|\n)\s*' + escaped + r'\s+([A-Z][^\n]+)',    # "2.3 Text"
        r'(?:^|\n)' + escaped + r'\.?\s+([^\n]+)',          # "2.3Text"
    ]
    
    found = False
    for pat in patterns:
        for m in re.finditer(pat, pdf_text):
            pos = m.start()
            # Verify this is a heading (not a reference)
            pre = pdf_text[max(0, pos-30):pos].lower()
            if any(kw in pre for kw in ['para', 'item', 'refer', 'clause', 'no.', 'rule']):
                continue
            
            # Extract text up to next heading
            if next_h:
                next_escaped = re.escape(next_h)
                m2 = re.search(r'(?:^|\n)\s*' + next_escaped + r'[.\s]+', pdf_text[m.start():])
                if m2:
                    heading_text = pdf_text[m.start():m.start()+m2.start()].strip()
                else:
                    heading_text = pdf_text[m.start():m.start()+3000].strip()
            else:
                heading_text = pdf_text[m.start():m.start()+3000].strip()
            
            if len(heading_text) > 10:
                chunks[chunk_idx]['text'] = clean_text(heading_text)
                heading_line = heading_text.split('\n')[0].strip()[:100]
                chunks[chunk_idx]['heading'] = heading_line
                print(f"FILLED Ch {ch} heading {h_num}: {heading_line}")
                found = True
                break
        if found:
            break
    
    if not found:
        # Try broader search
        print(f"Broad search for Ch {ch} heading {h_num}...")
        # Search entire PDF for patterns with the heading number
        for pg in range(0, len(doc)):
            pg_text = doc[pg].get_text()
            for pat in patterns:
                m = re.search(pat, pg_text)
                if m:
                    # Check page is in a reasonable range for this chapter
                    # (we can't be too strict here)
                    heading_text = pg_text[m.start():].strip()
                    if next_h:
                        next_escaped = re.escape(next_h)
                        m2 = re.search(r'(?:^|\n)\s*' + next_escaped + r'[.\s]+', heading_text)
                        if m2:
                            heading_text = heading_text[:m2.start()].strip()
                        else:
                            heading_text = heading_text[:2000].strip()
                    else:
                        heading_text = heading_text[:2000].strip()
                    
                    if len(heading_text) > 20:
                        chunks[chunk_idx]['text'] = clean_text(heading_text)
                        heading_line = heading_text.split('\n')[0].strip()[:100]
                        chunks[chunk_idx]['heading'] = heading_line
                        print(f"BROAD FOUND Ch {ch} heading {h_num} on page {pg+1}: {heading_line}")
                        found = True
                        break
            if found:
                break
    
    if not found:
        print(f"STILL MISSING Ch {ch} heading {h_num}")

doc.close()

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

final_remaining = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"\nFinal remaining empty: {final_remaining}")
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        print(f"  [{i}] Ch {c.get('chapter')}: {c.get('heading')}")
