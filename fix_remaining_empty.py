"""
Handle the remaining 21 empty chunks. For each one, look at the text content of
the preceding AND following chunks to extract the right portion of text.
Many of these are cases where the heading text was eaten by an adjacent chunk.
"""
import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Also load the original unmodified file for raw text
ORIG_FILE = r'chunks after validation\RAM_2022_Sixth_Edition.jsonl'
with open(ORIG_FILE, 'r', encoding='utf-8') as f:
    orig_chunks = [json.loads(line) for line in f]

def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

def extract_heading_num(heading):
    if not heading: return None
    m = re.match(r'^(\d+(?:\.\d+)?)', heading.strip())
    return m.group(1) if m else None

# Build original full text per chapter
orig_full = {}
for c in orig_chunks:
    ch = c.get('chapter', '?')
    if ch not in orig_full:
        orig_full[ch] = ''
    orig_full[ch] += clean_text(c.get('text', '')) + '\n'

# For remaining empty chunks, look in the original full chapter text
# and manually try to extract
empty_indices = []
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        empty_indices.append(i)

print(f"Processing remaining {len(empty_indices)} empty chunks...")

# Specific fixes for known missing headings based on the PDF structure
# These are headings where the content exists in the original PDF but
# uses different numbering or formatting

# Group remaining empties by chapter
empty_by_ch = {}
for i in empty_indices:
    ch = chunks[i].get('chapter')
    h_num = extract_heading_num(chunks[i].get('heading', ''))
    if ch not in empty_by_ch:
        empty_by_ch[ch] = []
    empty_by_ch[ch].append((i, h_num))

for ch, empties in sorted(empty_by_ch.items(), key=lambda x: int(x[0])):
    full_text = orig_full.get(ch, '')
    print(f"\n=== Chapter {ch} (original text: {len(full_text)} chars) ===")
    
    for idx, h_num in empties:
        # Look in the chunk BEFORE this one
        prev_idx = idx - 1
        while prev_idx >= 0 and chunks[prev_idx].get('chapter') != ch:
            prev_idx -= 1
        
        # Look in the chunk AFTER this one
        next_idx = idx + 1
        while next_idx < len(chunks) and chunks[next_idx].get('chapter') != ch:
            next_idx += 1
        
        prev_text = chunks[prev_idx].get('text', '') if prev_idx >= 0 else ''
        next_text = chunks[next_idx].get('text', '') if next_idx < len(chunks) else ''
        
        prev_h = chunks[prev_idx].get('heading', '') if prev_idx >= 0 else ''
        next_h = chunks[next_idx].get('heading', '') if next_idx < len(chunks) else ''
        
        print(f"  Empty {h_num}: between [{prev_h}]({len(prev_text)} chars) and [{next_h}]({len(next_text)} chars)")
        
        # For many of these, the content is embedded at the END of the previous chunk
        # or at the START of the next chunk with a different heading marker
        
        # Strategy: If previous chunk text is very long and next chunk is also populated,
        # try to find a natural split point in the previous chunk
        
        if len(prev_text) > 500 and h_num:
            # Search for the heading number pattern in prev_text
            escaped = re.escape(h_num)
            # Try: "At Railway Board Level", "At Zonal Level", etc.
            # These are common sub-heading patterns
            sub_patterns = [
                r'At\s+Railway\s+Board\s+Level',
                r'At\s+Zonal\s+Level',
                r'At\s+Division',
                r'At\s+Field\s+Level',
                r'At\s+Ministry',
                r'At\s+Station',
            ]
            
            # Also search for the exact heading number anywhere in prev text
            for pat_str in [escaped + r'\.\s+', escaped + r'\s+']:
                for m in re.finditer(pat_str, prev_text):
                    # Check if this is at a line boundary
                    pos = m.start()
                    if pos == 0 or prev_text[pos-1] == '\n':
                        before = prev_text[:pos].strip()
                        after = prev_text[pos:].strip()
                        if len(before) > 50 and len(after) > 50:
                            chunks[prev_idx]['text'] = before
                            chunks[idx]['text'] = after
                            heading_line = after.split('\n')[0].strip()[:100]
                            chunks[idx]['heading'] = heading_line
                            print(f"    FIXED: Split from prev chunk at pos {pos}")
                            break
                else:
                    continue
                break

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

remaining = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"\nRemaining empty chunks: {remaining}")
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        print(f"  [{i}] Ch {c.get('chapter')}: {c.get('heading')}")
