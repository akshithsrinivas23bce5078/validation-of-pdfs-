import json
import fitz
import re
import difflib
from bs4 import BeautifulSoup
import sys

# Windows console fix for unicode
sys.stdout.reconfigure(encoding='utf-8')

def extract_text_from_html(html):
    if not html or html == "{}": return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ")

# Load JSONL text
filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_SECRETARIAT_SERVICE_RULES_validated.jsonl"
jsonl_text = ""
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]
    for c in chunks:
        heading = c.get('heading', '')
        text = c.get('text', '')
        table_text = extract_text_from_html(c.get('table_html', ''))
        jsonl_text += heading + " " + text + " " + table_text + " "

jsonl_text = re.sub(r'\s+', ' ', jsonl_text).strip()

# Load PDF text
pdf_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU SECRETARIAT SERVICE RULES.pdf"
doc = fitz.open(pdf_path)

pdf_text = ""
for p in range(len(doc)):
    text = doc[p].get_text("text")
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    pdf_text += text + " "

pdf_text = re.sub(r'\s+', ' ', pdf_text).strip()

print(f"JSONL Text Length: {len(jsonl_text)} characters")
print(f"PDF Text Length:   {len(pdf_text)} characters")

matcher = difflib.SequenceMatcher(None, pdf_text, jsonl_text)
missing_blocks = []

for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == 'delete':
        missing_str = pdf_text[i1:i2]
        if len(missing_str.strip()) > 50:
            missing_blocks.append(missing_str)

print(f"\nFound {len(missing_blocks)} missing text blocks (>50 chars) from JSONL.")
for idx, block in enumerate(missing_blocks):
    print(f"\n--- Missing Block {idx+1} ---")
    print(block[:300] + "..." if len(block) > 300 else block)

