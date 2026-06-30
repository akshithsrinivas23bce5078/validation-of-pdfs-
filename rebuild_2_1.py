import json
import re
import os
from unidecode import unidecode

json_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 2_1.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 2_1.jsonl'

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart', 'figure']

headers = {
    "2.1": "2.1 INTRODUCTION",
    "2.2": "2.2 INSPECTION AND EXAMINATION OF SEWER",
    "2.3": "2.3 SEWER CLEANING",
    "2.4": "2.4 SEWER REHABILITATION",
    "2.5": "2.5 PROTECTION OF SEWER SYSTEMS",
    "2.6": "2.6 PROTECTION AGAINST INFILTRATION & EXFILTRATION",
    "2.7": "2.7 MANHOLES AND APPURTENANCES",
    "2.8": "2.8 CROSS DRAINAGE WORKS",
    "2.9": "2.9 PRESSURE / VACUUM SEWER",
    "2.10": "2.10 HOUSE SERVICE CONNECTION",
    "2.11": "2.11 SAFETY PRACTICES",
    "2.12": "2.12 TROUBLESHOOTING",
    "2.13": "2.13 SUMMARY"
}

with open(json_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

unique_doc_id = chunks[0].get('doc_id', 'CH2-BD84F95AF2')

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
current_parent_chunk = None
current_parent_prefix = None

for c in chunks:
    heading = str(c.get('heading', '')).strip()
    
    # Exclude logic
    combined = heading.lower()
    if any(w in combined for w in avoid_words):
        continue
        
    text = c.get('text', '').strip()
    
    # Extract 2.x prefix
    m = re.match(r'^(2\.\d+)', heading)
    if not m:
        # If it somehow doesn't match 2.x, just append to current parent
        if current_parent_chunk:
            current_parent_chunk['text'] += f"\n\n{heading}\n{text}"
        continue
        
    prefix = m.group(1)
    
    if prefix != current_parent_prefix:
        if current_parent_chunk:
            final_chunks.append(current_parent_chunk)
            
        current_parent_prefix = prefix
        current_parent_chunk = c.copy()
        current_parent_chunk['heading'] = headers.get(prefix, f"{prefix} MISSING HEADER")
        
        # If the original heading was exactly the top-level (e.g. 2.1 INTRODUCTION)
        # We don't need to inject it into the text.
        # If it was a child (e.g. 2.1.1), inject it.
        if re.match(r'^2\.\d+\.\d+', heading):
            current_parent_chunk['text'] = f"{heading}\n{text}"
        else:
            current_parent_chunk['text'] = text
            
        # Clean fields
        current_parent_chunk['chapter'] = "2"
        current_parent_chunk['title'] = "SEWER SYSTEMS"
        current_parent_chunk['doc_id'] = unique_doc_id
        current_parent_chunk['has_table'] = False
        current_parent_chunk['table_html'] = {}
        
    else:
        # Append to existing parent
        if re.match(r'^2\.\d+\.\d+', heading):
            current_parent_chunk['text'] += f"\n\n{heading}\n{text}"
        else:
            current_parent_chunk['text'] += f"\n\n{text}"

# append the last one
if current_parent_chunk:
    final_chunks.append(current_parent_chunk)

# Apply Unidecode to all
final_chunks = [clean_dict(c) for c in final_chunks]

os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + '\n')

print(f"Processed into {len(final_chunks)} flattened chunks.")
print(f"Unique doc_id used: {unique_doc_id}")
