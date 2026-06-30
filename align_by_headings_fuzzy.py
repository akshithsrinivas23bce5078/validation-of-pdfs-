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
    
    indices = [0] * len(vc_list)
    found = [False] * len(vc_list)
    
    # 1. Find indices using fuzzy search
    for i, vc in enumerate(vc_list):
        total_count += 1
        title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
        words = [w for w in re.split(r'\W+', title) if len(w) > 3]
        
        idx = -1
        # Search for exact title
        idx = giant_text.lower().find(title.lower())
        
        if idx == -1 and len(words) >= 2:
            # Search for first two words
            phrase = f"{words[0]} {words[1]}".lower()
            idx = giant_text.lower().find(phrase)
            
        if idx == -1 and len(words) >= 3:
            # Search for words 2 and 3
            phrase = f"{words[1]} {words[2]}".lower()
            idx = giant_text.lower().find(phrase)
            
        if idx != -1:
            indices[i] = idx
            found[i] = True
            found_count += 1
            
    # 2. Fix non-monotonic indices and interpolate missing ones
    # Ensure indices[0] is 0
    indices[0] = 0
    found[0] = True
    
    last_valid = 0
    for i in range(1, len(indices)):
        if found[i]:
            if indices[i] <= indices[last_valid]:
                # Non-monotonic! This means our fuzzy search found a false positive earlier in the text
                # We will mark it as NOT found, and interpolate later
                found[i] = False
            else:
                last_valid = i
                
    # Interpolate
    for i in range(1, len(indices)):
        if not found[i]:
            # Find next valid
            next_valid = -1
            for j in range(i+1, len(indices)):
                if found[j]:
                    next_valid = j
                    break
            
            start_val = indices[i-1]
            end_val = indices[next_valid] if next_valid != -1 else len(giant_text)
            dist = next_valid - (i - 1) if next_valid != -1 else len(indices) - (i - 1)
            
            indices[i] = start_val + (end_val - start_val) // dist
            
    # 3. Slice the text
    indices.append(len(giant_text))
    
    for i in range(len(vc_list)):
        start = indices[i]
        end = indices[i+1]
        vc_list[i]['text'] = clean_text(giant_text[start:end])

# Verify
empty = sum(1 for c in val_chunks if not c.get('text', '').strip())
print(f"Found {found_count} out of {total_count} headings. Empty chunks: {empty}")

# Check Para 4, 6 and 49
for c in val_chunks:
    if str(c['chapter']) == '1' and ('Para 4' in c['heading'] or 'Para 6' in c['heading']):
        print(f"\n--- {c['heading']} ---")
        print(c['text'][:100])
    if str(c['chapter']) == '2' and 'Para 49' in c['heading']:
        print(f"\n--- {c['heading']} ---")
        print(c['text'][:100])

with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
