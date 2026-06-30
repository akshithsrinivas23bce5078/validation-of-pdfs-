import json
import re
import fitz

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\parsed_toc.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

ch_ranges = {
    '1': (16, 78),
    '2': (79, 322),
    '3': (323, 399),
    '4': (400, 514)
}

ch_texts = {'1': "", '2': "", '3': "", '4': ""}
page_starts = {'1': {}, '2': {}, '3': {}, '4': {}}

for ch, (s, e) in ch_ranges.items():
    for p in range(s, e + 1):
        if p-1 < len(doc):
            text = doc[p-1].get_text()
            page_starts[ch][p] = len(ch_texts[ch])
            ch_texts[ch] += " " + text

found_count = 0
total_count = 0
unfound = []

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
                
        if expected_page == 0:
            expected_page = available_pages[0] if available_pages else 0
        
        # Monotonicity constraint: search_start from last found position
        last_found_valid_index = 0
        if i > 0:
            for j in range(i-1, -1, -1):
                if found[j]:
                    last_found_valid_index = indices[j]
                    break
        
        # Get the next paragraph's expected page to set the upper bound
        next_expected_page = available_pages[-1] if available_pages else expected_page
        if i + 1 < len(vc_list):
            for t in toc.get(ch, []):
                if t['para'] == vc_list[i+1].get('para'):
                    next_expected_page = t['page']
                    break
        
        # Search window: from last found index to well past the next paragraph's expected page
        # Use a generous upper bound: next para's page + 15 pages
        search_start = last_found_valid_index
        
        end_page = max(expected_page, next_expected_page)
        for _ in range(15):
            next_pages = [p for p in available_pages if p > end_page]
            if next_pages:
                end_page = next_pages[0]
        
        search_end = page_starts[ch].get(end_page, len(giant_text))
        search_end = max(search_end, search_start + 50000)
        search_end = min(search_end, len(giant_text))
        
        para_num = str(vc.get('para'))
        search_window = giant_text[search_start:search_end]
        
        if '-' in vc['heading']:
            title_part = vc['heading'].split('-', 1)[1].strip()
        else:
            title_part = vc['heading']
        
        title_words = [w for w in re.split(r'\W+', title_part) if len(w) >= 4]
        
        m = None
        
        # STRATEGY 1: number + UPPERCASE title word within 30 chars
        # This is the STRONGEST signal - real headings are in UPPERCASE
        if title_words:
            for tw in title_words[:3]:
                upper_word = tw.upper()
                pattern = r'(?m)^\s*(?:Para\s*)?' + re.escape(para_num) + r'\b[\.\-\)\s][\s\S]{0,30}?' + re.escape(upper_word)
                candidates = list(re.finditer(pattern, search_window))
                
                for cand in candidates:
                    matched_text = search_window[cand.start():cand.end()]
                    if upper_word in matched_text:
                        m = cand
                        break
                
                if m:
                    break
        
        # STRATEGY 1b: Wider window (100 chars) + UPPERCASE
        if not m and title_words:
            for tw in title_words[:3]:
                upper_word = tw.upper()
                pattern = r'(?m)^\s*(?:Para\s*)?' + re.escape(para_num) + r'\b[\.\-\)\s][\s\S]{0,100}?' + re.escape(upper_word)
                candidates = list(re.finditer(pattern, search_window))
                
                for cand in candidates:
                    matched_text = search_window[cand.start():cand.end()]
                    if upper_word in matched_text:
                        m = cand
                        break
                
                if m:
                    break
        
        # STRATEGY 2: Case-insensitive title word match (weaker)
        if not m and title_words:
            for tw in title_words[:3]:
                pattern = r'(?m)^\s*(?:Para\s*)?' + re.escape(para_num) + r'\b[\.\-\)\s][\s\S]{0,100}?' + re.escape(tw)
                candidates = list(re.finditer(pattern, search_window, re.IGNORECASE))
                if candidates:
                    m = candidates[0]
                    break
        
        # STRATEGY 3: Just the number with punctuation (last resort)
        if not m:
            pattern = r'(?m)^\s*(?:Para\s*)?' + re.escape(para_num) + r'\b[\.\-\)]\s+'
            candidates = list(re.finditer(pattern, search_window))
            if candidates:
                m = candidates[0]
            
        if m:
            indices[i] = search_start + m.start()
            found[i] = True
            found_count += 1
        else:
            found[i] = False
            unfound.append(f"Ch{ch} Para {para_num}: {vc['heading']}")

    # Interpolate missing indices
    for i in range(len(indices)):
        if not found[i]:
            prev_val = 0
            prev_idx = -1
            for j in range(i-1, -1, -1):
                if found[j]:
                    prev_val = indices[j]
                    prev_idx = j
                    break
            
            next_val = len(giant_text)
            next_idx = len(indices)
            for j in range(i+1, len(indices)):
                if found[j]:
                    next_val = indices[j]
                    next_idx = j
                    break
            
            num_missing = next_idx - prev_idx - 1
            step = (next_val - prev_val) // (num_missing + 1)
            indices[i] = prev_val + step * (i - prev_idx)

    # Make strictly increasing
    for i in range(1, len(indices)):
        if indices[i] < indices[i-1]:
            indices[i] = indices[i-1]
            
    indices.append(len(giant_text))
    
    # Extract text
    for i in range(len(vc_list)):
        start = indices[i]
        end = indices[i+1]
        vc_list[i]['text'] = clean_text(giant_text[start:end])
        
print(f"Found {found_count} out of {total_count} headings precisely.")
if unfound:
    print(f"\nUnfound headings:")
    for u in unfound:
        print(f"  {u}")

# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
