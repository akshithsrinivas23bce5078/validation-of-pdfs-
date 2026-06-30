"""
Extract text from RAM PDF for chapters 18, 19, 22 to fill remaining empty chunks.
Also fix remaining missing sub-headings (2.3, 7.10, etc.) by finding them in the
actual text even with OCR noise.
"""
import json
import re
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Installing PyMuPDF...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pymupdf', '-q'])
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

# Extract PDF text for relevant page ranges
doc = fitz.open(PDF_FILE)
total_pages = len(doc)
print(f"PDF has {total_pages} pages")

# Get full PDF text
all_text = ''
for page in doc:
    all_text += page.get_text() + '\n'

# Search for chapter markers to find page ranges
# Ch 18 - RLDA is around pages 640-650 based on TOC
# Ch 19 - RSPB around pages 650-660
# Ch 22 - E-Office around pages 680-700

# Let me find specific patterns
for pattern in ['RAILWAY LAND DEVELOPMENT AUTHORITY', 'RAILWAY SPORTS PROMOTION BOARD', 'E-OFFICE', 'e-Office']:
    positions = [m.start() for m in re.finditer(pattern, all_text, re.IGNORECASE)]
    if positions:
        # Find which page this is on
        for pos in positions[:3]:
            # Rough page estimation
            for page_num in range(total_pages):
                page_text = doc[page_num].get_text()
                if pattern.lower() in page_text.lower():
                    print(f"Found '{pattern}' on page {page_num + 1}")
                    break
            break

# Now get specific sections

# Ch 18 (RLDA): Extract text between RLDA section and RSPB section
rlda_start = all_text.lower().find('railway land development authority')
rspb_start = all_text.lower().find('railway sports promotion board')
if rlda_start == -1:
    rlda_start = all_text.lower().find('rail land development')
if rspb_start == -1:
    rspb_start = all_text.lower().find('railway sports')

print(f"\nRLDA starts at {rlda_start}, RSPB at {rspb_start}")

if rlda_start != -1 and rspb_start != -1 and rspb_start > rlda_start:
    ch18_text = all_text[rlda_start:rspb_start].strip()
    print(f"Ch 18 text length: {len(ch18_text)}")
    print(f"Ch 18 first 200 chars: {ch18_text[:200]}")
    
    # Find headings 1, 3, 5 in this text
    for h_num in ['1', '3', '5']:
        m = re.search(r'(?:^|\n)\s*' + re.escape(h_num) + r'\.\s+[A-Z]', ch18_text)
        if m:
            # Find next heading
            next_num = str(int(h_num) + 1)
            m2 = re.search(r'(?:^|\n)\s*' + re.escape(next_num) + r'\.\s+', ch18_text[m.start():])
            if m2:
                heading_text = ch18_text[m.start():m.start()+m2.start()].strip()
            else:
                heading_text = ch18_text[m.start():].strip()
            
            # Find the chunk and fill it
            for i, c in enumerate(chunks):
                if c.get('chapter') == '18' and extract_heading_num(c.get('heading', '')) == h_num and not c.get('text', '').strip():
                    chunks[i]['text'] = clean_text(heading_text)
                    heading_line = heading_text.split('\n')[0].strip()[:100]
                    chunks[i]['heading'] = heading_line
                    print(f"  FILLED Ch 18 heading {h_num}: {heading_line}")
                    break
        else:
            print(f"  NOT FOUND Ch 18 heading {h_num} in PDF text")

# Ch 19 (RSPB): Extract text between RSPB and next chapter
eoffice_start = all_text.lower().find('e-office')
if eoffice_start == -1:
    eoffice_start = all_text.lower().find('audit of companies under')

ch19_text = all_text[rspb_start:eoffice_start].strip() if rspb_start != -1 and eoffice_start > rspb_start else ''
if ch19_text:
    print(f"\nCh 19 text length: {len(ch19_text)}")
    for h_num in ['4', '5']:
        m = re.search(r'(?:^|\n)\s*' + re.escape(h_num) + r'\.\s+[A-Z]', ch19_text)
        if m:
            next_num = str(int(h_num) + 1)
            m2 = re.search(r'(?:^|\n)\s*' + re.escape(next_num) + r'\.\s+', ch19_text[m.start():])
            if m2:
                heading_text = ch19_text[m.start():m.start()+m2.start()].strip()
            else:
                heading_text = ch19_text[m.start():m.start()+5000].strip()
            
            for i, c in enumerate(chunks):
                if c.get('chapter') == '19' and extract_heading_num(c.get('heading', '')) == h_num and not c.get('text', '').strip():
                    chunks[i]['text'] = clean_text(heading_text)
                    heading_line = heading_text.split('\n')[0].strip()[:100]
                    chunks[i]['heading'] = heading_line
                    print(f"  FILLED Ch 19 heading {h_num}: {heading_line}")
                    break
        else:
            print(f"  NOT FOUND Ch 19 heading {h_num}")

