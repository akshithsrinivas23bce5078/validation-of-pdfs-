import json
import re
import os

input_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
output_dir = r'chunks after validation'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'Local Fund Audit Depart Manual  Vol - II_validated.jsonl')

with open(input_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

validated_chunks = []
doc_id = "LFAD-CABFE45CDA"

def is_table(text):
    # Heuristic for table detection
    lines = text.split('\n')
    for line in lines:
        if line.count('  ') > 3 or '|' in line:
            return True
    return False

for i, c in enumerate(chunks):
    start_page = c.get('start_page', 0)
    
    # Filter out Preface, Foreword, TOC (Pages 1-15)
    if start_page < 16:
        continue
        
    chapter_num = ""
    chapter_title = ""
    
    if 16 <= start_page <= 79:
        chapter_num = "1"
        chapter_title = "PANORAMIC VIEW OF AUDIT DEPARTMENT"
    elif 80 <= start_page <= 323:
        chapter_num = "2"
        chapter_title = "AUDIT ON THE ACCOUNTS OF MUNICIPALITIES"
    elif 324 <= start_page <= 399:
        chapter_num = "3"
        chapter_title = "AUDIT ON THE ACCOUNTS OF TOWN PANCHAYATS"
    elif 400 <= start_page <= 514:
        chapter_num = "4"
        chapter_title = "AUDIT ON THE ACCOUNTS OF PANCHAYAT UNION COUNCIL"
    else:
        # Ignore pages beyond 514
        continue

    heading = str(c.get('heading', '')).strip()
    text = str(c.get('content', '')).strip()

    # Sometimes heading is in text, strip it out if it perfectly matches the start
    if text.startswith(heading) and len(heading) > 0:
        text = text[len(heading):].strip()

    # Another heuristic: sometimes text starts with "1. ", "1.1 " which is the heading
    # In some manuals we only keep the number in the heading, but user said "according to pdf"
    # We will just clean up weird heading artifacts
    if heading.endswith(':'):
        heading = heading[:-1].strip()
    
    has_table = is_table(text)
    
    validated_chunk = {
        "DOC_NAME": "Local Fund Audit Depart Manual Vol - II",
        "doc_id": doc_id,
        "chapter": chapter_num,
        "title": chapter_title,
        "heading": heading,
        "text": text,
        "page_no": f"({start_page})",
        "has_table": has_table,
        "table_html": "{}"
    }
    
    validated_chunks.append(validated_chunk)

with open(output_path, 'w', encoding='utf-8') as f:
    for vc in validated_chunks:
        f.write(json.dumps(vc, ensure_ascii=False) + '\n')

print(f"Processed {len(chunks)} chunks.")
print(f"Validated {len(validated_chunks)} chunks.")
print(f"Filtered out {len(chunks) - len(validated_chunks)} chunks (TOC/Appendices).")
