"""
Final pass: Extract text for the remaining 21 empty chunks by:
1. Splitting large preceding chunks at the heading boundary
2. For Ch 18, 19, 22 - extract from original source text with broader patterns
"""
import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Also load ALL original text for broader search
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

# Build chapter full text from original
orig_ch_text = {}
for c in orig_chunks:
    ch = c.get('chapter', '?')
    if ch not in orig_ch_text:
        orig_ch_text[ch] = []
    orig_ch_text[ch].append(clean_text(c.get('text', '')))

fixed = 0

# Specific manual fixes based on analysis:

# Ch 3 heading 2.3 - between 2.2 and 3
# Look in previous chunk for any "2.3" pattern
for i, c in enumerate(chunks):
    if c.get('chapter') == '3' and extract_heading_num(c.get('heading', '')) == '2.2':
        text = c['text']
        # Find if there's a "2.3" at end
        m = re.search(r'\n\s*2\.3\s', text)
        if not m:
            # Check next chunk's text  
            pass

# Generic approach: for each empty chunk, check if the NEXT populated chunk
# contains text that should be split
for i, c in enumerate(chunks):
    if c.get('text', '').strip():
        continue
    
    ch = c.get('chapter')
    h_num = extract_heading_num(c.get('heading', ''))
    if not h_num:
        continue
    
    # Search in previous chunk
    prev_idx = i - 1
    while prev_idx >= 0 and (chunks[prev_idx].get('chapter') != ch or not chunks[prev_idx].get('text', '').strip()):
        prev_idx -= 1
    
    if prev_idx >= 0 and chunks[prev_idx].get('chapter') == ch:
        prev_text = chunks[prev_idx].get('text', '')
        
        # Look for heading_num at start of a line anywhere in prev_text
        escaped = re.escape(h_num)
        # More flexible: look for the number followed by any text
        # But NOT as a footnote reference (like "para 7.10" or "section 2.3")
        for m in re.finditer(r'(?:^|\n)\s*' + escaped + r'[.\s]', prev_text):
            pos = m.start()
            if pos > 0 and prev_text[pos-1] != '\n':
                pos = prev_text.rfind('\n', 0, pos) + 1
            
            # Verify it's not a false positive by checking context
            pre = prev_text[max(0, pos-30):pos].lower().strip()
            if pre.endswith(('para', 'section', 'refer', 'item', 'clause', 'no.')):
                continue
            
            before = prev_text[:pos].strip()
            after = prev_text[pos:].strip()
            
            if len(before) > 20 and len(after) > 20:
                chunks[prev_idx]['text'] = before
                chunks[i]['text'] = after
                heading_line = after.split('\n')[0].strip()[:100]
                if heading_line:
                    chunks[i]['heading'] = heading_line
                print(f"FIXED Ch {ch} heading {h_num}: split from prev at pos {pos}")
                fixed += 1
                break

# Special handling for Ch 18 (RLDA) - headings 1, 3, 5
# These headings have no content because the chapter content is merged oddly
# Ch 18 heading 1 = "Introduction" (should be "1. INTRODUCTION")
# Look in the original text for Ch 18
ch18_texts = orig_ch_text.get('18', [])
ch18_full = '\n'.join(ch18_texts)

# Search for "1. INTRODUCTION" or similar
for i, c in enumerate(chunks):
    if c.get('chapter') == '18' and extract_heading_num(c.get('heading', '')) == '1':
        if not c.get('text', '').strip():
            # Search original text for "INTRODUCTION" or "1. Brief" or "1. About"
            m = re.search(r'1\.\s+(INTRODUCTION|Introduction|BRIEF|Brief|ABOUT|About)', ch18_full)
            if m:
                # Find next heading (2.)
                m2 = re.search(r'\n\s*2\.\s+', ch18_full[m.start():])
                if m2:
                    text = ch18_full[m.start():m.start()+m2.start()].strip()
                    chunks[i]['text'] = text
                    chunks[i]['heading'] = text.split('\n')[0].strip()[:100]
                    print(f"FIXED Ch 18 heading 1 from original text")
                    fixed += 1
            else:
                # Use the heading text that came before heading 2 in the original
                idx_2 = ch18_full.find('2. Organisation')
                if idx_2 == -1:
                    idx_2 = ch18_full.find('2. ORGANISATION')
                if idx_2 > 50:
                    text = ch18_full[:idx_2].strip()
                    chunks[i]['text'] = text
                    chunks[i]['heading'] = '1. Introduction'
                    print(f"FIXED Ch 18 heading 1 (before heading 2)")
                    fixed += 1