# Ch 22 (E-Office): headings 6, 7, 8
# Find e-Office text in PDF
eoffice_text = all_text[eoffice_start:].strip() if eoffice_start != -1 else ''
# Actually need to find the Ch 22 section specifically
# Look for "E-OFFICE" or "eOffice" as chapter heading
ch22_markers = ['CHAPTER 22', 'E-OFFICE', 'e-Office']
for marker in ch22_markers:
    idx = all_text.find(marker)
    if idx != -1:
        print(f"\nFound Ch 22 marker '{marker}' at pos {idx}")
        # Get text from here
        ch22_text = all_text[idx:idx+20000]
        for h_num in ['6', '7', '8']:
            m = re.search(r'(?:^|\n)\s*' + re.escape(h_num) + r'\.\s+[A-Z]', ch22_text)
            if m:
                next_num = str(int(h_num) + 1)
                m2 = re.search(r'(?:^|\n)\s*' + re.escape(next_num) + r'\.\s+', ch22_text[m.start():])
                if m2:
                    heading_text = ch22_text[m.start():m.start()+m2.start()].strip()
                else:
                    # Take up to 3000 chars or end
                    heading_text = ch22_text[m.start():m.start()+3000].strip()
                
                for i, c in enumerate(chunks):
                    if c.get('chapter') == '22' and extract_heading_num(c.get('heading', '')) == h_num and not c.get('text', '').strip():
                        chunks[i]['text'] = clean_text(heading_text)
                        heading_line = heading_text.split('\n')[0].strip()[:100]
                        chunks[i]['heading'] = heading_line
                        print(f"  FILLED Ch 22 heading {h_num}: {heading_line}")
                        break
            else:
                print(f"  NOT FOUND Ch 22 heading {h_num}")
        break

# Now handle the remaining sub-heading misses by looking in the original chunks
# For cases like 7.10, 2.3, 7.23, 7.2, 7.14, 7.9, 4.4
# These are likely embedded in the preceding chunk's text but with OCR noise

# Load original unmodified
with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    orig_chunks = [json.loads(line) for line in f]

orig_ch_full = {}
for c in orig_chunks:
    ch = c.get('chapter', '?')
    if ch not in orig_ch_full:
        orig_ch_full[ch] = ''
    orig_ch_full[ch] += clean_text(c.get('text', '')) + '\n'

# For each remaining empty, try extracting from PDF text by chapter
remaining_empty = [(i, c) for i, c in enumerate(chunks) if not c.get('text', '').strip()]
print(f"\n=== Attempting PDF extraction for {len(remaining_empty)} remaining ===")

for i, c in remaining_empty:
    ch = c.get('chapter')
    h_num = extract_heading_num(c.get('heading', ''))
    if not h_num:
        continue
    
    # Get page number range from surrounding chunks
    prev_page = None
    next_page = None
    for j in range(i-1, max(0, i-5), -1):
        p = chunks[j].get('page.no', '')
        if p and p != 'N/A':
            # Extract page number
            nums = re.findall(r'\d+', str(p))
            if nums:
                prev_page = int(nums[-1])
                break
    for j in range(i+1, min(len(chunks), i+5)):
        p = chunks[j].get('page.no', '')
        if p and p != 'N/A':
            nums = re.findall(r'\d+', str(p))
            if nums:
                next_page = int(nums[0])
                break
    
    if prev_page and next_page:
        # Extract text from those PDF pages
        start_pg = max(0, prev_page - 1)  # 0-indexed
        end_pg = min(total_pages, next_page)
        pdf_text = ''
        for pg in range(start_pg, end_pg):
            pdf_text += doc[pg].get_text() + '\n'
        
        # Search for heading pattern
        escaped = re.escape(h_num)
        m = re.search(r'(?:^|\n)\s*' + escaped + r'[.\s]+[A-Z]', pdf_text)
        if m:
            # Find next heading
            user_seq = {
                '3': ['1', '2', '2.1', '2.2', '2.3', '3'],
                '5': ['7.9', '7.10', '7.11'],
                '6': ['7.22', '7.23', '7.24'],
                '7': ['10', '11', '12'],
                '8': ['7.9', '7.10', '7.11'],
                '9': ['6', '6.1', '6.2'],
                '12': ['2.2', '2.3', '2.4'],
                '14': ['7.1', '7.2', '7.3', '7.13', '7.14', '7.15'],
                '15': ['2.2', '2.3', '3', '4.3', '4.4', '4.5'],
                '16': ['7.8', '7.9', '7.10'],
            }
            seq = user_seq.get(ch, [])
            idx_in_seq = seq.index(h_num) if h_num in seq else -1
            next_h = seq[idx_in_seq + 1] if idx_in_seq != -1 and idx_in_seq + 1 < len(seq) else None
            
            if next_h:
                next_escaped = re.escape(next_h)
                m2 = re.search(r'(?:^|\n)\s*' + next_escaped + r'[.\s]+', pdf_text[m.start():])
                if m2:
                    heading_text = pdf_text[m.start():m.start()+m2.start()].strip()
                else:
                    heading_text = pdf_text[m.start():m.start()+2000].strip()
            else:
                heading_text = pdf_text[m.start():m.start()+2000].strip()
            
            chunks[i]['text'] = clean_text(heading_text)
            heading_line = heading_text.split('\n')[0].strip()[:100]
            chunks[i]['heading'] = heading_line
            print(f"  FILLED from PDF Ch {ch} heading {h_num}: {heading_line}")

doc.close()

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

remaining = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"\nFinal remaining empty chunks: {remaining}")
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        print(f"  [{i}] Ch {c.get('chapter')}: {c.get('heading')}")
