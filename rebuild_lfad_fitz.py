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
    '1': (16, 79),
    '2': (80, 323),
    '3': (324, 399),
    '4': (400, 514)
}

ch_texts = {'1': "", '2': "", '3': "", '4': ""}
page_starts = {'1': {}, '2': {}, '3': {}, '4': {}}

# The document seems to have printed page numbers which align mostly with 1-based index or maybe a small offset.
# Let's just use the index of the doc. 
# Page 199 (0-indexed 198) has printed '199'. So printed page P is doc[P-1].

for ch, (s, e) in ch_ranges.items():
    for p in range(s, e + 1):
        # p is the printed page number, so doc[p-1] is the fitz page.
        if p-1 < len(doc):
            text = doc[p-1].get_text()
            page_starts[ch][p] = len(ch_texts[ch])
            ch_texts[ch] += " " + text

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
                
        if expected_page == 0:
            expected_page = available_pages[0] if available_pages else 0
            
        start_page = expected_page
        for _ in range(3):
            prev_pages = [p for p in available_pages if p < start_page]
            if prev_pages:
                start_page = prev_pages[-1]
                
        search_start = page_starts[ch].get(start_page, 0)
        
        end_page = expected_page
        for _ in range(3):
            next_pages = [p for p in available_pages if p > end_page]
            if next_pages:
                end_page = next_pages[0]
        
        search_end = page_starts[ch].get(end_page, len(giant_text))
        
        title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
        words = [w for w in re.split(r'\W+', title) if len(w) > 3]
        
        # Adding para number search to make it more precise
        para_num = str(vc.get('para'))
        
        idx = -1
        search_window = giant_text[search_start:search_end].lower()
        
        # Search for exact string "<para>. <title>"
        exact_title = f"{para_num}. {title}".lower()
        idx_in_window = search_window.find(exact_title)
        
        # If not found, try "<para>." and title words
        if idx_in_window == -1:
            idx_in_window = search_window.find(title.lower())
            
        if idx_in_window == -1 and len(words) >= 2:
            phrase = f"{words[0]} {words[1]}".lower()
            idx_in_window = search_window.find(phrase)
            
        if idx_in_window == -1 and len(words) >= 3:
            phrase = f"{words[1]} {words[2]}".lower()
            idx_in_window = search_window.find(phrase)
            
        if idx_in_window != -1:
            # check if we can align closer to the number
            pattern = re.compile(rf'\b{para_num}\s*\.\s+.*?' + re.escape(title.lower()[:10]))
            m = pattern.search(search_window)
            if m:
                indices[i] = search_start + m.start()
            else:
                indices[i] = search_start + idx_in_window
            found[i] = True
            found_count += 1
        else:
            closest_expected = expected_page
            if expected_page not in available_pages:
                prev_pages = [p for p in available_pages if p < expected_page]
                if prev_pages:
                    closest_expected = prev_pages[-1]
            indices[i] = page_starts[ch].get(closest_expected, search_start)
            
    for i in range(1, len(indices)):
        if indices[i] < indices[i-1]:
            indices[i] = indices[i-1]
            
    indices.append(len(giant_text))
    
    for i in range(len(vc_list)):
        start = indices[i]
        end = indices[i+1]
        vc_list[i]['text'] = clean_text(giant_text[start:end])

print(f"Found {found_count} out of {total_count} headings precisely.")

with open('temp_lfad_fixed.jsonl', 'w', encoding='utf-8') as f:
    for c in val_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
