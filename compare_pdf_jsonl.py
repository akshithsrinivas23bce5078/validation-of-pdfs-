import json
import fitz
import re
import difflib
from unidecode import unidecode

# Load JSONL text
filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
jsonl_text = ""
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]
    for c in chunks:
        jsonl_text += c["text"] + " "

jsonl_text = re.sub(r'\s+', ' ', jsonl_text).strip()

# Load PDF text
pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TN_Vision_2023(PHASE 1).pdf"
doc = fitz.open(pdf_path)

pdf_text = ""
for p in range(8, 66): # Pages 9 to 66
    text = doc[p].get_text("text")
    # Clean the exact same headers we stripped
    text = re.sub(r'Strategic Plan for Infrastructure Development in Tamil Nadu :Vision Tamil Nadu 2023\s*\d+', '', text)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^Figure\s*\d+.*$', '', text, flags=re.MULTILINE)
    pdf_text += text + " "

pdf_text = unidecode(pdf_text)
pdf_text = re.sub(r'\s+', ' ', pdf_text).strip()

# Compare lengths
print(f"JSONL Text Length: {len(jsonl_text)} characters")
print(f"PDF Text Length:   {len(pdf_text)} characters")

# Find missing blocks
matcher = difflib.SequenceMatcher(None, pdf_text, jsonl_text)
missing_blocks = []

for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == 'delete': # Present in PDF, missing in JSONL
        missing_str = pdf_text[i1:i2]
        if len(missing_str.strip()) > 50: # Only care about significant chunks > 50 chars
            missing_blocks.append(missing_str)

print(f"\nFound {len(missing_blocks)} missing text blocks (>50 chars).")
for idx, block in enumerate(missing_blocks):
    print(f"\n--- Missing Block {idx+1} ---")
    print(block[:200] + "..." if len(block) > 200 else block)

