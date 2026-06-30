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
            text_to_add = " " + clean_text(rc.get('content', ''))
            page_starts[ch][p] = len(ch_texts[ch])
            ch_texts[ch] += text_to_add

for ch in ch_texts:
    ch_texts[ch] = ch_texts[ch].strip()

found_count = 0
total_count = 0

for ch in ['1', '2', '3', '4']:
    vc_list = [c for c in val_chunks if str(c['chapter']) == ch]
    giant_text = ch_texts[ch]
    available_pages = sorted(page_starts[ch].keys())
    
    raw_indices = [None] * len(vc_list)
    
    for i, vc in enumerate(vc_list):
        total_count += 1
        
        expected_page = 0
        for t in toc.get(ch, []):
            if t['para'] == vc.get('para'):
                expected_page = t['page']
                break
                
        start_page = expected_page
        for _ in range(3):
            prev_pages = [p for p in available_pages if p < start_page]
            if prev_pages: start_page = prev_pages[-1]
                
        search_start = page_starts[ch].get(start_page, 0)
        
        end_page = expected_page
        for _ in range(3):
            next_pages = [p for p in available_pages if p > end_page]
            if next_pages: end_page = next_pages[0]
        
        search_end = page_starts[ch].get(end_page, len(giant_text))
        
        title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
        words = [w for w in re.split(r'\W+', title) if len(w) > 3]
        para_num = vc.get('para')
        para_pattern = rf"(?:para[\s\.\:\-]*{para_num}|{para_num}[\s\.\:\-]+)"
        
        search_window = giant_text[search_start:search_end].lower()
        idx_in_window = search_window.find(title.lower())
        
        # High confidence matches
        if idx_in_window == -1 and len(words) >= 2:
            regex1 = para_pattern + r".{0,30}?" + re.escape(f"{words[0]} {words[1]}".lower())
            m = re.search(regex1, search_window)
            if m: idx_in_window = m.start()
            
        if idx_in_window == -1 and len(words) >= 3:
            regex2 = para_pattern + r".{0,30}?" + re.escape(f"{words[1]} {words[2]}".lower())
            m = re.search(regex2, search_window)
            if m: idx_in_window = m.start()
            
        # Medium confidence match: long exact phrase without para prefix
        if idx_in_window == -1 and len(words) >= 2:
            phrase = f"{words[0]} {words[1]}".lower()
            if len(phrase) >= 15:
                idx_in_window = search_window.find(phrase)
            
        if idx_in_window != -1:
            raw_indices[i] = search_start + idx_in_window
            found_count += 1
            
    # Interpolate / Clamp Nones
    indices = [0] * len(vc_list)
    indices[0] = raw_indices[0] if raw_indices[0] is not None else 0
    
    for i in range(1, len(vc_list)):
        if raw_indices[i] is not None:
            indices[i] = raw_indices[i]
        else:
            expected_page = 0
            for t in toc.get(ch, []):
                if t['para'] == vc_list[i].get('para'):
                    expected_page = t['page']
                    break
            
            closest_expected = expected_page
            if expected_page not in available_pages:
                prev_pages = [p for p in available_pages if p < expected_page]
                if prev_pages: closest_expected = prev_pages[-1]
            
            fallback = page_starts[ch].get(closest_expected, indices[i-1])
            indices[i] = fallback

    # Forward Monotonicity Pass
    for i in range(1, len(indices)):
        if indices[i] < indices[i-1]:
            indices[i] = indices[i-1]
            
    # Backward Monotonicity Pass (Clamping fallbacks that overshoot the next known match)
    for i in range(len(indices)-2, -1, -1):
        if indices[i] > indices[i+1]:
            indices[i] = indices[i+1]
            
    # Now there are NO overshoots, and NO non-monotonic arrays!
    # But some lengths might still be 0 if they were completely squeezed. 
    # If they are squeezed, we evenly distribute the gap!
    
    for i in range(len(indices)):
        if i < len(indices)-1 and indices[i] == indices[i+1]:
            # Squeezed! Try to push i backwards if possible
            if i > 0 and indices[i] > indices[i-1] + 100:
                indices[i] -= 100  # Give it at least 100 chars
                
    indices.append(len(giant_text))
    
    for i in range(len(vc_list)):
        start = indices[i]
        end = indices[i+1]
        vc_list[i]['text'] = clean_text(giant_text[start:end])

print(f"Found {found_count} out of {total_count} headings precisely.")

with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
