"""
Full reconstruction of RAM_2022_Sixth_Edition_fixed.jsonl
to match the user's required heading sequence for all 22 chapters.

Strategy:
1. Load the existing chunks
2. For each chapter, compare existing headings vs user-required headings
3. For missing headings, search inside adjacent chunk texts for the heading text
4. Split chunks where needed, or create placeholder entries
5. Write the final file
"""
import json
import re
import copy

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
OUTPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    all_chunks = [json.loads(line) for line in f]

# Load the new_toc_mapping to get heading names
with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)
toc_keys = list(toc.keys())

# Unicode cleanup
def clean_text(t):
    if not t: return t
    t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"')
    t = t.replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
    t = t.replace('\u00e2\u0080\u0093', '-').replace('\u00e2\u0080\u0099', "'")
    return t

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

# Group chunks by chapter
ch_chunks = {}
for c in all_chunks:
    ch = c.get('chapter', '?')
    if ch not in ch_chunks:
        ch_chunks[ch] = []
    ch_chunks[ch].append(c)

# For each chapter, find the TOC heading name for each user-required heading number
# Build a mapping from the TOC: for each chapter, heading_num -> TOC heading name
# The TOC is a flat list; we need to group by chapter boundaries
# Chapter boundaries are where heading number resets to a lower value

def get_toc_heading_name(ch_num, heading_num):
    """Find the TOC heading name that matches this chapter + heading_num"""
    # The existing chunks already have heading names that correspond to TOC entries
    # So we can just use the existing heading if we have it
    if ch_num in ch_chunks:
        for c in ch_chunks[ch_num]:
            num = extract_heading_num(c.get('heading', ''))
            if num == heading_num:
                return c['heading']
    return None

# For MISSING headings, we need to search inside the text of existing chunks
# to find the heading text and split

