import json
import re
import os
from unidecode import unidecode

json_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\Chapter 10_0.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 10_0.jsonl'

avoid_words = ['foreword', 'preface', 'annexure', 'appendix', 'diagram', 'flowchart', 'figure']

headers = {
    "10.1": "10.1 INTRODUCTION",
    "10.2": "10.2 ON-SITE FACILITY MAINTENANCE SYSTEMS",
    "10.3": "10.3 MAINTAINING ON-SITE FACILITIES",
    "10.4": "10.4 LATRINE / TOILET",
    "10.5": "10.5 ON-SITE METHODS",
    "10.6": "10.6 SEPTAGE TREATMENT UNIT",
    "10.7": "10.7 SUMMARY"
}

with open(json_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

unique_doc_id = chunks[0].get('doc_id', 'ONS-AACF36242D')

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

# Pre-computation for Tables and Page ranges
prefix_tables = {}
prefix_pages = {}

for c in chunks:
    heading = str(c.get('heading', '')).strip()
    m = re.match(r'^(10\.\d+)', heading)
    if m:
        prefix = m.group(1)
        
        # Track tables
        if c.get('has_table'):
            if prefix not in prefix_tables:
                prefix_tables[prefix] = []
            prefix_tables[prefix].append(c.get('table_html', ''))
            
        # Track pages
        page_str = c.get('page.no', '')
        nums = re.findall(r'\d+', page_str)
        if nums:
            if prefix not in prefix_pages:
                prefix_pages[prefix] = []
            prefix_pages[prefix].extend([int(n) for n in nums])

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
    
    # Extract 10.x prefix
    m = re.match(r'^(10\.\d+)', heading)
    if not m:
        # Check if heading starts with Table (e.g. "Table 10.1 Key pathogens...")
        if heading.startswith('Table'):
            # find which prefix we're under
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
        
        # If the original heading was exactly the top-level (e.g. 10.1 INTRODUCTION)
        if re.match(r'^10\.\d+\.\d+', heading):
            current_parent_chunk['text'] = f"{heading}\n{text}"
        else:
            current_parent_chunk['text'] = text
            
        # Clean fields
        current_parent_chunk['chapter'] = "10"
        current_parent_chunk['title'] = "ON-SITE SYSTEMS"
        current_parent_chunk['doc_id'] = unique_doc_id
        
        # Restore Table tags
        if prefix in prefix_tables:
            current_parent_chunk['has_table'] = True
            current_parent_chunk['table_html'] = "\n".join(prefix_tables[prefix])
        else:
            current_parent_chunk['has_table'] = False
            current_parent_chunk['table_html'] = {}
            
        # Restore Page range
        if prefix in prefix_pages:
            pages = prefix_pages[prefix]
            min_p = min(pages)
            max_p = max(pages)
            current_parent_chunk['page.no'] = f"({min_p}-{max_p})"
            
    else:
        # Append to existing parent
        if re.match(r'^10\.\d+\.\d+', heading):
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
