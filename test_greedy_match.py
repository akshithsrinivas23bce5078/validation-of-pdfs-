import json
import re
from difflib import SequenceMatcher

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

toc_headings = list(toc.values())

def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def norm_no_numbers(t):
    t = re.sub(r'^\d+(\.\d+)*\s*', '', t)
    return re.sub(r'[^a-z0-9]', '', t.lower())

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
chunks = []
with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        chunks.append(json.loads(line))

toc_idx = 0
assigned_headings = []
matched_indices = set()

for c in chunks:
    title = c.get('original_title', '')
    if not title:
        title = c.get('heading', '')
    n_title = norm(title)
    
    best_idx = -1
    best_score = 0.0
    
    # We look ahead up to 100 entries
    for i in range(toc_idx, min(len(toc_headings), toc_idx + 100)):
        n_toc = norm(toc_headings[i])
        n_toc_no_nums = norm_no_numbers(toc_headings[i])
        
        if not n_title:
            continue
            
        score1 = SequenceMatcher(None, n_title, n_toc).ratio()
        score2 = SequenceMatcher(None, n_title, n_toc_no_nums).ratio()
        score = max(score1, score2)
        
        # Check if it's a strong substring
        if len(n_title) > 5 and (n_title in n_toc or n_title in n_toc_no_nums or n_toc_no_nums in n_title):
            score = max(score, 0.85)
            
        # Dynamic threshold based on jump distance
        jump = i - toc_idx
        threshold = 0.4
        if jump > 3: threshold = 0.6
        if jump > 10: threshold = 0.8
        if jump > 20: threshold = 0.9
        
        if score > threshold and score > best_score:
            best_score = score
            best_idx = i
            
    if best_idx != -1:
        assigned_headings.append(toc_headings[best_idx])
        matched_indices.add(best_idx)
        toc_idx = best_idx + 1  # Advance TOC pointer to the next expected heading
    else:
        # If no match, it's a continuation of the LAST matched heading
        # (or the first one if we haven't matched any)
        if toc_idx > 0:
            assigned_headings.append(toc_headings[toc_idx - 1])
        else:
            assigned_headings.append(toc_headings[0])

print(f"Chunks processed: {len(chunks)}")
print(f"Unique headings assigned: {len(matched_indices)}")
print(f"Missing headings: {len(toc_headings) - len(matched_indices)}")

# Print the missing ones
missing = [h for i, h in enumerate(toc_headings) if i not in matched_indices]
print("First 10 missing:")
for m in missing[:10]:
    print(" -", m)
