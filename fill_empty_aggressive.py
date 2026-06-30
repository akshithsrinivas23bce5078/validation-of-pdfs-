"""
Search all existing chunk text (across ALL chunks in the same chapter) for the 
remaining 36 empty headings. Use case-insensitive and fuzzy matching.
"""
import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

def extract_heading_num(heading):
    if not heading: return None
    m = re.match(r'^(\d+(?:\.\d+)?)', heading.strip())
    return m.group(1) if m else None

# For each empty chunk, search ALL chunks in same chapter for the heading pattern
empty_indices = []
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        empty_indices.append(i)

print(f"Searching for {len(empty_indices)} empty headings...")

for ei in empty_indices:
    ch = chunks[ei].get('chapter')
    h_num = extract_heading_num(chunks[ei].get('heading', ''))
    if not h_num:
        continue
    
    escaped = re.escape(h_num)
    
    # Build patterns - try very flexible matching
    patterns = [
        re.compile(r'(?:^|\n)\s*' + escaped + r'[\.\s]+([^\n]{5,})', re.IGNORECASE),
        re.compile(r'(?:^|\n)\s*' + escaped + r'\s+([A-Z][^\n]{3,})', re.IGNORECASE),
        # For things like "11. AUDIT" where there might be extra spaces
        re.compile(r'(?:^|\n)\s*' + escaped + r'\s*\.\s*([A-Z][^\n]+)', re.IGNORECASE),
    ]
    
    found = False
    for ci, c in enumerate(chunks):
        if c.get('chapter') != ch or ci == ei:
            continue
        
        text = c.get('text', '')
        if not text:
            continue
        
        for pat in patterns:
            m = pat.search(text)
            if m:
                pos = m.start()
                # Verify this is actually a heading, not a reference
                # Check context: if preceded by "para" or "section", skip
                pre_context = text[max(0, pos-20):pos].lower()
                if 'para' in pre_context or 'section' in pre_context or 'refer' in pre_context:
                    continue
                
                # Split the text
                before = text[:pos].strip()
                after = text[pos:].strip()
                
                if len(after) > 10:
                    # Get heading line
                    heading_line = after.split('\n')[0].strip()
                    
                    chunks[ci]['text'] = before
                    chunks[ei]['text'] = after
                    chunks[ei]['heading'] = heading_line
                    
                    print(f"  FOUND Ch {ch} heading {h_num} in chunk {ci}: '{heading_line[:60]}...'")
                    found = True
                    break
        if found:
            break
    
    if not found:
        print(f"  STILL MISSING Ch {ch} heading {h_num}")

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

# Count remaining empty
remaining = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"\nRemaining empty chunks: {remaining}")
