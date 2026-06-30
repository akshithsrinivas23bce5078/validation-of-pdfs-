import json
import fitz
import re

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual_fixed.jsonl'

print("Extracting bold sequences...")
doc = fitz.open(pdf_path)
bold_headings = []

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
            if is_bold and re.match(r'^\d+\s*(?:[A-Za-z]\s*)?\.|\d+\(A\)', line_text):
                line_text = line_text.replace('\ufffd', '-').replace('\u2014', '-').replace('\u2013', '-')
                line_text = re.sub(r'\s+', ' ', line_text).strip()
                bold_headings.append(line_text)

print(f"Extracted {len(bold_headings)} bold headings from PDF.")

headings_data = []
for seq in bold_headings:
    m = re.match(r'^(\d+(?:\(A\))?(?:\s+[A-Za-z])?(?:\.\d+)*\.[^\n]{2,150}?(?:\.\s*-|\.-|\.(?=\s+[A-Z]|$)|-))', seq)
    if m:
        th = m.group(1).strip()
    else:
        th = seq
    # Only keep reasonable length headings
    if len(th) > 3:
        headings_data.append(th)

# Sort headings by length descending so we match longer ones first
headings_data.sort(key=len, reverse=True)

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

new_chunks = []
print(f"Processing {len(chunks)} chunks...")

for idx, c in enumerate(chunks):
    text = c.get('text', '')
    text_norm = re.sub(r'\s+', ' ', text).replace('\ufffd', '-').replace('\u2014', '-').replace('\u2013', '-')
    
    # Check if there's any heading embedded in the text
    splits = []
    
    # We only check for headings that might be embedded
    # By searching for headings in text
    for th in headings_data:
        # Find all exact string matches of th in text_norm
        # Only if it starts at a word boundary
        start_idx = 0
        while True:
            pos = text_norm.find(th, start_idx)
            if pos == -1:
                break
            
            # Check boundaries
            valid_start = pos == 0 or text_norm[pos-1].isspace()
            valid_end = pos + len(th) == len(text_norm) or text_norm[pos+len(th)].isspace()
            
            if valid_start and valid_end:
                splits.append({'start': pos, 'end': pos + len(th), 'heading': th})
            
            start_idx = pos + 1

    if not splits:
        new_chunks.append(c)
        continue
        
    splits.sort(key=lambda x: x['start'])
    
    filtered_splits = []
    last_end = -1
    for s in splits:
        if s['start'] >= last_end:
            filtered_splits.append(s)
            last_end = s['end']

    if not filtered_splits:
        new_chunks.append(c)
        continue

    # Split the chunk
    import copy
    
    # Check if the first split is just the current heading
    if filtered_splits[0]['start'] < 10:
        c['heading'] = filtered_splits[0]['heading']
        text_norm = text_norm[filtered_splits[0]['end']:].strip()
        text_norm = re.sub(r'^[\s\.\-]+', '', text_norm).strip()
        c['text'] = text_norm
        filtered_splits.pop(0)
    
    if not filtered_splits:
        new_chunks.append(c)
        continue
        
    print(f"Chunk {idx} being split into {len(filtered_splits)+1} parts.")
    
    # If there's prefix text before the first remaining split
    first_start = filtered_splits[0]['start']
    prefix_text = text_norm[:first_start].strip()
    
    current_chunk = copy.deepcopy(c)
    if prefix_text:
        current_chunk['text'] = prefix_text
        new_chunks.append(current_chunk)
        
    for i, s in enumerate(filtered_splits):
        start_pos = s['end']
        end_pos = filtered_splits[i+1]['start'] if i+1 < len(filtered_splits) else len(text_norm)
        
        body_text = text_norm[start_pos:end_pos].strip()
        body_text = re.sub(r'^[\s\.\-]+', '', body_text).strip()
        
        new_c = copy.deepcopy(c)
        new_c['heading'] = s['heading']
        new_c['text'] = body_text
        if i > 0 or prefix_text:
            new_c['has_table'] = False
            new_c['table_html'] = "{}"
            
        new_chunks.append(new_c)

# Clean headings for all chunks
for c in new_chunks:
    h = c.get('heading', '')
    h = h.replace('\ufffd', '-').replace('\u2014', '-').replace('\u2013', '-')
    c['heading'] = h

with open(output_path, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Finished. Total chunks: {len(new_chunks)}")
