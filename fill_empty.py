"""
Fix empty placeholder chunks by searching through existing text content to find
the missing heading text embedded within neighboring chunks.
"""
import json
import re
import copy

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Also load the ORIGINAL file before reconstruction to search unmodified text
ORIG_FILE = r'chunks after validation\RAM_2022_Sixth_Edition.jsonl'
with open(ORIG_FILE, 'r', encoding='utf-8') as f:
    orig_chunks = [json.loads(line) for line in f]

def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    return t

# Build full text per chapter from ORIGINAL chunks
ch_full_text = {}
for c in orig_chunks:
    ch = c.get('chapter', '?')
    if ch not in ch_full_text:
        ch_full_text[ch] = ''
    t = clean_text(c.get('text', ''))
    ch_full_text[ch] += t + '\n'

def find_heading_in_full_text(full_text, heading_num, next_heading_num=None):
    """Search for heading_num in full text and extract text up to next_heading_num"""
    escaped = re.escape(heading_num)
    
    # Try multiple patterns
    patterns = [
        # "4. ROLES AND RESPONSIBILITIES..." (all caps after number)
        r'(' + escaped + r'\.?\s+[A-Z][A-Z\s&\-/,()]+)',
        # "4. Roles And Responsibilities..." (title case)
        r'(' + escaped + r'\.?\s+[A-Z][a-zA-Z\s&\-/,()]+)',
    ]
    
    best_match = None
    best_pos = -1
    
    for pat in patterns:
        for m in re.finditer(pat, full_text):
            # Verify this is truly a heading match (not a reference like "para 4")
            # Check that the heading_num is at a line boundary or after a newline
            start = m.start()
            if start == 0 or full_text[start-1] == '\n' or full_text[start-1] == ' ':
                if best_pos == -1 or start < best_pos:
                    best_pos = start
                    best_match = m
                    break
    
    if best_match is None:
        return None, None
    
    start_pos = best_match.start()
    heading_line = best_match.group(1).strip()
    
    # Find the end: either next_heading_num or a reasonable amount of text
    end_pos = len(full_text)
    if next_heading_num:
        next_escaped = re.escape(next_heading_num)
        next_patterns = [
            r'\n' + next_escaped + r'\.?\s+[A-Z]',
            r'\n' + next_escaped + r'\.\s+[A-Z]',
        ]
        for npat in next_patterns:
            nm = re.search(npat, full_text[start_pos:])
            if nm:
                end_pos = start_pos + nm.start()
                break
    
    text_content = full_text[start_pos:end_pos].strip()
    return heading_line, text_content


# User's required heading sequence per chapter
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

# For each empty chunk, try to find text from original full text
fixed_count = 0
still_empty = []

for i, chunk in enumerate(chunks):
    if chunk.get('text', '').strip():
        continue
    
    ch = chunk.get('chapter')
    h_num = extract_heading_num(chunk.get('heading', ''))
    if not h_num or ch not in ch_full_text:
        still_empty.append((ch, chunk.get('heading', '')))
        continue
    
    # Determine the next heading number
    expected = user_seq.get(ch, [])
    if h_num in expected:
        idx = expected.index(h_num)
        next_h = expected[idx + 1] if idx + 1 < len(expected) else None
    else:
        next_h = None
    
    full_text = ch_full_text[ch]
    heading_line, text_content = find_heading_in_full_text(full_text, h_num, next_h)
    
    if text_content and len(text_content) > 10:
        chunks[i]['text'] = text_content
        if heading_line:
            chunks[i]['heading'] = heading_line
        fixed_count += 1
        print(f"FIXED Ch {ch} heading {h_num}: found {len(text_content)} chars")
    else:
        still_empty.append((ch, chunk.get('heading', ''), h_num))
        print(f"STILL EMPTY Ch {ch} heading {h_num}")

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"\nFixed {fixed_count} empty chunks")
print(f"Still empty: {len(still_empty)}")
for item in still_empty:
    print(f"  {item}")
