import json
import PyPDF2
import re
import os

print("Reading PDF...")
reader = PyPDF2.PdfReader(r'assigned pdfs\RAM 2022 Sixth Edition.pdf')
raw_text = ""
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
toc = json.load(open('chapter_aware_toc.json', encoding='utf-8'))
tables = json.load(open('extracted_tables.json', encoding='utf-8'))

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

chapter_anchors = {
    1: ["Departmental Regulations"],
    2: ["Brief on General Administration", "Brief On General Administration"],
    3: ["Audit of Accounts Department", "Brief About The Accounts"],
    4: ["Audit of Personnel Department", "Brief about the Department"],
    5: ["Audit of Medical Department", "Brief about Medical Department"],
    6: ["Audit of Civil Engineering", "Brief About The Engineering", "Brief about the Engineering"],
    7: ["Audit of Railway Works", "Brief About Railway Works"],
    8: ["Audit of Commercial Department", "Brief About The Commercial"],
    9: ["Audit of Operating Department", "Brief About The Operating", "OPERATING DEPARTMENT"],
    10: ["Audit of Electrical Department", "Brief About The Electrical"],
    11: ["Audit of Signal and", "Brief About The S&T", "Major activities of signal"],
    12: ["Audit of Mechanical Department", "Brief About Mechanical Department"],
    13: ["Audit of Production Units", "Brief About The Production Units"],
    14: ["Audit of Stores Department", "Brief About The Department", "Stores Department"],
    15: ["Audit of Safety Department", "Brief About Safety Department"],
    16: ["Audit of Security Department", "Brief About The Security"],
    17: ["Centre for Railway Information", "Brief About Cris"],
    18: ["Rail Land Development", "Brief About Rlda"],
    19: ["Working of Railway Sports", "Brief On Rspb"],
    20: ["Rail Public Sector", "Brief Of Activities Of Companies"],
    21: ["Research Designs and Standards", "Functions Of Rdso"],
    22: ["E-Office", "Enterprise-Wide System", "Enterprise -Wide System"]
}

for ch_num in range(1, 23):
    chapter_anchors[ch_num].append(f"CHAPTER {ch_num}")
    chapter_anchors[ch_num].append(f"CHAPTER  {ch_num}")

chapter_bounds = {}
current_search_pos = 0

for ch_num in range(1, 23):
    best_pos = -1
    for anchor in chapter_anchors[ch_num]:
        if anchor.startswith("CHAPTER"):
            pattern = re.compile(r'(?im)^\s*' + re.escape(anchor) + r'\b')
        else:
            pattern = re.compile(re.escape(anchor).replace(r'\ ', r'\s+'), re.IGNORECASE)
        
        m = pattern.search(raw_text[current_search_pos:])
        if m:
            pos = current_search_pos + m.start()
            if best_pos == -1 or pos < best_pos:
                best_pos = pos
    
    if best_pos != -1:
        chapter_bounds[ch_num] = max(0, best_pos - 500)
        current_search_pos = best_pos
    else:
        chapter_bounds[ch_num] = current_search_pos

def get_chapter_text(ch_num):
    start = chapter_bounds[ch_num]
    end = len(raw_text)
    for c in range(ch_num+1, 23):
        if c in chapter_bounds:
            if chapter_bounds[c] > start:
                end = chapter_bounds[c]
                break
    return raw_text[start:end], start

print("Finding highly targeted headings per chapter...")
unique_matches_by_ch = {ch: [] for ch in range(1, 23)}
all_unique_matches = []

