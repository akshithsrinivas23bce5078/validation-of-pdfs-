import json
import re

raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

for vc in val_chunks:
    vc['text'] = ""

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def get_para_num_and_words(val_heading):
    match = re.match(r'Para\s+(\d+)\s*-\s*(.+)', val_heading, re.IGNORECASE)
    if not match: return 0, []
    num = int(match.group(1))
    title = match.group(2)
    words = [w.lower() for w in re.split(r'\W+', title) if len(w) >= 3]
    return num, words

def is_match(raw_heading, num, words):
    if not raw_heading: return False
    rh = raw_heading.strip().lower()
    
    # Needs to have the number
    num_pattern = rf'^{num}[\.\)\-\s]'
    if not re.search(num_pattern, rh):
        return False
        
    # Needs to match at least one word from the title (or title is too short)
    if not words: return True
    if any(w in rh for w in words):
        return True
    return False

def get_ch(p):
    if 16 <= p <= 79: return '1'
    if 80 <= p <= 323: return '2'
    if 324 <= p <= 399: return '3'
    if 400 <= p <= 515: return '4'
    return ''

for ch in ['1', '2', '3', '4']:
    rc_list = [c for c in raw_chunks if get_ch(c.get('start_page', 0)) == ch]
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    
    if not rc_list or not vc_list: continue
    
    active_vc_idx = 0  # Start with the first paragraph active
    
    # We might have preamble text before Para 1 starts, it goes into Para 1.
    
    for rc in rc_list:
        rh = rc.get('heading', '')
        
        # Check next few paragraphs to see if this raw chunk starts one of them
        matched_idx = -1
        # Check up to 3 paragraphs ahead to handle skipping
        for ahead in range(1, 4):
            if active_vc_idx + ahead < len(vc_list):
                next_vc = vc_list[active_vc_idx + ahead]
                num, words = get_para_num_and_words(next_vc['heading'])
                if is_match(rh, num, words):
                    matched_idx = active_vc_idx + ahead
                    break
        
        if matched_idx != -1:
            active_vc_idx = matched_idx
            
        # Append content
        # Sometimes heading text itself should be included? The original raw_chunks had the heading separated from content.
        # But we already have the heading in val_chunks. So just append content.
        text_to_add = rc.get('content', '').strip()
        if text_to_add:
            vc_list[active_vc_idx]['text'] += " " + text_to_add

# Verify Pilgrim Tax
for c in val_chunks:
    if 'Pilgrim Tax' in c['heading']:
        print(f"\\n--- {c['heading']} ---")
        print(c['text'][:200])

empty = [c['heading'] for c in val_chunks if not c['text'].strip()]
print(f"\\nEmpty chunks remaining: {len(empty)}")
if empty:
    print(empty[:10])

with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        c['text'] = clean_text(c['text'])
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