def find_heading_in_text(text, heading_num):
    """Search for a heading like '4. ...' or '5. ...' inside text content.
    Returns the position and the full heading line if found."""
    # Try patterns like "4. ROLES AND RESPONSIBILITIES" or "5. IMPORTANT RISK"
    # The heading_num could be "4", "5", "3.2", etc.
    escaped = re.escape(heading_num)
    # Pattern: heading_num followed by period/space and uppercase text
    patterns = [
        r'(?m)^' + escaped + r'\.?\s+[A-Z][A-Z\s]+',  # At start of line, ALL CAPS
        r'(?m)^' + escaped + r'\.\s+[A-Z][a-z]+',       # At start of line, Title Case
        r'\n' + escaped + r'\.?\s+[A-Z][A-Z\s]+',        # After newline, ALL CAPS
        r'\n' + escaped + r'\.\s+[A-Z][a-z]+',            # After newline, Title Case
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.start(), m.group().strip()
    return -1, None

# Now process each chapter
final_chunks = []
changes_log = []

for ch_num in sorted(user_seq.keys(), key=int):
    expected = user_seq[ch_num]
    existing = ch_chunks.get(ch_num, [])
    
    # Map existing chunks by their heading number
    existing_by_num = {}
    for c in existing:
        num = extract_heading_num(c.get('heading', ''))
        if num:
            existing_by_num[num] = c
    
    actual_nums = [extract_heading_num(c.get('heading', '')) for c in existing]
    missing = [h for h in expected if h not in actual_nums]
    extra = [h for h in actual_nums if h and h not in expected]
    
    if not missing and not extra:
        # Perfect match - just add in order
        for h_num in expected:
            if h_num in existing_by_num:
                chunk = copy.deepcopy(existing_by_num[h_num])
                chunk['text'] = clean_text(chunk.get('text', ''))
                chunk['heading'] = clean_text(chunk.get('heading', ''))
                chunk['title'] = clean_text(chunk.get('title', ''))
                final_chunks.append(chunk)
        continue
    
    # Handle missing headings by searching in text of surrounding chunks
    # First, build the ordered list of what we have
    ordered_existing = []
    for h_num in expected:
        if h_num in existing_by_num:
            ordered_existing.append((h_num, existing_by_num[h_num]))
    
    # For each missing heading, find which existing chunk contains it
    for miss_num in missing:
        found = False
        for i, (ex_num, ex_chunk) in enumerate(ordered_existing):
            text = ex_chunk.get('text', '')
            pos, heading_line = find_heading_in_text(text, miss_num)
            if pos != -1:
                # Found! Split the chunk
                before_text = text[:pos].strip()
                after_text = text[pos:].strip()
                
                # Update the existing chunk to have only the before text
                ex_chunk['text'] = before_text
                
                # Create new chunk for the missing heading
                new_chunk = copy.deepcopy(ex_chunk)
                new_chunk['heading'] = heading_line if heading_line else f"{miss_num}."
                new_chunk['text'] = after_text
                
                # Insert into ordered_existing right after current
                ordered_existing.insert(i + 1, (miss_num, new_chunk))
                changes_log.append(f"Ch {ch_num}: Split heading {miss_num} from chunk {ex_num}")
                found = True
                break
        
        if not found:
            # Check if the heading might be at the START of the next existing chunk's text
            # or we need to create an empty placeholder
            # Try looking through ALL existing chunks for this chapter
            for c in existing:
                text = c.get('text', '')
                pos, heading_line = find_heading_in_text(text, miss_num)
                if pos != -1:
                    before_text = text[:pos].strip()
                    after_text = text[pos:].strip()
                    c['text'] = before_text
                    
                    new_chunk = copy.deepcopy(c)
                    new_chunk['heading'] = heading_line if heading_line else f"{miss_num}."
                    new_chunk['text'] = after_text
                    
                    # Find position in ordered_existing
                    insert_pos = len(ordered_existing)
                    for j, (en, _) in enumerate(ordered_existing):
                        if expected.index(en) > expected.index(miss_num) if en in expected else False:
                            insert_pos = j
                            break
                    ordered_existing.insert(insert_pos, (miss_num, new_chunk))
                    changes_log.append(f"Ch {ch_num}: Found heading {miss_num} in non-ordered chunk")
                    found = True
                    break
            
            if not found:
                # Create empty placeholder chunk
                template = existing[0] if existing else {'chapter': ch_num}
                new_chunk = {
                    'DOC_NAME': template.get('DOC_NAME', 'RAM 2022 Sixth Edition'),
                    'doc_id': template.get('doc_id', ''),
                    'chapter': ch_num,
                    'title': template.get('title', ''),
                    'heading': f"{miss_num}.",
                    'text': '',
                    'page.no': 'N/A',
                    'has_table': False,
                    'table_html': {}
                }
                insert_pos = len(ordered_existing)
                for j, (en, _) in enumerate(ordered_existing):
                    if en in expected and expected.index(en) > expected.index(miss_num):
                        insert_pos = j
                        break
                ordered_existing.insert(insert_pos, (miss_num, new_chunk))
                changes_log.append(f"Ch {ch_num}: Created EMPTY placeholder for heading {miss_num}")
    
    # Now add chunks in user-required order, skipping extras
    added = set()
    for h_num in expected:
        for en, chunk in ordered_existing:
            if en == h_num and en not in added:
                chunk = copy.deepcopy(chunk)
                chunk['text'] = clean_text(chunk.get('text', ''))
                chunk['heading'] = clean_text(chunk.get('heading', ''))
                chunk['title'] = clean_text(chunk.get('title', ''))
                final_chunks.append(chunk)
                added.add(en)
                break
    
    # Log extras that were dropped
    for h in extra:
        changes_log.append(f"Ch {ch_num}: DROPPED extra heading {h}")

# Write output
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Written {len(final_chunks)} chunks to {OUTPUT_FILE}")
print(f"\n=== Changes Log ===")
for log in changes_log:
    print(f"  {log}")

# Verify
print(f"\n=== Verification ===")
for ch_num in sorted(user_seq.keys(), key=int):
    expected = user_seq[ch_num]
    actual = [extract_heading_num(c.get('heading', '')) for c in final_chunks if c.get('chapter') == ch_num]
    if expected == actual:
        print(f"  Ch {ch_num}: OK ({len(actual)} chunks)")
    else:
        missing = [h for h in expected if h not in actual]
        extra = [h for h in actual if h and h not in expected]
        print(f"  Ch {ch_num}: STILL WRONG")
        if missing: print(f"    Still missing: {missing}")
        if extra: print(f"    Still extra: {extra}")
