import json
import os

json_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 9_2.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 9_2.jsonl'

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

with open(json_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

final_chunks = []
# Pick the first doc_id to unify them
unique_doc_id = chunks[0].get('doc_id', 'CH9-163DF729FA')

replacements = {
    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
    '\u2013': '-', '\u2014': '-', '\u2022': '*', '\u00a0': ' ', '\u00ad': '-', '\u2026': '...'
}

def clean_text(text):
    if not isinstance(text, str): return text
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

for c in chunks:
    # 1. Clean chapter
    chapter = "9"
    
    # 2. Clean title
    title = 'Management Information System'
        
    heading = str(c.get('heading', '')).strip()
    
    # Check exclusions
    combined = (title + ' ' + heading).lower()
    if any(w in combined for w in avoid_words):
        continue
        
    final_chunks.append({
        "DOC_NAME": "Chapter 9_2",
        "doc_id": unique_doc_id,
        "chapter": chapter,
        "title": title,
        "heading": clean_text(heading),
        "text": clean_text(c.get('text', '').strip()),
        "page.no": c.get('page.no', ''),
        "has_table": c.get('has_table', False),
        "table_html": c.get('table_html', {})
    })

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Processed chunks: {len(final_chunks)}")
print(f"Unique doc_id used: {unique_doc_id}")
