import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0

for c in chunks:
    text = c['text']
    
    # Check if the text starts with the heading
    # Usually it starts with Para XX - TITLE. or XX. TITLE:
    # Pattern: optional Para, optional numbers with punctuation, then UPPERCASE string, then punctuation/newline
    
    # To be extremely precise, we can use the actual heading words
    heading = c.get('heading', '')
    title_part = heading.split('-', 1)[-1].strip() if '-' in heading else heading
    words = [w for w in re.findall(r'[A-Za-z0-9]{3,}', title_part.lower()) if w not in ('the', 'and', 'for')]
    
    if not words:
        continue
        
    text_prefix = text[:200].lower()
    
    # find the position of the first word and the last word that exist in the prefix
    found_positions = []
    for w in words:
        pos = text_prefix.find(w)
        if pos != -1:
            found_positions.append((pos, pos + len(w)))
            
    if found_positions:
        # get the span of matched words
        min_pos = min(p[0] for p in found_positions)
        max_pos = max(p[1] for p in found_positions)
        
        # if the span is at the very beginning (min_pos <= 25)
        if min_pos <= 25 and max_pos <= 180:
            # check the characters following max_pos to find the end of the heading
            rem_text = text[max_pos:max_pos+50]
            delim_match = re.search(r'(:|:-|\.|\n)', rem_text)
            if delim_match:
                final_end = max_pos + delim_match.end()
            else:
                final_end = max_pos
                
            c['text'] = text[final_end:].lstrip()
            removed_count += 1
            continue

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Safe heading removal applied to {removed_count} chunks.")
