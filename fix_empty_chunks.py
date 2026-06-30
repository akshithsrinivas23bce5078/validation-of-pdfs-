"""
Properly fix RAM_2022_Sixth_Edition_fixed.jsonl by:
1. For each empty chunk, search the PRECEDING chunk's text for the heading text
2. Split the preceding chunk at that boundary
3. For chunks that are too long (grabbed too much), re-split properly
4. For truly unfindable headings, search the PDF text
"""
import json
import re
import copy

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

user_seq = {
    '1': ['1', '1.1', '1.2', '1.3', '1.4'],
    '2': ['1', '2', '3', '3.1', '3.2', '4', '5', '6', '7', '7.1', '7.2', '7.3'],
    '3': ['1', '2', '2.1', '2.2', '2.3', '3', '3.1', '3.2', '3.3', '4', '5', '5.1', '5.2', '5.3', '6', '7', '8', '9', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10'],
    '4': ['1', '2', '3', '3.1', '3.2', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14'],
    '5': ['1', '2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20'],
    '6': ['1', '2', '2.1', '2.2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '7.24', '7.25', '7.26', '7.27', '7.28', '7.29', '7.30', '7.31', '7.32', '7.33', '7.34', '7.35', '7.36', '7.37', '7.38', '7.39'],
    '7': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
    '8': ['1', '2', '2.1', '2.2', '2.3', '2.4', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '8'],
    '9': ['1', '1.1', '1.2', '2', '2.1', '2.2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '7', '7.1', '7.2', '7.3', '8', '8.1', '8.2', '8.3'],
    '10': ['1', '2', '2.1', '2.2', '2.3', '2.4', '2.5', '3', '4', '5', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15'],
    '11': ['1', '2', '2.1', '2.2', '2.3', '2.4', '3', '3.1', '3.2', '3.3', '4', '5', '5.1', '5.2', '5.3', '6', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '8', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '8.10', '8.11', '8.12', '8.13'],
    '12': ['1', '1.1', '2', '2.1', '2.2', '2.3', '2.4', '3', '3.1', '3.2', '3.3', '3.4', '4', '5', '6', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '7.24', '7.25', '8'],
    '13': ['1', '2', '3', '4'],
    '14': ['1', '2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21'],
    '15': ['1', '2', '2.1', '2.2', '2.3', '3', '3.1', '3.2', '3.3', '3.4', '4', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '5', '5.1', '5.2', '6', '7', '7.1', '7.2', '7.3'],
    '16': ['1', '2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '8'],
    '17': ['1', '2', '3', '4', '5', '6', '6.1', '7', '8'],
    '18': ['1', '2', '3', '4', '5', '6', '7', '7.1', '7.2'],
    '19': ['1', '2', '3', '3.1', '3.2', '4', '5', '6'],
    '20': ['1', '2', '3', '4', '5', '5.1', '5.2'],
    '21': ['1', '2', '3', '4', '5', '6', '7', '8', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '8.10', '8.11', '8.12', '8.13', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19', '8.20', '8.21', '8.22', '8.23', '8.24'],
    '22': ['1', '2', '2.1', '2.2', '3', '4', '5', '5.1', '5.2', '6', '7', '8']
}

def extract_heading_num(heading):
    if not heading: return None
    m = re.match(r'^(\d+(?:\.\d+)?)', heading.strip())
    return m.group(1) if m else None

def find_split_point(text, heading_num):
    """Find where heading_num starts in text. Returns (position, heading_line) or (-1, None)"""
    escaped = re.escape(heading_num)
    
    # For sub-headings like 3.2, search more carefully
    if '.' in heading_num:
        patterns = [
            r'(?:^|\n)\s*' + escaped + r'\s+([A-Z][A-Za-z\s&\-/,()]+)',
            r'(?:^|\n)\s*' + escaped + r'\.\s+([A-Z][A-Za-z\s&\-/,()]+)',
        ]
    else:
        patterns = [
            r'(?:^|\n)\s*' + escaped + r'\.\s+([A-Z][A-Z\s&\-/,()]+)',
            r'(?:^|\n)\s*' + escaped + r'\.\s+([A-Z][a-zA-Z\s&\-/,()]+)',
        ]
    
    for pat in patterns:
        for m in re.finditer(pat, text):
            pos = m.start()
            # Skip if it's in the middle of a word or number
            if pos > 0 and text[pos] != '\n' and text[pos-1] not in (' ', '\n', '\t'):
                continue
            # Get the full heading line
            line_end = text.find('\n', m.start() + 1)
            if line_end == -1:
                line_end = len(text)
            heading_line = text[m.start():line_end].strip()
            return pos, heading_line
    
    return -1, None

# Step 1: Fix chunks that grabbed too much text by splitting at next heading boundary
# For each chunk, if next chunk in same chapter is empty, try to split
for i in range(len(chunks) - 1):
    ch = chunks[i].get('chapter')
    next_ch = chunks[i+1].get('chapter')
    if ch != next_ch:
        continue
    
    text = chunks[i].get('text', '')
    next_h_num = extract_heading_num(chunks[i+1].get('heading', ''))
    
    if not next_h_num:
        continue
    
    # If next chunk is empty AND current chunk is very long, try splitting
    if not chunks[i+1].get('text', '').strip() and len(text) > 200:
        pos, heading_line = find_split_point(text, next_h_num)
        if pos != -1 and pos > 0:
            chunks[i]['text'] = text[:pos].strip()
            chunks[i+1]['text'] = text[pos:].strip()
            if heading_line:
                chunks[i+1]['heading'] = heading_line.split('\n')[0].strip()
            print(f"SPLIT: Ch {ch} heading {next_h_num} from idx {i}")
    
    # Also fix overly long chunks that contain the NEXT heading's text
    # Check if current chunk text contains the pattern for the next heading
    if chunks[i+1].get('text', '').strip() and len(text) > 5000:
        pos, heading_line = find_split_point(text, next_h_num)
        if pos != -1 and pos > 100:
            # The current chunk contains text that belongs to the next chunk
            overflow = text[pos:].strip()
            chunks[i]['text'] = text[:pos].strip()
            # Prepend overflow to next chunk
            chunks[i+1]['text'] = overflow + '\n' + chunks[i+1]['text']
            print(f"TRIMMED: Ch {ch} idx {i} -> overflow moved to heading {next_h_num}")

# Step 2: Re-check for still-empty chunks and try harder
still_empty = []
for i, chunk in enumerate(chunks):
    if chunk.get('text', '').strip():
        continue
    
    ch = chunk.get('chapter')
    h_num = extract_heading_num(chunk.get('heading', ''))
    
    # Search in the preceding chunk
    if i > 0 and chunks[i-1].get('chapter') == ch:
        prev_text = chunks[i-1].get('text', '')
        pos, heading_line = find_split_point(prev_text, h_num)
        if pos != -1 and pos > 0:
            chunks[i]['text'] = prev_text[pos:].strip()
            chunks[i-1]['text'] = prev_text[:pos].strip()
            if heading_line:
                chunks[i]['heading'] = heading_line.split('\n')[0].strip()
            print(f"SPLIT from prev: Ch {ch} heading {h_num}")
            continue
    
    # Search in chunk i-2 (two before)
    if i > 1 and chunks[i-2].get('chapter') == ch:
        prev_text = chunks[i-2].get('text', '')
        pos, heading_line = find_split_point(prev_text, h_num)
        if pos != -1 and pos > 0:
            chunks[i]['text'] = prev_text[pos:].strip()
            chunks[i-2]['text'] = prev_text[:pos].strip()
            if heading_line:
                chunks[i]['heading'] = heading_line.split('\n')[0].strip()
            print(f"SPLIT from prev-2: Ch {ch} heading {h_num}")
            continue
    
    still_empty.append((ch, h_num, chunk.get('heading', '')))

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"\nStill empty: {len(still_empty)}")
for ch, h_num, heading in still_empty:
    print(f"  Ch {ch}: {heading} ({h_num})")

# Final verification
print(f"\n=== Final Verification ===")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    final_chunks = [json.loads(line) for line in f]

for ch_num in sorted(user_seq.keys(), key=int):
    expected = user_seq[ch_num]
    actual = [extract_heading_num(c.get('heading', '')) for c in final_chunks if c.get('chapter') == ch_num]
    if expected == actual:
        empty_count = sum(1 for c in final_chunks if c.get('chapter') == ch_num and not c.get('text', '').strip())
        status = f"OK ({len(actual)} chunks" + (f", {empty_count} empty" if empty_count else "") + ")"
        print(f"  Ch {ch_num}: {status}")
    else:
        missing = [h for h in expected if h not in actual]
        extra = [h for h in actual if h and h not in expected]
        print(f"  Ch {ch_num}: WRONG")
        if missing: print(f"    Missing: {missing}")
        if extra: print(f"    Extra: {extra}")
