import json
import re

val_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
raw_path = r'unvalidated chunks\Local Fund Audit Depart Manual  Vol - II.jsonl'

with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

with open(raw_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

with open('parsed_toc.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

ch_ranges = {
    '1': (16, 79),
    '2': (80, 323),
    '3': (324, 399),
    '4': (400, 514)
}

ch_texts = {'1': "", '2': "", '3': "", '4': ""}
page_starts = {'1': {}, '2': {}, '3': {}, '4': {}}

for rc in raw_chunks:
    p = rc.get('start_page', 0)
    for ch, (s, e) in ch_ranges.items():
        if s <= p <= e:
            text_to_add = " " + rc.get('content', '')
            page_starts[ch][p] = len(ch_texts[ch])
            ch_texts[ch] += text_to_add

for ch in ch_texts:
    ch_texts[ch] = clean_text(ch_texts[ch])

found_count = 0
total_count = 0

for ch in ['1', '2', '3', '4']:
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    giant_text = ch_texts[ch]
    available_pages = sorted(page_starts[ch].keys())
    
    indices = [0] * len(vc_list)
    found = [False] * len(vc_list)
    
    for i, vc in enumerate(vc_list):
        total_count += 1
        
        expected_page = 0
        for t in toc.get(ch, []):
            if t['para'] == vc.get('para'):
                expected_page = t['page']
                break
                
        # Find nearest start page <= expected_page
        closest_start_page = 0
        for p in reversed(available_pages):
            if p <= expected_page:
                closest_start_page = p
                break
        
        search_start = page_starts[ch].get(closest_start_page, 0)
        
        # Find end page exactly 3 pages ahead
        end_page = closest_start_page
        for _ in range(3):
            next_pages = [p for p in available_pages if p > end_page]
            if next_pages:
                end_page = next_pages[0]
        
        search_end = page_starts[ch].get(end_page, len(giant_text))
        
        title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
        words = [w for w in re.split(r'\W+', title) if len(w) > 3]
        
        idx = -1
        search_window = giant_text[search_start:search_end].lower()
        
        idx_in_window = search_window.find(title.lower())
        
        if idx_in_window == -1 and len(words) >= 2:
            phrase = f"{words[0]} {words[1]}".lower()
            idx_in_window = search_window.find(phrase)
            
        if idx_in_window == -1 and len(words) >= 3:
            phrase = f"{words[1]} {words[2]}".lower()
            idx_in_window = search_window.find(phrase)
            
        if idx_in_window != -1:
            indices[i] = search_start + idx_in_window
            found[i] = True
            found_count += 1
        else:
            indices[i] = search_start
            
    for i in range(1, len(indices)):
        if indices[i] < indices[i-1]:
            indices[i] = indices[i-1]
            
    indices.append(len(giant_text))
    
    for i in range(len(vc_list)):
        start = indices[i]
        end = indices[i+1]
        vc_list[i]['text'] = clean_text(giant_text[start:end])

print(f"Found {found_count} out of {total_count} headings precisely. Fallbacks used page bounds.")

# Check Paragaphs
for c in val_chunks:
    if str(c['chapter']) == '1' and c.get('para') in [3, 4, 6]:
        print(f"\n--- {c['heading']} ---")
        print(c['text'][:150])
    if str(c['chapter']) == '2' and c.get('para') == 49:
        print(f"\n--- {c['heading']} ---")
        print(c['text'][:150])

with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
