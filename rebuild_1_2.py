import json
import os
from unidecode import unidecode

json_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 1_2.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 1_2.jsonl'

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart']

with open(json_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Pick the first doc_id to unify them
unique_doc_id = chunks[0].get('doc_id', 'CH1-6F9FBAC002')

def clean_dict(d):
    new_d = {}
    for k, v in d.items():
        if isinstance(v, str):
            new_d[k] = unidecode(v)
        elif isinstance(v, dict):
            new_d[k] = clean_dict(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str):
                    new_list.append(unidecode(item))
                elif isinstance(item, dict):
                    new_list.append(clean_dict(item))
                else:
                    new_list.append(item)
            new_d[k] = new_list
        else:
            new_d[k] = v
    return new_d

final_chunks = []

for c in chunks:
    # 1. Clean chapter
    chapter = "1"
    
    # 2. Clean title
    title = 'INTRODUCTION'
        
    heading = str(c.get('heading', '')).strip()
    
    # 3. Check exclusions
    combined = (title + ' ' + heading).lower()
    if any(w in combined for w in avoid_words):
        continue
        
    text = c.get('text', '').strip()
    
    # 4. Fix the specific extraction bug in chunk 22 (1.5.1 Public Relations)
    if heading == "1.5.1 Public Relations and Public Opinion related to Sewerage Works":
        text = text.replace("Reference to light.", "Reference to Figure 1.1 is important. Only when the public are met directly, the system drawbacks will come to light.")
        
    chunk_data = {
        "DOC_NAME": "Chapter 1_2",
        "doc_id": unique_doc_id,
        "chapter": chapter,
        "title": title,
        "heading": heading,
        "text": text,
        "page.no": c.get('page.no', ''),
        "has_table": c.get('has_table', False),
        "table_html": c.get('table_html', {})
    }
    
    final_chunks.append(clean_dict(chunk_data))

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + '\n')

print(f"Processed chunks: {len(final_chunks)}")
print(f"Unique doc_id used: {unique_doc_id}")
