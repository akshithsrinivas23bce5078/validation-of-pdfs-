import json
import fitz
import re

# Load JSONL text
filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
jsonl_text = ""
with open(filepath, "r", encoding="utf-8") as f:
    for line in f:
        c = json.loads(line)
        jsonl_text += c.get('heading', '') + " " + c.get('text', '') + " "

# Normalize jsonl text
def normalize(t):
    return re.sub(r'[\s\W_]+', '', t).lower()

jsonl_norm = normalize(jsonl_text)

# Load PDF text
pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf"
doc = fitz.open(pdf_path)

pdf_text = ""
for p in range(len(doc)):
    text = doc[p].get_text("text")
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    pdf_text += text + "\n\n"

# Find missing paragraphs
# Split PDF into paragraphs separated by double newlines or similar
paras = re.split(r'\n\s*\n', pdf_text)
missing = []

for para in paras:
    if len(para.strip()) < 100: continue
    
    # check if it is part of annexure/foreword/preface
    if any(word in para.lower() for word in ['foreword', 'preface', 'annexure', 'appendix', 'flowchart']):
        continue
        
    p_norm = normalize(para)
    if p_norm not in jsonl_norm:
        missing.append(para)

print(f"Found {len(missing)} potentially missing paragraphs.")
if missing:
    print(missing[0][:500])
