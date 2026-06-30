import fitz
import json
import re

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU MINISTERIAL SERVICE RULES.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_MINISTERIAL_SERVICE_RULES_validated.jsonl'

# 1. Extract text from PDF
doc = fitz.open(pdf_path)
pdf_text = ""
for i in range(len(doc)):
    text = doc[i].get_text()
    # Strip headers/footers/page numbers
    # We can do basic cleanup
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line: continue
        # ignore page numbers
        if re.match(r'^-?\s*\d+\s*-?$', line): continue
        if line == 'TAMIL NADU MINISTERIAL SERVICE RULES': continue
        if line.startswith('CONTENTS'): continue
        clean_lines.append(line)
    pdf_text += " " + " ".join(clean_lines)

# 2. Extract text from JSONL
json_text = ""
chunks = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        chunks.append(c)
        json_text += " " + c['text'].replace('\n', ' ')

def normalize(t):
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'[^\w\s]', '', t)
    return t.lower().strip()

norm_pdf = normalize(pdf_text)
norm_json = normalize(json_text)

print(f"Total pages: {len(doc)}")
print(f"PDF length (normalized chars): {len(norm_pdf)}")
print(f"JSONL length (normalized chars): {len(norm_json)}")

diff_len = len(norm_pdf) - len(norm_json)
print(f"Difference: {diff_len} characters")

if diff_len > 1000:
    print("Significant text is missing. Searching for missing blocks...")
    # Find the largest missing block by splitting PDF into sentences
    sentences = re.split(r'(?<=\.)\s+', pdf_text)
    missing = []
    for s in sentences:
        if len(s) > 50:
            norm_s = normalize(s)
            if norm_s not in norm_json:
                missing.append(s)
    
    print(f"Found {len(missing)} potentially missing sentences/blocks.")
    if len(missing) > 0:
        print("Sample missing:", missing[0][:200])
else:
    print("No significant text missing found.")
