import json
import re

raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

# Build giant text string for each chapter
texts_by_ch = {'1': '', '2': '', '3': '', '4': ''}
for c in raw_chunks:
    p = c.get('start_page', 0)
    ch = ''
    if 16 <= p <= 79: ch = '1'
    elif 80 <= p <= 323: ch = '2'
    elif 324 <= p <= 399: ch = '3'
    elif 400 <= p <= 515: ch = '4'
    if ch:
        # Add heading if it exists so we can search it
        if c.get('heading'):
            texts_by_ch[ch] += "\n" + c['heading'] + "\n"
        texts_by_ch[ch] += c.get('content', '') + " "

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def get_para_num(heading):
    match = re.match(r'Para\s+(\d+)\s*-', heading, re.IGNORECASE)
    return match.group(1) if match else ''

# Segment text
for ch in ['1', '2', '3', '4']:
    giant_text = texts_by_ch[ch]
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    
    indices = []
    # Find start indices for all paragraphs
    for vc in vc_list:
        num = get_para_num(vc['heading'])
        # Try to find something like "23. PILGRIM TAX" or just "23." followed by words from title
        title_words = [w for w in re.split(r'\W+', vc['heading'].split('-')[1]) if len(w) > 3]
        
        best_idx = -1
        # Search for exact numbered heading
        pattern = rf'(?:\n|^)\s*{num}[\.\)\-\s]+(.{{0,50}})'
        for m in re.finditer(pattern, giant_text, re.IGNORECASE):
            text_after = m.group(1).lower()
            if not title_words or any(w.lower() in text_after for w in title_words):
                best_idx = m.start()
                break
                
        # If not found, try without newline
        if best_idx == -1:
            pattern2 = rf'\b{num}[\.\)\-\s]+([A-Z][a-zA-Z\s]{{5,50}})'
            for m in re.finditer(pattern2, giant_text):
                text_after = m.group(1).lower()
                if not title_words or any(w.lower() in text_after for w in title_words):
                    best_idx = m.start()
                    break
                    
        indices.append(best_idx)
    
    # Fix missing indices by interpolation or fallback
    # If an index is -1, it means we couldn't find the exact start.
    # We will just distribute the text evenly or give it to the previous one
    
    # First pass: if index is found, ensure it is strictly increasing
    valid_indices = []
    last_valid = 0
    for idx in indices:
        if idx != -1 and idx >= last_valid:
            valid_indices.append(idx)
            last_valid = idx
        else:
            valid_indices.append(-1)
            
    # Interpolate -1s (just use the previous valid index, meaning this chunk gets empty text, which is bad)
    # Actually, if we missed a heading, the text is just lumped.
    # We can just split it halfway?
    for i in range(len(valid_indices)):
        if valid_indices[i] == -1:
            # Find prev valid
            prev_val = 0
            for j in range(i-1, -1, -1):
                if valid_indices[j] != -1:
                    prev_val = valid_indices[j]
                    break
            valid_indices[i] = prev_val
            
    # Assign text
    for i in range(len(vc_list)):
        start = valid_indices[i]
        end = valid_indices[i+1] if i+1 < len(valid_indices) else len(giant_text)
        if start == end:
            # Empty chunk
            vc_list[i]['text'] = ""
        else:
            text_slice = giant_text[start:end]
            vc_list[i]['text'] = clean_text(text_slice)

# Verify Pilgrim Tax
for c in val_chunks:
    if 'Pilgrim Tax' in c['heading']:
        print(f"\\n--- {c['heading']} ---")
        print(c['text'][:200])

empty = [c['heading'] for c in val_chunks if not c['text'].strip()]
print(f"Empty chunks remaining: {len(empty)}")

# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
