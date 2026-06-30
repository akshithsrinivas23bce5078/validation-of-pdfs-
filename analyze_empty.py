import json
import re

path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

empty_indices = [i for i, c in enumerate(chunks) if not c['text'].strip()]
print(f"Total empty chunks: {len(empty_indices)}")

# Let's see if the text for empty chunk `i` is in chunk `i+1` or `i-1`
def clean_heading(h):
    return re.sub(r'^Para\s*\d+\s*-\s*', '', h, flags=re.IGNORECASE).strip()

found_in_next = 0
found_in_prev = 0

for i in empty_indices:
    c = chunks[i]
    heading = clean_heading(c['heading'])
    
    # Try to find words of the heading in the next chunk
    words = heading.split()
    
    in_next = False
    in_prev = False
    
    if i < len(chunks) - 1:
        next_text = chunks[i+1]['text']
        if any(w in next_text for w in words if len(w) > 3):
            in_next = True
            
    if i > 0:
        prev_text = chunks[i-1]['text']
        if any(w in prev_text for w in words if len(w) > 3):
            in_prev = True
            
    if in_next: found_in_next += 1
    if in_prev: found_in_prev += 1

print(f"Empty chunks whose heading words appear in the next chunk: {found_in_next}")
print(f"Empty chunks whose heading words appear in the previous chunk: {found_in_prev}")