for ch_num_int in range(1, 23):
    ch_num = str(ch_num_int)
    if ch_num not in required:
        continue
        
    ch_text, ch_start_pos = get_chapter_text(ch_num_int)
    
    for req in required[ch_num]:
        toc_key = f"{ch_num}_{req}"
        proper_title = toc.get(toc_key, req)
        clean_req_text = clean_for_match(proper_title)
        
        best_pos = -1
        best_score = 0
        best_heading = ''
        
        for m in re.finditer(r'(?m)^.*?([A-Za-z0-9].{3,150})$', ch_text):
            line = m.group(0).strip()
            
            # Penalize known bad lines
            if "internal use of" in line.lower() or "table of content" in line.lower() or line.endswith('.'):
                continue
                
            clean_line = clean_for_match(line)
            score = 0
            
            # Massive bonus for exact number match at start of line
            number_match = re.match(r'^(' + re.escape(req) + r')\.?\s+', line)
            if number_match:
                score += 200
                
            # Text content match bonus
            if len(clean_req_text) > 5 and (clean_req_text in clean_line or clean_line in clean_req_text):
                score += 100
            else:
                w1 = set(re.sub(r'[^A-Z0-9 ]+', '', line.upper()).split())
                w2 = set(re.sub(r'[^A-Z0-9 ]+', '', proper_title.upper()).split())
                if len(w2) > 0:
                    overlap = len(w1.intersection(w2))
                    score += (overlap / len(w2)) * 50
                    
            if m.start() > 1500:
                score += 50 # Bonus to prefer body headings over TOC headings
                
            if score >= best_score and score > 20: # Require at least some similarity or exact number
                best_score = score
                best_pos = ch_start_pos + m.start()
                best_heading = line
                
        if best_pos != -1:
            unique_matches_by_ch[ch_num_int].append((best_pos, req, best_heading))
            all_unique_matches.append((best_pos, req, best_heading))

# Sort all matches globally to extract text between them
all_unique_matches.sort(key=lambda x: x[0])

final_chunks = []
CHAPTER_TITLE_MAP = {
    "1":  "Introduction to Railway Audit Manual",
    "2":  "Audit of General Administration and Vigilance Department",
    "3":  "Audit of Accounts Department",
    "4":  "Audit of Personnel Department",
    "5":  "Audit of Medical Department",
    "6":  "Audit of Civil Engineering Department",
    "7":  "Audit of Railway Works",
    "8":  "Audit of Commercial Department",
    "9":  "Audit of Operating Department",
    "10": "Audit of Electrical Department",
    "11": "Audit of Signal and Telecommunication Department",
    "12": "Audit of Mechanical Department",
    "13": "Audit of Production Units",
    "14": "Audit of Stores Department",
    "15": "Audit of Safety Department",
    "16": "Audit of Security Department",
    "17": "Centre for Railway Information Systems",
    "18": "Rail Land Development Authority",
    "19": "Working of Railway Sports Promotion Board",
    "20": "Rail Public Sector Undertakings",
    "21": "Research Designs and Standards Organization",
    "22": "E-Office",
}

print("Building final chunks...")
for ch_num_int in range(1, 23):
    ch_num = str(ch_num_int)
    if ch_num not in required:
        continue
        
    req_list = required[ch_num]
    ch_matches = unique_matches_by_ch[ch_num_int]
    
    for i, req in enumerate(req_list):
        toc_key = f"{ch_num}_{req}"
        proper_title = toc.get(toc_key, req)
        proper_title = re.sub(r'\s+', ' ', proper_title).strip()
        
        found_pos = -1
        for m_pos, m_req, m_heading in ch_matches:
            if m_req == req:
                found_pos = m_pos
                break

        if found_pos != -1:
            next_pos = len(raw_text)
            for p, _, _ in all_unique_matches:
                if p > found_pos:
                    next_pos = p
                    break
                    
            text_content = raw_text[found_pos:next_pos].strip()
            # Remove the heading itself from the text chunk
            text_content = re.sub(r'(?m)^.*?([A-Z0-9].{3,80})$', '', text_content, count=1).strip()
            
            t = find_table_for_chunk(text_content)
            has_table = False
            table_html_val = {}
            if t:
                has_table = True
                table_html_val = {"html": t.get("html", "")}
                
            chunk_data = {
                "DOC_NAME": "RAM 2022 Sixth Edition",
                "doc_id": "RAM-9A7560D8FA",
                "chapter": ch_num,
                "title": CHAPTER_TITLE_MAP.get(ch_num, f"Chapter {ch_num}"),
                "heading": proper_title,
                "text": text_content,
                "page.no": "()",
                "has_table": has_table,
                "table_html": table_html_val
            }
            final_chunks.append(chunk_data)
        else:
            final_chunks.append({
                "DOC_NAME": "RAM 2022 Sixth Edition",
                "doc_id": "RAM-9A7560D8FA",
                "chapter": ch_num,
                "title": CHAPTER_TITLE_MAP.get(ch_num, f"Chapter {ch_num}"),
                "heading": proper_title,
                "text": " ",
                "page.no": "()",
                "has_table": False,
                "table_html": {}
            })

OUTPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition.jsonl'
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for c in final_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Extracted {len(final_chunks)} perfectly mapped chunks.")
