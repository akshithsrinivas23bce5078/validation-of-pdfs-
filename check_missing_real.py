import fitz
import json
import re

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU MINISTERIAL SERVICE RULES.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_MINISTERIAL_SERVICE_RULES_validated.jsonl'

# Extract text from JSONL
json_text = ""
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        json_text += " " + c['text'].replace('\n', ' ')

def normalize(t):
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'[^\w\s]', '', t)
    return t.lower().strip()

norm_json = normalize(json_text)

# Extract text from PDF, skipping TOC (pages 0-2) and Annexures
doc = fitz.open(pdf_path)
real_missing = []

# Find where Annexure I starts to stop parsing
annexure_started = False

for i in range(3, len(doc)):
    page_text = doc[i].get_text()
    
    # Check for Annexure I header to stop completely
    if 'ANNEXURE  I' in page_text or 'ANNEXURE - I' in page_text:
        annexure_started = True
        break
        
    lines = page_text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if re.match(r'^-?\s*\d+\s*-?$', line): continue
        if line == 'TAMIL NADU MINISTERIAL SERVICE RULES': continue
        clean_lines.append(line)
    
    page_clean_text = " ".join(clean_lines)
    
    # Split into sentences to check missing
    sentences = re.split(r'(?<=[.!?])\s+', page_clean_text)
    for s in sentences:
        if len(s) > 80:
            norm_s = normalize(s)
            if norm_s not in norm_json:
                real_missing.append(s)

print(f"Found {len(real_missing)} potentially missing sentences in the main body.")
if len(real_missing) > 0:
    for i, m in enumerate(real_missing[:10]):
        print(f"Missing {i+1}: {m}")
