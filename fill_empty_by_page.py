import json
import re

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'

with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

# Build a dictionary mapping page number to text
page_texts = {}
for rc in raw_chunks:
    p = rc.get('start_page', 0)
    if p not in page_texts:
        page_texts[p] = ""
    page_texts[p] += " " + rc.get('content', '')

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

fixed_count = 0
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        # Fallback: assign text from its physical page number
        p = c.get('page_number', 0)
        
        # Sometimes the page number is off by 1 in the TOC. Let's include p, p+1, p-1
        text = ""
        for pg in [p, p+1, p+2]:
            if pg in page_texts and page_texts[pg].strip():
                text = page_texts[pg]
                break
                
        if not text:
            # If still nothing, try p-1
            if p-1 in page_texts:
                text = page_texts[p-1]
                
        if text:
            c['text'] = clean_text(text)
            fixed_count += 1

empty_count = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"Fixed {fixed_count} chunks. Empty chunks remaining: {empty_count}")

with open(path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
