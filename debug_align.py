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

ch_ranges = {'1': (16, 79)}
ch_texts = {'1': ""}
page_starts = {'1': {}}

for rc in raw_chunks:
    p = rc.get('start_page', 0)
    if 16 <= p <= 79:
        text_to_add = " " + clean_text(rc.get('content', ''))
        page_starts['1'][p] = len(ch_texts['1'])
        ch_texts['1'] += text_to_add

ch_texts['1'] = ch_texts['1'].strip()
giant_text = ch_texts['1']

vc_list = [c for c in val_chunks if str(c['chapter']) == '1']
available_pages = sorted(page_starts['1'].keys())

indices = [0] * len(vc_list)
found = [False] * len(vc_list)

for i, vc in enumerate(vc_list):
    expected_page = 0
    for t in toc.get('1', []):
        if t['para'] == vc.get('para'):
            expected_page = t['page']
            break
            
    start_page = expected_page
    for _ in range(3):
        prev_pages = [p for p in available_pages if p < start_page]
        if prev_pages:
            start_page = prev_pages[-1]
            
    search_start = page_starts['1'].get(start_page, 0)
    
    end_page = expected_page
    for _ in range(3):
        next_pages = [p for p in available_pages if p > end_page]
        if next_pages:
            end_page = next_pages[0]
            
    search_end = page_starts['1'].get(end_page, len(giant_text))
    
    title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
    words = [w for w in re.split(r'\W+', title) if len(w) > 3]
    
    search_window = giant_text[search_start:search_end].lower()
    
    idx_in_window = search_window.find(title.lower())
    match_type = "EXACT"
    
    if idx_in_window == -1 and len(words) >= 2:
        phrase = f"{words[0]} {words[1]}".lower()
        idx_in_window = search_window.find(phrase)
        match_type = "WORDS 0+1"
        
    if idx_in_window == -1 and len(words) >= 3:
        phrase = f"{words[1]} {words[2]}".lower()
        idx_in_window = search_window.find(phrase)
        match_type = "WORDS 1+2"
        
    if idx_in_window != -1:
        indices[i] = search_start + idx_in_window
        found[i] = True
    else:
        closest_expected = expected_page
        if expected_page not in available_pages:
            prev_pages = [p for p in available_pages if p < expected_page]
            if prev_pages:
                closest_expected = prev_pages[-1]
        indices[i] = page_starts['1'].get(closest_expected, search_start)
        match_type = f"FALLBACK ({closest_expected})"
        
    print(f"Para {vc.get('para')}: Expected={expected_page}, Search=[{start_page}, {end_page}], Start={search_start}, End={search_end}")
    print(f"   Match: {match_type}, idx_in_window: {idx_in_window}, FINAL INDEX: {indices[i]}")

print("Applying monotonicity:")
for i in range(1, len(indices)):
    if indices[i] < indices[i-1]:
        print(f"   Fixing Para {vc_list[i].get('para')} ({indices[i]}) -> ({indices[i-1]})")
        indices[i] = indices[i-1]
