import json
import re

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

expected_keys = {
    "DOC_NAME", "doc_id", "chapter", "title", "heading", "text", 
    "page.no", "has_table", "table_html", "para"
}

with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

total = len(chunks)
empty_texts = 0
invalid_keys = []
invalid_doc_name = 0
invalid_page_no = 0

for i, c in enumerate(chunks):
    keys = set(c.keys())
    if keys != expected_keys:
        invalid_keys.append(i+1)
        
    if not c.get('text', '').strip():
        empty_texts += 1
        
    if c.get('DOC_NAME') != "Local Fund Audit Depart Manual Vol - II":
        invalid_doc_name += 1
        
    page_no = c.get('page.no', '')
    if not re.match(r'^\(\d+-\d+\)$', page_no):
        invalid_page_no += 1

print("=== FINAL VALIDATION REPORT ===")
print(f"Total Chunks: {total} (Expected: 337)")
print(f"Zero-length texts: {empty_texts} (Expected: 0)")
print(f"Invalid Keys found in chunks: {len(invalid_keys)} (Expected: 0)")
print(f"Invalid DOC_NAME format: {invalid_doc_name} (Expected: 0)")
print(f"Invalid page.no format: {invalid_page_no} (Expected: 0)")
