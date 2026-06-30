import json
import re
import PyPDF2

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Maintenance manual of WAG-9 vol. III_PDA West Central Rai.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Maintenance manual of WAG-9 vol. III_PDA West Central Rai.jsonl'

# 1. Get headings from JSONL
with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(l) for l in f]

json_headings = set()
for c in chunks:
    json_headings.add(c['heading'])

# 2. Get headings from PDF
pdf_text = ""
try:
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for i in range(len(reader.pages)):
            pdf_text += reader.pages[i].extract_text() + "\n"
except Exception as e:
    print(f"Error reading PDF: {e}")

# Try to find all section headings in format X.Y Title
# Chapters are 6, 7, 8 in this file.
matches = re.findall(r'(?m)^([678]\.\d\s+[A-Za-z &-]+)', pdf_text)
# Clean up matches
pdf_headings = set()
for m in matches:
    # Clean trailing spaces and newlines
    h = m.strip()
    # sometimes OCR splits words or has random chars, let's keep only reasonable length
    if len(h) > 5 and len(h) < 50:
        pdf_headings.add(h)

print("=== Headings found in JSONL ===")
for h in sorted(list(json_headings)):
    print(h)

print("\n=== Headings found in PDF (Regex Approximation) ===")
for h in sorted(list(pdf_headings)):
    print(h)

missing_in_json = pdf_headings - json_headings
print("\n=== Missing in JSONL ===")
for h in sorted(list(missing_in_json)):
    print(h)
