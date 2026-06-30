import json
import re

input_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\22__Transaction_Entries_Accounting_Manual_Par_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\22__Transaction_Entries_Accounting_Manual_Par_State_Audit_West_Ben.jsonl'

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

with open(input_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

final_chunks = []
for c in chunks:
    # Fix chapter numeric form
    chapter = str(c.get('chapter', '')).replace('Chapter', '').strip()
    
    title = str(c.get('title', '')).strip()
    heading = str(c.get('heading', '')).strip()
    
    # Check exclusion list
    should_skip = False
    combined_check = (title + ' ' + heading).lower()
    for word in avoid_words:
        if word in combined_check:
            should_skip = True
            break
            
    if should_skip:
        continue
        
    # Build strict dictionary
    new_chunk = {
        "DOC_NAME": c.get("DOC_NAME"),
        "doc_id": c.get("doc_id"),
        "chapter": chapter,
        "title": title,
        "heading": heading,
        "text": c.get("text", "").strip(),
        "page.no": c.get("page.no", ""),
        "has_table": c.get("has_table", False),
        "table_html": c.get("table_html", {})
    }
    
    final_chunks.append(new_chunk)

with open(output_path, 'w', encoding='utf-8') as f:
    for chunk in final_chunks:
        f.write(json.dumps(chunk) + '\n')

print(f"Successfully processed Document 22.")
print(f"Total original chunks: {len(chunks)}")
print(f"Total validated chunks: {len(final_chunks)}")
