import re
import json
import PyPDF2

def norm(s):
    return re.sub(r'[^A-Z0-9]+', '', s.upper())

# 1. Load TOC Mapping and identify 1-level and 2-level headings
toc = json.load(open('new_toc_mapping.json', encoding='utf-8'))
valid_headings = {}
for k, v in toc.items():
    num_part = v.split()[0]
    nums = [x for x in num_part.split('.') if x]
    if len(nums) <= 2 and re.match(r'^\d+(\.\d+)?$', num_part):
        valid_headings[v] = num_part

valid_headings["3. Organizational Set Up"] = "3"

def sort_key(v):
    num_str = v.split()[0]
    nums = [int(x) for x in num_str.split('.') if x.isdigit()]
    return nums

sorted_headings = sorted(list(valid_headings.keys()), key=sort_key)

# 2. Extract HTML tables
tables_map = {}
try:
    with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            c = json.loads(line)
            if c.get('has_table'):
                tables_map[c['heading']] = c['table_html']
except FileNotFoundError:
    pass

# 3. Read PDF
reader = PyPDF2.PdfReader(r'assigned pdfs\RAM 2022 Sixth Edition.pdf')
raw_text = ""
for i in range(31, len(reader.pages)):
    raw_text += reader.pages[i].extract_text() + '\n'

# 4. Clean raw text
raw_text = re.sub(r'(?m)^Railway Audit Manual\s*$\n^\s*\d+\s*$\n^For internal use of IA&AD\s*$', '', raw_text)
raw_text = re.sub(r'(?m)^Chapter \d+.*?Manual\s*$\n^\s*\d+\s*$\n^For internal use of IA&AD\s*$', '', raw_text)
raw_text = re.sub(r'^\s*\d*\s*For internal use of IA&AD\s*CHAPTER \d+.*?\s*', '', raw_text, flags=re.DOTALL)
raw_text = re.sub(r'\n\s*\d+\s*Refer Headquarters.*?\n', '\n', raw_text)
raw_text = re.sub(r'\n\s*\d+\s*Ministry of Railways.*?\n', '\n', raw_text)
raw_text = re.sub(r'\n\s*\d+\s*Representation purpose only.*?scale\s*\n', '\n', raw_text)

valid_matches = []
last_pos = 0

for h in sorted_headings:
    num_part = valid_headings[h]
    # We look for \bNUM\b followed by text
    # Or just fuzzy match the string if it's Chapter 1 where we had missing
    
    pattern = r'(?m)(?:^|\s)(' + re.escape(num_part) + r'(?:\.)?)\s+([A-Z].{3,80})'
    
    # Special manual overrides:
    if h == "3. Organizational Set Up":
        pattern = r'(?i)(Organizational\s*set\s*up)'
    elif h == "3.3 All India Railway Map With Jurisdiction & Headquarters Only":
        pattern = r'(?i)(All\s*India\s*Railway\s*Map)'
        
    m = re.search(pattern, raw_text[last_pos:])
    if m:
        match_pos = last_pos + m.start(1)
        valid_matches.append((match_pos, h))
        last_pos = match_pos + 1
    else:
        m2 = re.search(pattern, raw_text)
        if m2:
            valid_matches.append((m2.start(1), h))
        else:
            print(f"  [WARN] Heading not found in raw text: {h}")

valid_matches.sort(key=lambda x: x[0])

# Filter duplicates
unique_matches = []
seen_headings = set()
for start_pos, h in valid_matches:
    if h not in seen_headings:
        unique_matches.append((start_pos, h))
        seen_headings.add(h)

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

# Load Chapter 1 chunks we already perfectly extracted!
ch1_headings = set()
try:
    with open('ch1_extracted.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            c = json.loads(line)
            if c["heading"] == "3.2 List Of Indian Railway Zones, Their Headquarters And Divisions":
                c["has_table"] = True
                c["table_html"] = tables_map.get(c["heading"], {})
            chunks.append(c)
            ch1_headings.add(c["heading"])
except FileNotFoundError:
    pass

for i in range(len(unique_matches)):
    start_pos, proper_heading = unique_matches[i]
    
    # Skip chapter 1 headings since we loaded them perfectly
    if proper_heading in ch1_headings:
        continue
        
    end_pos = unique_matches[i+1][0] if i + 1 < len(unique_matches) else len(raw_text)
    
    line_end = raw_text.find('\n', start_pos)
    if line_end == -1 or line_end > end_pos:
        line_end = start_pos
        
    text = raw_text[line_end:end_pos].strip()
    
    if 'Map' in proper_heading or 'Representation purpose only' in text:
        text = ' '
        
    ch_num = proper_heading.split('.')[0]
    
    has_table = False
    table_html = {}
    if proper_heading in tables_map:
        has_table = True
        table_html = tables_map[proper_heading]
        
    chunks.append({
        "DOC_NAME": "RAM 2022 Sixth Edition",
        "doc_id": "RAM-9A7560D8FA",
        "chapter": ch_num,
        "title": CHAPTER_TITLE_MAP.get(ch_num, f"Chapter {ch_num}"),
        "heading": proper_heading,
        "text": text,
        "page.no": "()", 
        "has_table": has_table,
        "table_html": table_html
    })

print(f"Extracted {len(chunks)} chunks total.")

with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c) + '\n')
