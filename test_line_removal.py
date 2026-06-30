import json
import re

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

def clean_text_of_heading(heading, text):
    parts = heading.split(' ', 1)
    if len(parts) != 2:
        return text
    
    num, title = parts
    
    # Split text into lines
    lines = text.split('\n')
    
    # We only look at the first few lines to strip heading
    while lines:
        first_line = lines[0].strip()
        if not first_line:
            lines.pop(0)
            continue
            
        # If first line is exactly the number, remove it
        if first_line == num:
            lines.pop(0)
            continue
            
        # If first line is exactly the title, remove it
        # Sometimes title in heading might differ slightly in spacing, so we normalize spaces
        if re.sub(r'\s+', ' ', first_line.lower()) == re.sub(r'\s+', ' ', title.lower()):
            lines.pop(0)
            continue
            
        # If the first line is exactly "num title", remove it
        if re.sub(r'\s+', ' ', first_line.lower()) == re.sub(r'\s+', ' ', heading.lower()):
            lines.pop(0)
            continue
            
        # If none of these match, stop stripping
        break
        
    return '\n'.join(lines).strip()

for i, c in enumerate(chunks[485:495]):
    new_text = clean_text_of_heading(c['heading'], c['text'])
    print(f"--- Chunk {485+i} ---")
    print(f"HEADING: {c['heading']}")
    print(f"OLD: {repr(c['text'].split(chr(10))[:3])}")
    print(f"NEW: {repr(new_text.split(chr(10))[:2])}")
