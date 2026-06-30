import json
import re

raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'
val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'

with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

# Clear text fields
for vc in val_chunks:
    vc['text'] = ""

def get_para_num_and_words(val_heading):
    # e.g., "Para 23 - Pilgrim Tax" -> 23, ["Pilgrim", "Tax"]
    match = re.match(r'Para\s+(\d+)\s*-\s*(.+)', val_heading, re.IGNORECASE)
    if not match: return 0, []
    num = int(match.group(1))
    title = match.group(2)
    words = [w.lower() for w in re.findall(r'[a-zA-Z]{3,}', title)]
    return num, set(words)

def is_transition(raw_c, next_vc):
    if not next_vc: return False
    
    r_head = str(raw_c.get('heading', '')).strip().lower()
    r_text = str(raw_c.get('content', '')).strip().lower()
    
    num, words = get_para_num_and_words(next_vc['heading'])
    if num == 0: return False
    
    # Check if raw heading starts with number
    num_pattern = rf'^{num}[\.\)\-\s]'
    if re.search(num_pattern, r_head):
        # Must match at least one significant word from the title
        if any(w in r_head for w in words):
            return True
            
    # Sometimes heading is in text
    # But ONLY if it's the very beginning of the text
    if re.search(rf'^{num}[\.\)\-\s]', r_text[:50]):
        if any(w in r_text[:100] for w in words):
            return True
            
    # Fallback: if c_page is > next_vc's expected page + 2, we missed it, force transition?
    # No, that caused the bug. But we need SOME fallback if OCR totally failed.
    # We will log it instead.
    
    return False

def merge_texts(t1, t2):
    if not t1: return t2
    if not t2: return t1
    max_len = min(len(t1), len(t2), 300)
    for i in range(max_len, 20, -1):
        if t1[-i:] == t2[:i]: return t1 + t2[i:]
    for i in range(max_len, 20, -1):
        if t1[-i:].replace(' ','') == t2[:i].replace(' ',''): return t1 + t2[i:]
    return t1 + ' ' + t2

# Group by chapter
for ch in ['1', '2', '3', '4']:
    def get_ch(p):
        if 16 <= p <= 79: return '1'
        if 80 <= p <= 323: return '2'
        if 324 <= p <= 399: return '3'
        if 400 <= p <= 515: return '4'
        return ''
        
    rc_list = [c for c in raw_chunks if get_ch(c.get('start_page', 0)) == ch]
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    
    if not rc_list or not vc_list: continue
    
    current_vc_idx = 0
    for rc in rc_list:
        next_vc = vc_list[current_vc_idx + 1] if current_vc_idx + 1 < len(vc_list) else None
        
        if is_transition(rc, next_vc):
            current_vc_idx += 1
            
        # Also handle edge case where multiple paragraphs are skipped (unlikely with this logic, but possible)
        # We won't do it yet to see if this pure text-matching works.
        
        vc_list[current_vc_idx]['text'] = merge_texts(vc_list[current_vc_idx]['text'], rc.get('content', ''))

# Check empty chunks
empty = [c['heading'] for c in val_chunks if not c['text'].strip()]
print(f"Empty chunks remaining: {len(empty)}")
if empty:
    print("Some empty chunks:", empty[:10])

# Verify Pilgrim Tax
for c in val_chunks:
    if 'Pilgrim Tax' in c['heading']:
        print(f"\\n--- {c['heading']} ---")
        print(c['text'][:200])

# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
