import json
import re
import os

input_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\21__Forms___Formats_Accounting_Manual_Part_5_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\21__Forms___Formats_Accounting_Manual_Part_5_State_Audit_West_Ben.jsonl'

# 1. Read unvalidated chunks
with open(input_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

# 2. Merge phantom chunks
merged_chunks = []
current_valid_chunk = None

for c in raw_chunks:
    fid = str(c.get('form_id', '')).strip()
    sec = str(c.get('section', '')).strip()
    
    # Phantom chunks are rows that got split into separate chunks
    # In section 4, form IDs that are pure numbers (like '1', '2', '3') but not '4' (which is the chapter itself)
    is_phantom = False
    if sec == '4' and re.match(r'^\d+$', fid) and fid != '4':
        is_phantom = True
        
    if is_phantom and current_valid_chunk is not None:
        # Merge text
        current_valid_chunk['text'] += ' ' + c.get('text', '')
        
        # Merge table html
        parent_html = current_valid_chunk.get('table_html', '')
        child_html = c.get('table_html', '')
        
        if parent_html and child_html:
            # remove </table> from parent and <table border='1'> from child
            parent_html = parent_html.replace('</table>', '')
            child_html = re.sub(r'^<table[^>]*>', '', child_html)
            current_valid_chunk['table_html'] = parent_html + child_html
    else:
        current_valid_chunk = dict(c) # copy
        merged_chunks.append(current_valid_chunk)

# 3. Format keys and filter out avoided words
chapter_titles = {
    '1': 'Introduction',
    '2': 'New Forms and Formats introduced',
    '3': 'Combined list of all formats (Form number wise)',
    '4': 'Form of Formats'
}

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

final_chunks = []
for c in merged_chunks:
    chapter = str(c.get('section', ''))
    
    # Identify heading and title
    if str(c.get('form_id', '')) == chapter:
        heading = f"{chapter}. {c.get('title', '')}"
    else:
        heading = f"{c.get('form_id', '')} {c.get('title', '')}"
        
    title = chapter_titles.get(chapter, c.get('title', ''))
    
    # Check exclusion list
    should_skip = False
    combined_check = (title + ' ' + heading).lower()
    for word in avoid_words:
        if word in combined_check:
            should_skip = True
            break
            
    if should_skip:
        continue
        
    # Standardize dictionary
    new_chunk = {
        "DOC_NAME": c.get("DOC_NAME"),
        "doc_id": c.get("doc_id"),
        "chapter": chapter,
        "title": title,
        "heading": heading.strip(),
        "text": c.get("text", "").strip(),
        "page.no": c.get("page.no", ""),
        "has_table": c.get("has_table", False),
        "table_html": c.get("table_html", {})
    }
    final_chunks.append(new_chunk)

# 4. Write output
with open(output_path, 'w', encoding='utf-8') as f:
    for chunk in final_chunks:
        f.write(json.dumps(chunk) + '\n')

print(f"Successfully processed Document 21.")
print(f"Total original chunks: {len(raw_chunks)}")
print(f"Total merged & validated chunks: {len(final_chunks)}")
