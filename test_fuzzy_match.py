import json
import re
import difflib

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

toc_headings = list(toc.values())

def norm_no_numbers(t):
    t = re.sub(r'^\d+(\.\d+)*\s*', '', t)
    return re.sub(r'[^a-z0-9]', '', t.lower())

def fuzzy_match(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl'
chunks = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        chunks.append(json.loads(line))

toc_idx = 0
assigned_headings = []

for c in chunks:
    title = c.get('title', '')
    text = c.get('text', '')
    
    # We create a searchable string from the title and first 300 chars of text
    search_str = norm_no_numbers(title + " " + text[:300])
    
    best_idx = -1
    best_score = 0.8  # Threshold
    
    # Lookahead in TOC
    for i in range(toc_idx, len(toc_headings)):
        n_toc = norm_no_numbers(toc_headings[i])
        
        # If it's a direct substring
        if n_toc and n_toc in search_str:
            best_idx = i
            best_score = 1.0
            break
            
        # Or try fuzzy match
        score = fuzzy_match(n_toc, search_str[:len(n_toc) + 5])
        if score > best_score:
            best_score = score
            best_idx = i
            
    if best_idx != -1:
        assigned_headings.append(toc_headings[best_idx])
        toc_idx = best_idx
    else:
        # If no match, continuation of the current TOC heading
        if toc_idx < len(toc_headings):
            # We don't advance toc_idx
            assigned_headings.append(toc_headings[toc_idx] if toc_idx < len(toc_headings) else toc_headings[-1])
        else:
            assigned_headings.append(toc_headings[-1])

print(f"Chunks processed: {len(chunks)}")
print(f"Unique headings assigned: {len(set(assigned_headings))}")
print(f"Highest TOC index reached: {toc_idx}")
