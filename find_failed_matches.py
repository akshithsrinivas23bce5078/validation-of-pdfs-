import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Find chunks ending with a lowercase letter (likely cut mid-word)
for i, c in enumerate(chunks):
    if c['chapter'] == '4':
        text = c.get('text', '').strip()
        if text and text[-1].islower() and not text[-1] in ['s', 'd', 't', 'n', 'y', 'e', 'l', 'r']: # Just a heuristic
            print(f"Chunk {i} ({c['heading']}) ends with: {repr(text[-20:])}")

# Let's also re-run the matching logic from fix_alignment_lfad.py to see WHICH ONES failed!
import fitz
doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

ch_ranges = {'4': (399, 514)}
ch_texts = {'4': ""}
page_starts = {'4': {}}

for p in range(399, 514 + 1):
    if p-1 < len(doc):
        text = doc[p-1].get_text()
        page_starts['4'][p] = len(ch_texts['4'])
        ch_texts['4'] += " " + text

giant_text = ch_texts['4']
available_pages = sorted(page_starts['4'].keys())

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\parsed_toc.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

for c in chunks:
    if c['chapter'] != '4': continue
    
    expected_page = 0
    for t in toc.get('4', []):
        if t['para'] == c.get('para'):
            expected_page = t['page']
            break
            
    if expected_page == 0:
        expected_page = available_pages[0] if available_pages else 0
        
    start_page = expected_page
    for _ in range(3):
        prev_pages = [p for p in available_pages if p < start_page]
        if prev_pages:
            start_page = prev_pages[-1]
            
    search_start = page_starts['4'].get(start_page, 0)
    
    end_page = expected_page
    for _ in range(3):
        next_pages = [p for p in available_pages if p > end_page]
        if next_pages:
            end_page = next_pages[0]
            
    search_end = page_starts['4'].get(end_page, len(giant_text))
    search_end = max(search_end, search_start + 10000)
    
    para_num = str(c.get('para'))
    search_window = giant_text[search_start:search_end]
    
    pattern = r'(?m)^\s*(?:Para\s*)?' + re.escape(para_num) + r'\b[\.\-\)]\s*'
    m = re.search(pattern, search_window, re.IGNORECASE)
    
    if not m:
        title = c['title'] if '-' not in c['heading'] else c['heading'].split('-', 1)[1].strip()
        first_word = re.split(r'\W+', title.strip())[0]
        if len(first_word) > 2:
            pattern2 = r'(?m)^\s*(?:Para\s*)?' + re.escape(para_num) + r'\b.*?' + re.escape(first_word)
            m = re.search(pattern2, search_window, re.IGNORECASE)
            
    if not m:
        print(f"FAILED TO MATCH: {c['heading']} (Para {para_num}) expected around page {expected_page}")
        # Show a little bit of text from the expected page to see what's actually there
        expected_start = page_starts['4'].get(expected_page, 0)
        print("   Text at expected page:\n", giant_text[expected_start:expected_start+200])

