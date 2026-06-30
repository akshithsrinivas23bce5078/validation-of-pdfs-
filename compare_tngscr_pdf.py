import json
import fitz
import re
import difflib
from unidecode import unidecode

# Load JSONL text
filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\tngscr_rules_1973_160625_validated.jsonl"
jsonl_text = ""
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]
    for c in chunks:
        # We append heading and text since heading is extracted from the pdf text
        jsonl_text += c.get("heading", "") + " " + c.get("text", "") + " "

jsonl_text = unidecode(jsonl_text)
jsonl_text = re.sub(r'\s+', ' ', jsonl_text).strip()

# Load PDF text
pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\tngscr_rules_1973_160625.pdf"
doc = fitz.open(pdf_path)

pdf_text = ""
for p in range(doc.page_count):
    text = doc[p].get_text("text")
    pdf_text += text + " "

pdf_text = unidecode(pdf_text)
pdf_text = re.sub(r'\s+', ' ', pdf_text).strip()

# Compare lengths
print(f"JSONL Text Length: {len(jsonl_text)} characters")
print(f"PDF Text Length:   {len(pdf_text)} characters")

# Find missing blocks
matcher = difflib.SequenceMatcher(None, pdf_text, jsonl_text)
missing_blocks_in_jsonl = []
extra_blocks_in_jsonl = []

for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == 'delete': # Present in PDF, missing in JSONL
        missing_str = pdf_text[i1:i2]
        if len(missing_str.strip()) > 50: # Only care about significant chunks > 50 chars
            missing_blocks_in_jsonl.append(missing_str)
    elif tag == 'insert': # Present in JSONL, not in PDF
        extra_str = jsonl_text[j1:j2]
        if len(extra_str.strip()) > 50:
            extra_blocks_in_jsonl.append(extra_str)

print(f"\nFound {len(missing_blocks_in_jsonl)} missing text blocks in JSONL (>50 chars).")
for idx, block in enumerate(missing_blocks_in_jsonl[:5]): # Print first 5
    print(f"\n--- Missing Block {idx+1} ---")
    print(block[:200] + "..." if len(block) > 200 else block)

print(f"\nFound {len(extra_blocks_in_jsonl)} extra text blocks in JSONL (>50 chars).")
for idx, block in enumerate(extra_blocks_in_jsonl[:5]): # Print first 5
    print(f"\n--- Extra Block {idx+1} ---")
    print(block[:200] + "..." if len(block) > 200 else block)

if len(missing_blocks_in_jsonl) > 5 or len(extra_blocks_in_jsonl) > 5:
    print("... and more blocks not shown.")
