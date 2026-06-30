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

print("Finding all numeric headings...")
matches = []
for m in re.finditer(r'(?m)^(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Za-z][^\n]{3,150})$', raw_text):
    pos = m.start()
    num = m.group(1)
    text_content = m.group(2).strip()
    
    if "internal use of" in text_content or "Railway Audit" in text_content:
        continue
    if "Table of Content" in text_content.title():
        continue
    if text_content.endswith('.') or len(text_content.split()) > 20:
        continue
        
    full_heading = f"{num} {text_content}"
    matches.append((pos, num, full_heading))

for m in re.finditer(r'(?i)(Organizational\s*set\s*up)', raw_text):
    matches.append((m.start(), "3", "3. Organizational Set Up"))
for m in re.finditer(r'(?i)(All\s*India\s*Railway\s*Map)', raw_text):
    matches.append((m.start(), "3.3", "3.3 All India Railway Map With Jurisdiction & Headquarters Only"))

matches.sort(key=lambda x: x[0])

unique_matches = []
seen_pos = set()
for m in matches:
    if not any(abs(p - m[0]) < 10 for p in seen_pos):
        unique_matches.append(m)
        seen_pos.add(m[0])

print(f"Found {len(unique_matches)} numeric headings.")

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

chunks = []
current_match_idx = 0

for ch_num in range(1, 23):
    ch_num = str(ch_num)
    if ch_num not in required:
        continue
        
    req_list = required[ch_num]
    positions = []
    
    for req in req_list:
        found = False
        # Look forward in unique_matches for the next occurrence of `req`
        # We allow skipping at most 100 matches to avoid jumping chapters if one is missing
        for search_idx in range(current_match_idx, min(current_match_idx + 100, len(unique_matches))):
            match_pos, match_num, match_heading = unique_matches[search_idx]
            if match_num == req:
                positions.append((match_pos, match_heading))
                current_match_idx = search_idx + 1
                found = True
                break
                
        if not found:
            print(f"Error: Could not find '{req}' in Chapter {ch_num}")
            
    for i in range(len(positions)):
        pos, heading = positions[i]
        
        if i + 1 < len(positions):
            next_pos = positions[i+1][0]
        else:
            # For the last heading, grab text until the next chapter marker or 50k chars
            next_ch = str(int(ch_num) + 1)
            ch_match = re.search(rf'(?im)^\s*CHAPTER\s+{next_ch}\b', raw_text[pos:])
            if ch_match:
                next_pos = pos + ch_match.start()
            else:
                next_pos = min(pos + 50000, len(raw_text))
                
        line_end = raw_text.find('\n', pos)
        if line_end == -1 or line_end > next_pos:
            line_end = pos
            
        text_content = raw_text[line_end:next_pos].strip()
        text_content = re.sub(r'(?m)^(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Z].{3,80})$', '', text_content)
        
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
            "heading": heading,
            "text": text_content.strip(),
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
