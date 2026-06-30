import json
import PyPDF2
import re
import os

print("Reading PDF...")
reader = PyPDF2.PdfReader(r'assigned pdfs\RAM 2022 Sixth Edition.pdf')
raw_text = ""
# Skip TOC pages (usually 1-30)
for i in range(31, len(reader.pages)):
    raw_text += reader.pages[i].extract_text() + '\n'

print("Cleaning raw text...")
raw_text = re.sub(r'(?m)^Railway Audit Manual\s*$\n^\s*\d+\s*$\n^For internal use of IA&AD\s*$', '', raw_text)
raw_text = re.sub(r'(?m)^Chapter \d+.*?Manual\s*$\n^\s*\d+\s*$\n^For internal use of IA&AD\s*$', '', raw_text)
raw_text = re.sub(r'^\s*\d*\s*For internal use of IA&AD\s*CHAPTER \d+.*?\s*', '', raw_text, flags=re.DOTALL)
raw_text = re.sub(r'\n\s*\d+\s*Refer Headquarters.*?\n', '\n', raw_text)
raw_text = re.sub(r'\n\s*\d+\s*Ministry of Railways.*?\n', '\n', raw_text)
raw_text = re.sub(r'\n\s*\d+\s*Representation purpose only.*?scale\s*\n', '\n', raw_text)
raw_text = re.sub(r'\b\d{1,3}\s+Railway Audit Mana?ual?\b', ' ', raw_text, flags=re.MULTILINE)

required = json.load(open('user_required_subdivisions.json', encoding='utf-8'))
tables = json.load(open('extracted_tables.json', encoding='utf-8'))
toc = json.load(open('chapter_aware_toc.json', encoding='utf-8'))

def clean_for_match(s):
    return re.sub(r'[^A-Z0-9]+', '', s.upper())

tables_map = {}
for t in tables:
    page = str(t.get('page', ''))
    if page not in tables_map:
        tables_map[page] = []
    tables_map[page].append(t)

def find_table_for_chunk(chunk_text):
    chunk_clean = clean_for_match(chunk_text)
    best_table = None
    best_score = 0
    for page, t_list in tables_map.items():
        for t in t_list:
            pre_clean = clean_for_match(t.get('preceding_text', ''))
            if len(pre_clean) > 20 and pre_clean in chunk_clean:
                return t
            
            overlap = 0
            if len(pre_clean) > 0:
                for i in range(10, len(pre_clean), 10):
                    if pre_clean[i:i+20] in chunk_clean:
                        overlap += 1
                score = overlap / max(1, len(pre_clean) / 10)
                if score > best_score and score > 0.3:
                    best_score = score
                    best_table = t
    return best_table

chunks = []
current_search_pos = 0

for ch_num in range(1, 23):
    ch_num = str(ch_num)
    if ch_num not in required:
        continue
        
    req_list = required[ch_num]
    positions = []
    
    for req in req_list:
        key = f"{ch_num}_{req}"
        title = toc.get(key, req)
        
        words = title.split()
        if len(words) > 1:
            sig_words = [re.escape(w.rstrip('.')) for w in words[1:5]]
            regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+' + r'\s+'.join(sig_words)
        else:
            regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+([A-Za-z].*)'
            
        pattern = re.compile(regex)
        match = pattern.search(raw_text, current_search_pos)
        
        if not match:
            if len(words) > 1:
                sig_words = [re.escape(words[1].rstrip('.'))]
                regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+' + r'\s+'.join(sig_words)
                pattern = re.compile(regex)
                match = pattern.search(raw_text, current_search_pos)
                
            if not match:
                regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+[A-Za-z]'
                pattern = re.compile(regex)
                match = pattern.search(raw_text, current_search_pos)
                
        if match:
            heading_full = title
            pos = match.start()
            positions.append((pos, heading_full))
            current_search_pos = pos + 1
        else:
            print(f"Error: Could not find '{req}' in Chapter {ch_num}")
            
    # Extract text between these positions
    for i in range(len(positions)):
        pos, heading = positions[i]
        
        if i + 1 < len(positions):
            next_pos = positions[i+1][0]
        else:
            # End of chapter -> find next chapter marker
            next_ch = str(int(ch_num) + 1)
            ch_match = re.search(rf'(?im)^\s*CHAPTER\s+{next_ch}\b', raw_text[pos:])
            if ch_match:
                next_pos = pos + ch_match.start()
            else:
                next_pos = min(pos + 50000, len(raw_text))
                
        text_content = raw_text[pos:next_pos].strip()
        
        t = find_table_for_chunk(text_content)
        has_table = False
        table_html_val = {}
        if t:
            has_table = True
            table_html_val = {"html": t.get("html", "")}
            
        chunk_data = {
            "chapter": ch_num,
            "title": f"Chapter {ch_num}",
            "heading": heading,
            "text": text_content,
            "page.no": "()",
            "has_table": has_table,
            "table_html": table_html_val
        }
        chunks.append(chunk_data)

print(f"Extracted {len(chunks)} chunks.")

OUTPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition.jsonl'
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
print("Saved exact chunks.")
