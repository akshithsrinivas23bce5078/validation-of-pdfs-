import json
import re

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

# Build a list of canonical headings
toc_headings = list(toc.values())

unval_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\RAM_2022_Sixth_Edition.jsonl'
unval_titles = []
with open(unval_path, 'r', encoding='utf-8') as f:
    for line in f:
        c = json.loads(line)
        title = c.get('title', '')
        ch_match = re.search(r'Chapter (\d+)', c.get('chapter', ''))
        ch = ch_match.group(1) if ch_match else ''
        unval_titles.append((ch, title))

def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

found = set()

for ch, title in unval_titles:
    n_title = norm(title)
    
    # Try to find a match in TOC
    for toc_k in toc_headings:
        n_toc = norm(toc_k)
        if n_title and n_title in n_toc:
            found.add(toc_k)
            break

print(f"Total TOC entries: {len(toc_headings)}")
print(f"Found via title matching: {len(found)}")
