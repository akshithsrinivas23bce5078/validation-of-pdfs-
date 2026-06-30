"""
For remaining empty chunks, use the TOC heading NAMES (not just numbers) 
to find split points in adjacent chunks.
Also handle cases where the heading text is simply embedded at the START
of the next chunk with proper heading name.
"""
import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Load TOC for heading names
with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)
toc_keys = list(toc.keys())

def extract_heading_num(heading):
    if not heading: return None
    m = re.match(r'^(\d+(?:\.\d+)?)', heading.strip())
    return m.group(1) if m else None

# Build TOC lookup: for each heading number + chapter context, get the heading name
toc_by_num = {}
for k in toc_keys:
    num = extract_heading_num(k)
    if num:
        if num not in toc_by_num:
            toc_by_num[num] = []
        toc_by_num[num].append(k)

# Find empty chunks
empty_indices = []
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        empty_indices.append(i)

print(f"Processing {len(empty_indices)} empty chunks...")

# For each empty chunk, try to find its content in the PRECEDING chunk
for ei in empty_indices:
    ch = chunks[ei].get('chapter')
    h_num = extract_heading_num(chunks[ei].get('heading', ''))
    if not h_num:
        continue
    
    # Get possible TOC heading names for this number
    toc_names = toc_by_num.get(h_num, [])
    
    # Search the preceding chunk (and the one before that)
    search_range = []
    for offset in [1, 2, 3]:
        idx = ei - offset
        if idx >= 0 and chunks[idx].get('chapter') == ch:
            search_range.append(idx)
    
    found = False
    for ci in search_range:
        text = chunks[ci].get('text', '')
        if not text or len(text) < 20:
            continue
        
        # Try each TOC name
        for toc_name in toc_names:
            # Extract the descriptive part after the number
            name_part = re.sub(r'^\d+\.?\d*\.?\s*', '', toc_name).strip()
            if len(name_part) < 3:
                continue
            
            # Search case-insensitively, allowing OCR noise (extra spaces)
            # Create a flexible pattern
            words = name_part.split()
            if len(words) < 2:
                continue
            
            # Use first 2-3 significant words for matching
            search_words = [w for w in words[:4] if len(w) > 2]
            if not search_words:
                continue
            
            # Build fuzzy regex: each word with flexible spacing
            pattern = r'\s+'.join(re.escape(w) for w in search_words)
            m = re.search(pattern, text, re.IGNORECASE)
            
            if m:
                # Found! Find the start of this heading (look back to start of line)
                pos = m.start()
                # Walk back to find the heading number
                line_start = text.rfind('\n', 0, pos)
                if line_start == -1:
                    line_start = 0
                else:
                    line_start += 1
                
                # Check if the heading number is near the match
                before_match = text[line_start:pos]
                num_check = re.search(r'^\s*' + re.escape(h_num) + r'\.?\s*$', before_match)
                
                # Use line_start as split point if heading num found, else use pos
                split_pos = line_start if num_check else pos
                
                # Verify we're not splitting at the very beginning
                if split_pos < 10:
                    continue
                
                before = text[:split_pos].strip()
                after = text[split_pos:].strip()
                
                if len(after) > 10:
                    chunks[ci]['text'] = before
                    chunks[ei]['text'] = after
                    # Clean up heading
                    heading_line = after.split('\n')[0].strip()[:100]
                    if heading_line:
                        chunks[ei]['heading'] = heading_line
                    print(f"  FOUND Ch {ch} heading {h_num}: '{name_part[:40]}' in chunk {ci}")
                    found = True
                    break
        
        if found:
            break
    
    if not found:
        # Special handling: check if the text is at the START of the next non-empty chunk
        for offset in [1, 2]:
            ni = ei + offset
            if ni < len(chunks) and chunks[ni].get('chapter') == ch:
                next_text = chunks[ni].get('text', '')
                if next_text:
                    # Check if next chunk starts with content for this heading
                    for toc_name in toc_names:
                        name_part = re.sub(r'^\d+\.?\d*\.?\s*', '', toc_name).strip()
                        words = name_part.split()[:3]
                        search_words = [w for w in words if len(w) > 2]
                        if not search_words:
                            continue
                        pattern = r'\s+'.join(re.escape(w) for w in search_words)
                        if re.search(pattern, next_text[:500], re.IGNORECASE):
                            # The next chunk starts with this heading's content
                            # Split the next chunk
                            m2 = re.search(pattern, next_text[:500], re.IGNORECASE)
                            # Find the SECOND occurrence of a heading pattern to split
                            next_h_num = extract_heading_num(chunks[ni].get('heading', ''))
                            if next_h_num:
                                next_escaped = re.escape(next_h_num)
                                split_m = re.search(r'(?:^|\n)\s*' + next_escaped + r'[\.\s]+[A-Z]', next_text[m2.end():])
                                if split_m:
                                    sp = m2.end() + split_m.start()
                                    chunks[ei]['text'] = next_text[:sp].strip()
                                    chunks[ni]['text'] = next_text[sp:].strip()
                                    heading_line = chunks[ei]['text'].split('\n')[0].strip()[:100]
                                    if heading_line:
                                        chunks[ei]['heading'] = heading_line
                                    print(f"  SPLIT from next: Ch {ch} heading {h_num}")
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

remaining = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"\nRemaining empty chunks: {remaining}")
