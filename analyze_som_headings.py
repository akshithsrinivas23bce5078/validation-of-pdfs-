import json
import fitz
import re

pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf"
jsonl_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl"

# 1. Extract bold headings from PDF
doc = fitz.open(pdf_path)
pdf_headings = []
for p in range(len(doc)):
    page = doc[p]
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' not in b: continue
        for l in b['lines']:
            line_text = ""
            is_bold = False
            for s in l['spans']:
                if 'Bold' in s['font']:
                    is_bold = True
                line_text += s['text']
            
            line_text = line_text.strip()
            # Most headings start with a number like "1.", "1 A.", "634 A." or similar
            if is_bold and re.match(r'^\d+\s*[A-Za-z]?\.', line_text):
                pdf_headings.append(line_text)

print(f"Found {len(pdf_headings)} headings in PDF.")

# 2. Extract headings from JSONL
with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

jsonl_headings = []
for c in chunks:
    h = c.get('heading', '').strip()
    if h:
        jsonl_headings.append(h)

print(f"Found {len(jsonl_headings)} headings in JSONL.")

# 3. Check for PDF headings not in JSONL headings (missing or embedded)
missing_in_jsonl = []
for ph in pdf_headings:
    # normalize spaces and some dashes
    norm_ph = re.sub(r'\s+', ' ', ph).strip().replace('\u2014', '-').replace('\u2013', '-')
    
    found = False
    for jh in jsonl_headings:
        norm_jh = re.sub(r'\s+', ' ', jh).strip().replace('\u2014', '-').replace('\u2013', '-')
        if norm_ph in norm_jh or norm_jh in norm_ph:
            found = True
            break
    
    if not found:
        missing_in_jsonl.append(ph)

print(f"Found {len(missing_in_jsonl)} PDF headings missing from JSONL headings.")
for idx, mh in enumerate(missing_in_jsonl[:20]):
    print(f"Missing: {mh}")

# Let's also check if these missing headings are embedded in the text
embedded = 0
for mh in missing_in_jsonl:
    norm_mh = re.sub(r'\s+', ' ', mh).strip()
    
    found_in_text = False
    for c in chunks:
        text = c.get('text', '')
        norm_text = re.sub(r'\s+', ' ', text).strip()
        if norm_mh in norm_text:
            found_in_text = True
            break
    
    if found_in_text:
        embedded += 1

print(f"{embedded} of these missing headings are embedded in the text.")