# Ch 18 heading 3 and 5
for i, c in enumerate(chunks):
    if c.get('chapter') == '18' and not c.get('text', '').strip():
        h_num = extract_heading_num(c.get('heading', ''))
        if h_num == '3':
            # heading 3 is between heading 2 and heading 4
            m = re.search(r'(?:^|\n)\s*3\.\s+[A-Z]', ch18_full)
            if m:
                m2 = re.search(r'(?:^|\n)\s*4\.\s+', ch18_full[m.start():])
                if m2:
                    text = ch18_full[m.start():m.start()+m2.start()].strip()
                    chunks[i]['text'] = text
                    chunks[i]['heading'] = text.split('\n')[0].strip()[:100]
                    print(f"FIXED Ch 18 heading 3 from original text")
                    fixed += 1
        elif h_num == '5':
            m = re.search(r'(?:^|\n)\s*5\.\s+[A-Z]', ch18_full)
            if m:
                m2 = re.search(r'(?:^|\n)\s*6\.\s+', ch18_full[m.start():])
                if m2:
                    text = ch18_full[m.start():m.start()+m2.start()].strip()
                    chunks[i]['text'] = text
                    chunks[i]['heading'] = text.split('\n')[0].strip()[:100]
                    print(f"FIXED Ch 18 heading 5 from original text")
                    fixed += 1

# Ch 19 heading 4 and 5
ch19_texts = orig_ch_text.get('19', [])
ch19_full = '\n'.join(ch19_texts)

for i, c in enumerate(chunks):
    if c.get('chapter') == '19' and not c.get('text', '').strip():
        h_num = extract_heading_num(c.get('heading', ''))
        if h_num in ['4', '5']:
            m = re.search(r'(?:^|\n)\s*' + re.escape(h_num) + r'\.\s+[A-Z]', ch19_full)
            if m:
                next_num = str(int(h_num) + 1) if '.' not in h_num else None
                if next_num:
                    m2 = re.search(r'(?:^|\n)\s*' + re.escape(next_num) + r'\.\s+', ch19_full[m.start():])
                    if m2:
                        text = ch19_full[m.start():m.start()+m2.start()].strip()
                    else:
                        text = ch19_full[m.start():].strip()
                else:
                    text = ch19_full[m.start():].strip()
                chunks[i]['text'] = text
                chunks[i]['heading'] = text.split('\n')[0].strip()[:100]
                print(f"FIXED Ch 19 heading {h_num} from original text")
                fixed += 1

# Ch 22 heading 6, 7, 8
ch22_texts = orig_ch_text.get('22', [])
ch22_full = '\n'.join(ch22_texts)

for i, c in enumerate(chunks):
    if c.get('chapter') == '22' and not c.get('text', '').strip():
        h_num = extract_heading_num(c.get('heading', ''))
        if h_num in ['6', '7', '8']:
            m = re.search(r'(?:^|\n)\s*' + re.escape(h_num) + r'\.\s+[A-Z]', ch22_full)
            if m:
                next_num = str(int(h_num) + 1)
                m2 = re.search(r'(?:^|\n)\s*' + re.escape(next_num) + r'\.\s+', ch22_full[m.start():])
                if m2:
                    text = ch22_full[m.start():m.start()+m2.start()].strip()
                else:
                    text = ch22_full[m.start():].strip()
                chunks[i]['text'] = text
                chunks[i]['heading'] = text.split('\n')[0].strip()[:100]
                print(f"FIXED Ch 22 heading {h_num} from original text")
                fixed += 1

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

remaining = sum(1 for c in chunks if not c.get('text', '').strip())
print(f"\nFixed {fixed} chunks")
print(f"Remaining empty chunks: {remaining}")
for i, c in enumerate(chunks):
    if not c.get('text', '').strip():
        ch = c.get('chapter')
        h = c.get('heading', '')
        print(f"  [{i}] Ch {ch}: {h}")
