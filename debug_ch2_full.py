import json
import fitz
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\parsed_toc.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

giant_text = ""
page_starts = {}
for p in range(80, 324):
    if p-1 < len(doc):
        text = doc[p-1].get_text()
        page_starts[p] = len(giant_text)
        giant_text += " " + text

vc_list = [c for c in chunks if str(c['chapter']) == '2']
available_pages = sorted(page_starts.keys())

indices = [0] * len(vc_list)
for i, vc in enumerate(vc_list):
    expected_page = 0
    for t in toc.get('2', []):
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
            
    search_start = page_starts.get(start_page, 0)
    
    end_page = expected_page
    for _ in range(3):
        next_pages = [p for p in available_pages if p > end_page]
        if next_pages:
            end_page = next_pages[0]
            
    search_end = page_starts.get(end_page, len(giant_text))
    
    title = vc['title'] if '-' not in vc['heading'] else vc['heading'].split('-', 1)[1].strip()
    para_num = str(vc.get('para'))
    
    search_window = giant_text[search_start:search_end].lower()
    
    def build_regex(text):
        words = [re.escape(w) for w in re.split(r'\W+', text.strip()) if w]
        return r'\W+'.join(words)
        
    exact_title = f"{para_num}. {title}".lower()
    pattern_str = build_regex(exact_title)
    
    m = re.search(pattern_str, search_window)
    if not m:
        m = re.search(build_regex(title.lower()), search_window)
        
    if not m:
        words = [w for w in re.split(r'\W+', title.lower()) if len(w) > 3]
        if len(words) >= 2:
            m = re.search(build_regex(f"{words[0]} {words[1]}"), search_window)
            
    if not m:
        if len(words) >= 3:
            m = re.search(build_regex(f"{words[1]} {words[2]}"), search_window)

    if m:
        indices[i] = search_start + m.start()
        print(f"[{i}] Para {para_num}: found at {indices[i]}")
    else:
        closest_expected = expected_page
        if expected_page not in available_pages:
            prev_pages = [p for p in available_pages if p < expected_page]
            if prev_pages:
                closest_expected = prev_pages[-1]
        indices[i] = page_starts.get(closest_expected, search_start)
        print(f"[{i}] Para {para_num}: NOT FOUND, set to {indices[i]} based on page {closest_expected}")

for i in range(1, len(indices)):
    if indices[i] < indices[i-1]:
        print(f"WARNING: indices[{i}] ({indices[i]}) < indices[{i-1}] ({indices[i-1]}), so setting indices[{i}] = {indices[i-1]}")
        indices[i] = indices[i-1]
