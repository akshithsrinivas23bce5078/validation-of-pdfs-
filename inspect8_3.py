import json
import fitz

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 8_3.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Chapter 8_3.pdf'
doc = fitz.open(pdf_path)

print(f'Total pages in PDF: {doc.page_count}')
for i in range(min(5, doc.page_count)):
    print(f"--- PAGE {i} ---")
    text = doc[i].get_text('text')
    print(repr(text[:1000]))
