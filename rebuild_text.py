import json
import fitz
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\19__Opening_Balance_Sheet_Accounting_Manual_P_State_Audit_West_Ben.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# 1. Fix chapter numbers
for c in chunks:
    first_token = c['text'].split(' ')[0]
    m = re.match(r'^(\d+)', first_token)
    if m:
        c['chapter'] = m.group(1)
        
# 2. Add 3.4
if not any(c['text'].startswith('3.4') for c in chunks):
    idx_33 = next(i for i, c in enumerate(chunks) if c['text'].startswith('3.3'))
    dummy = dict(chunks[idx_33])
    dummy['text'] = '3.4 '
    chunks.insert(idx_33 + 1, dummy)

def advanced_sort_key(c):
    ch = str(c['chapter'])
    chapter_val = int(ch) if ch.isdigit() else 9999
    
    first_token = c['text'].split(' ')[0]
    m = re.match(r'^(\d+(?:\.\d+)*)', first_token)
    if m:
        parts = m.group(1).split('.')
        sub_sort = [int(p) for p in parts]
    else:
        sub_sort = [9999]
    return (chapter_val, sub_sort)

chunks.sort(key=advanced_sort_key)

pdfpath = r'C:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\19. Opening Balance Sheet Accounting Manual P_State Audit West Ben.pdf'
doc = fitz.open(pdfpath)
text = ''
for p in doc:
    text += p.get_text()

text = re.sub(r' Guidelines for Opening Balance Sheet \n\d+\n', '\n', text)

positions = {}
for i, c in enumerate(chunks):
    p = c['text'].split(' ')[0]
    match_str = p
    if re.match(r'^\d+\.\d+\.[A-Za-z]+', p):
        match_str = re.match(r'^(\d+\.\d+)', p).group(1)
        
    if re.match(r'^\d+$', match_str):
        pattern = r'(?m)^\s*' + re.escape(match_str) + r'\.(?:\.|\s)'
        if match_str == "1":
            pattern = r'(?m)^AS\nAccounting'
        elif match_str == "29":
            pattern = r'(?m)^\s*29\s+SHEET'
    else:
        pattern = r'(?m)^\s*' + re.escape(match_str) + r'(?:\.|\s)'
        
    matches = list(re.finditer(pattern, text))
    valid_matches = [m for m in matches if m.start() > 12000]
    
    if valid_matches:
        positions[i] = valid_matches[0].start()
    else:
        print('NOT FOUND:', p)

if len(positions) == len(chunks):
    sorted_pos = sorted([(pos, idx) for idx, pos in positions.items()])
    
    for k in range(len(sorted_pos)):
        pos, idx = sorted_pos[k]
        if k + 1 < len(sorted_pos):
            end_pos = sorted_pos[k+1][0]
        else:
            end_pos = len(text)
            
        chunk_text = text[pos:end_pos].strip()
        chunk_text = " ".join(chunk_text.split())
        
        p_str = chunks[idx]['text'].split(' ')[0]
        if re.match(r'^\d+\.\d+$', p_str) or re.match(r'^\d+$', p_str):
            chunk_text = re.sub(r'^' + re.escape(p_str) + r'\.\s*', p_str + ' ', chunk_text)
            
        if p_str == "1":
            chunk_text = "1 " + chunk_text
            
        chunks[idx]['text'] = chunk_text
        
    with open(filepath, 'w', encoding='utf-8') as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
            
    print(f"Successfully replaced text for all {len(chunks)} chunks, including 3.4.")
else:
    print(f"Failed. Found {len(positions)} out of {len(chunks)}.")
