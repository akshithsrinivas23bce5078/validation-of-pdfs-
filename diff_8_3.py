import json
import fitz
import difflib
import re

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Chapter 8_3.pdf'
json_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 8_3.jsonl'

# Extract PDF text
doc = fitz.open(pdf_path)
pdf_text = ""
for i in range(doc.page_count):
    pdf_text += doc[i].get_text('text')

# Extract JSONL text
with open(json_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

jsonl_text = ""
for c in chunks:
    jsonl_text += c.get('heading', '') + " " + c.get('text', '') + " "

# Clean up whitespaces for comparison
def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

pdf_words = normalize_text(pdf_text).split()
jsonl_words = normalize_text(jsonl_text).split()

# Find sequences present in PDF but missing in JSONL
matcher = difflib.SequenceMatcher(None, pdf_words, jsonl_words)

missing_sequences = []
for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == 'delete': # Present in PDF, missing in JSONL
        missing_seq = " ".join(pdf_words[i1:i2])
        # Filter out tiny differences (less than 3 words) which might just be formatting
        if len(missing_seq.split()) > 2:
            missing_sequences.append(missing_seq)

print(f"Total words in PDF: {len(pdf_words)}")
print(f"Total words in JSONL: {len(jsonl_words)}")

if missing_sequences:
    print("\n--- CONTENT PRESENT IN PDF BUT MISSING IN JSONL ---")
    for seq in missing_sequences:
        print(f"- {seq}")
else:
    print("\nNO significant missing content found! JSONL perfectly captures the PDF text.")
