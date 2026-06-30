import json
import fitz
import re
import os

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Chapter 8_3.pdf'
json_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 8_3.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 8_3.jsonl'

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

with open(json_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

doc = fitz.open(pdf_path)
pdf_text = ''
for i in range(doc.page_count):
    pdf_text += doc[i].get_text('text')

# Normalize texts to just lowercase alphanumeric to check for missing blocks
def normalize(t):
    return re.sub(r'[^a-z0-9]', '', str(t).lower())

pdf_norm = normalize(pdf_text)
jsonl_norm = ''
for c in chunks:
    jsonl_norm += normalize(c.get('heading', '')) + normalize(c.get('text', ''))

final_chunks = []
for c in chunks:
    # 1. Clean chapter
    chapter = str(c.get('chapter', '')).replace('Chapter', '').strip()
    
    # 2. Clean title
    title = str(c.get('title', ''))
    if 'Asset Management' in title:
        title = 'Asset Management'
        
    heading = str(c.get('heading', '')).strip()
    
    # Check exclusions
    combined = (title + ' ' + heading).lower()
    if any(w in combined for w in avoid_words):
        continue
        
    final_chunks.append({
        "DOC_NAME": c.get('DOC_NAME'),
        "doc_id": c.get('doc_id'),
        "chapter": chapter,
        "title": title,
        "heading": heading,
        "text": c.get('text', '').strip(),
        "page.no": c.get('page.no', ''),
        "has_table": c.get('has_table', False),
        "table_html": c.get('table_html', {})
    })

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c) + '\n')

print(f"Processed chunks: {len(final_chunks)}")
print(f"PDF Norm len: {len(pdf_norm)}")
print(f"JSONL Norm len: {len(jsonl_norm)}")
