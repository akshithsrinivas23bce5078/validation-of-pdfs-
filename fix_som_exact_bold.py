import json
import fitz
import re
import copy

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual_fixed.jsonl'

# 1. Extract bold sequences from PDF
doc = fitz.open(pdf_path)
bold_sequences = []

for p in range(len(doc)):
    page = doc[p]
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' not in b: continue
        for l in b['lines']:
            line_text = ''
            is_bold = False
            for s in l['spans']:
                if 'Bold' in s['font']: is_bold = True
                line_text += s['text']
            
            line_text = line_text.strip()
            # If the bold sequence starts with a number
            if is_bold and re.match(r'^\d+\s*(?:[A-Za-z]\s*)?\.|\d+\(A\)', line_text):
                # Clean up weird chars
                line_text = line_text.replace('\ufffd', '-').replace('\u2014', '-').replace('\u2013', '-')
                bold_sequences.append(line_text)

# Clean up sequences: some are split across lines, but we just use the first line bold sequence for matching
# Since we just want to find where the heading starts.

# Let's filter bold sequences that are actually headings
headings_data = []
for seq in bold_sequences:
    seq_norm = re.sub(r'\s+', ' ', seq).strip()
    
    # The true heading is usually up to the first '.-' or '.-' or just '.'
    m = re.match(r'^(\d+(?:\(A\))?(?:\s+[A-Za-z])?(?:\.\d+)*\.[^\n]{2,150}?(?:\.\s*-|\.-|\.(?=\s+[A-Z]|$)|-))', seq_norm)
    if m:
        true_heading = m.group(1).strip()
    else:
        # Fallback
        true_heading = seq_norm
    
    headings_data.append({
        'full_bold': seq_norm,
        'true_heading': true_heading
    })

# 2. Read JSONL
with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

new_chunks = []

# 3. Process each chunk
for c in chunks:
    text = c.get('text', '')
    text_norm = re.sub(r'\s+', ' ', text).replace('\ufffd', '-').replace('\u2014', '-').replace('\u2013', '-')
    
    # Does this chunk contain any of the full_bold strings?
    # We should search for true_heading instead, because sometimes the text is formatted differently
    
    # Let's find all headings embedded in the text
    matches = []
    for hdata in headings_data:
        th = hdata['true_heading']
        
        # We only care if it's embedded NOT at the start (or if it is at the start and not already the heading)
        # But we must be careful not to match simple numbers that are part of text.
        # Ensure it has some length and text.
        if len(th) < 5: continue
        
        # Escape for regex
        pattern = r'(?:^|\s)(' + re.escape(th) + r')(?=\s|$)'
        for m in re.finditer(pattern, text_norm):
            matches.append({
                'start': m.start(1),
                'end': m.end(1),
                'heading': th
            })

    if not matches:
        # Also check if the current heading of the chunk is wrong and needs to be replaced
        new_chunks.append(c)
        continue

    # Sort matches by start position
    matches.sort(key=lambda x: x['start'])
    
    # Filter overlapping matches (keep the longer one or first one)
    filtered_matches = []
    for m in matches:
        overlap = False
        for fm in filtered_matches:
            if max(0, min(m['end'], fm['end']) - max(m['start'], fm['start'])) > 0:
                overlap = True
                break
        if not overlap:
            # Check if this heading is just the current heading at the beginning
            if m['start'] < 10 and (m['heading'] in c.get('heading', '') or c.get('heading', '') in m['heading']):
                # Just strip it from text
                text_norm = text_norm[m['end']:].strip()
                c['text'] = text_norm
                c['heading'] = m['heading']
                filtered_matches.append(m) # We handled it, but let's not split on it
                continue
            
            filtered_matches.append(m)
    
    # If no valid internal splits
    valid_splits = [m for m in filtered_matches if m['start'] >= 10]
    
    if not valid_splits:
        new_chunks.append(c)
        continue
        
    print(f"Splitting chunk '{c.get('heading', '')}' at {len(valid_splits)} places.")
    
    # Split the chunk
    last_idx = 0
    current_chunk = copy.deepcopy(c)
    
    # Prefix text before first internal heading
    first_start = valid_splits[0]['start']
    prefix_text = text_norm[:first_start].strip()
    if prefix_text:
        current_chunk['text'] = prefix_text
        new_chunks.append(current_chunk)
        
    for i, m in enumerate(valid_splits):
        start_pos = m['end']
        end_pos = valid_splits[i+1]['start'] if i+1 < len(valid_splits) else len(text_norm)
        
        body_text = text_norm[start_pos:end_pos].strip()
        body_text = re.sub(r'^[\s\.\-]+', '', body_text).strip()
        
        new_c = copy.deepcopy(c)
        new_c['heading'] = m['heading']
        new_c['text'] = body_text
        if i > 0 or prefix_text:
            new_c['has_table'] = False
            new_c['table_html'] = "{}"
            
        new_chunks.append(new_c)

# 4. Clean up current headings
for c in new_chunks:
    h = c.get('heading', '')
    h = h.replace('\ufffd', '-').replace('\u2014', '-').replace('\u2013', '-')
    c['heading'] = h
    
    # Sometimes text starts with a repetition of the heading, strip it
    t = c.get('text', '')
    if t.startswith(h):
        t = t[len(h):].strip()
        t = re.sub(r'^[\s\.\-]+', '', t).strip()
        c['text'] = t

with open(output_path, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Done. Original: {len(chunks)}, New: {len(new_chunks)}")
