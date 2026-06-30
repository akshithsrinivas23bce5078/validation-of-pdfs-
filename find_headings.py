import json
import re

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'

with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

ch_ranges = {
    '1': (16, 79),
    '2': (80, 323),
    '3': (324, 399),
    '4': (400, 514)
}

ch_texts = {'1': "", '2': "", '3': "", '4': ""}
for rc in raw_chunks:
    p = rc.get('start_page', 0)
    for ch, (s, e) in ch_ranges.items():
        if s <= p <= e:
            ch_texts[ch] += " " + rc.get('content', '')

for ch in ch_texts:
    ch_texts[ch] = clean_text(ch_texts[ch])

found_count = 0
total_count = 0

for ch in ['1', '2', '3', '4']:
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    giant_text = ch_texts[ch]
    
    for vc in vc_list:
        total_count += 1
        heading = vc['heading']
        match = re.match(r'Para\s+(\d+)\s+-\s+(.*)', heading, re.IGNORECASE)
        if not match: continue
        
        num = match.group(1)
        title = match.group(2).strip()
        
        words = [w for w in re.split(r'\W+', title) if len(w) > 3]
        
        # Build regex to find "X. Word1 Word2"
        idx = -1
        
        # Strategy 1: Exact match of number and full title
        pattern1 = rf'\b{num}[\.\)\-\s]+{re.escape(title)}\b'
        m = re.search(pattern1, giant_text, re.IGNORECASE)
        if m:
            idx = m.start()
        else:
            # Strategy 2: Number and first 2 significant words
            if len(words) >= 2:
                pattern2 = rf'\b{num}[\.\)\-\s]+{re.escape(words[0])}\s+{re.escape(words[1])}'
                m = re.search(pattern2, giant_text, re.IGNORECASE)
                if m: idx = m.start()
            
            # Strategy 3: Number and first significant word
            if idx == -1 and len(words) >= 1:
                pattern3 = rf'\b{num}[\.\)\-\s]+{re.escape(words[0])}'
                m = re.search(pattern3, giant_text, re.IGNORECASE)
                if m: idx = m.start()
                
        if idx != -1:
            found_count += 1
        else:
            print(f"Could not find: {heading}")

print(f"Found {found_count} out of {total_count} headings.")
