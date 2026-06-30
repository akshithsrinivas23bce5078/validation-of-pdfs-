import json
import re

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

toc_values = list(toc.values())

def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def norm_no_numbers(t):
    # remove leading numbers like 7.39
    t = re.sub(r'^\d+(\.\d+)*\s*', '', t)
    return re.sub(r'[^a-z0-9]', '', t.lower())

unval_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\RAM_2022_Sixth_Edition.jsonl'
unval_titles = []
with open(unval_path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        unval_titles.append(c.get('title', ''))

toc_idx = 0
matches = 0
for title in unval_titles:
    n_title = norm_no_numbers(title)
    if not n_title:
        continue
    
    # Search forward in TOC for a match
    found_idx = -1
    # Look ahead up to 50 entries
    for i in range(toc_idx, min(len(toc_values), toc_idx + 50)):
        n_toc = norm_no_numbers(toc_values[i])
        if n_title in n_toc or n_toc in n_title:
            found_idx = i
            break
            
    if found_idx != -1:
        #print(f"Matched {title} -> {toc_values[found_idx]}")
        matches += 1
        toc_idx = found_idx + 1

print(f"Matched {matches} out of {len(toc_values)} TOC entries sequentially!")
