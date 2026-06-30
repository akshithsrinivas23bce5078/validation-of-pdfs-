"""
extract_sequential.py
Reads the PDF text sequentially. Keeps track of the current Chapter.
Extracts headings sequentially and assigns them to the correct Chapter.
"""
import json
import PyPDF2
import re
import os

print("Loading TOC...")
chapter_aware_toc = json.load(open('chapter_aware_toc.json', encoding='utf-8'))


print("Extracting tables map...")
tables_map = {}
try:
    with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            c = json.loads(line)
            if c.get('has_table'):
                tables_map[c['heading']] = c['table_html']
except FileNotFoundError:
    pass

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
# Remove page footers / headers
raw_text = re.sub(r'\b\d{1,3}\s+Railway Audit Mana?ual?\b', ' ', raw_text, flags=re.MULTILINE)

# Build a master regex for all valid numeric headings:
# E.g. ^(1\.|1\.1|2\.|2\.1)\s+([A-Z].{3,80})$
# But wait, we want to find any `NUMBER. Heading` format where NUMBER matches a valid heading.
# Let's search for any pattern like: `(?m)^(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Z].{3,80})$`
# And then we check if it is a valid heading according to our valid_headings dict.

print("Finding all headings and chapter markers sequentially...")

# 1. Find all chapter markers
chapters = []
for m in re.finditer(r'(?i)(?m)^\s*CHAPTER\s+(\d+)\s+[-]\s*(.*)$', raw_text):
    chapters.append((m.start(), m.group(1).strip()))

# Fallback: if 'CHAPTER 3' doesn't have a dash
for m in re.finditer(r'(?i)(?m)^\s*CHAPTER\s+(\d+)(?:\s+.*)?$', raw_text):
    # Only add if we don't already have it close by
    pos = m.start()
    ch = m.group(1).strip()
    if not any(abs(c[0] - pos) < 50 for c in chapters):
        chapters.append((pos, ch))

chapters.sort(key=lambda x: x[0])
print(f"Found {len(chapters)} chapter markers:")
for pos, ch in chapters:
    print(f"  Pos: {pos}, Chapter: {ch}")

# 2. Find all potential headings
matches = []
# Match 1. Heading or 1.1 Heading at the start of a line
# Must have at least 1 letter, and shouldn't be "For internal use"
for m in re.finditer(r'(?m)^(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Za-z][^\n]{3,150})$', raw_text):
    pos = m.start()
    num = m.group(1)
    text_content = m.group(2).strip()
    
    # Filter out page footers and headers
    if "internal use of" in text_content or "Railway Audit" in text_content:
        continue
    if "Table of Content" in text_content.title():
        continue
    # Filter out list items that are just long sentences
    if text_content.endswith('.') or len(text_content.split()) > 20:
        continue
    
    # Normalize to title case
    if text_content == text_content.upper() and len(text_content) > 3:
        text_content = text_content.title()
    # Remove trailing footnotes
    text_content = re.sub(r'\d+$', '', text_content).strip()
    full_heading = f"{num} {text_content}"
    
    # Exclude common stop words from capitalization check
    words = text_content.split()
    if not words:
        continue
        
    stop_words = {'and', 'of', 'the', 'for', 'in', 'on', 'to', 'with', 'at', 'by', 'from', 'about', 'under', 'etc.', 'or', 'a', 'an'}
    sig_words = [w for w in words if w.lower() not in stop_words and re.match(r'[A-Za-z]', w)]
    if not sig_words:
        continue
        
    capitalized_words = sum(1 for w in sig_words if w[0].isupper())
    
    # A heading should have at least 75% of its significant words capitalized
    if capitalized_words / len(sig_words) >= 0.75:
        matches.append((pos, full_heading))

# Add special manual overrides that don't match the standard regex
for m in re.finditer(r'(?i)(Organizational\s*set\s*up)', raw_text):
    matches.append((m.start(), "3. Organizational Set Up"))
for m in re.finditer(r'(?i)(All\s*India\s*Railway\s*Map)', raw_text):
    matches.append((m.start(), "3.3 All India Railway Map With Jurisdiction & Headquarters Only"))

matches.sort(key=lambda x: x[0])

# Deduplicate matches
unique_matches = []
seen_pos = set()
for pos, h in matches:
    # avoid duplicates very close to each other (e.g. within 10 chars)
    if not any(abs(p - pos) < 10 for p in seen_pos):
        unique_matches.append((pos, h))
        seen_pos.add(pos)

print(f"Found {len(unique_matches)} headings.")

# 3. Assign each heading to a chapter based on its position relative to chapter markers
# Dynamically find chapter boundaries in the raw text
chapter_positions = []
for i in range(1, 23):
    pattern = re.compile(rf'(?im)^CHAPTER\s+{i}\b')
    match = pattern.search(raw_text)
    if match:
        chapter_positions.append((match.start(), str(i)))
    else:
        pattern = re.compile(rf'(?i)CHAPTER\s+{i}\b')
        match = pattern.search(raw_text)
        if match:
            chapter_positions.append((match.start(), str(i)))

chapters = sorted(chapter_positions, key=lambda x: x[0])

filtered_matches = []
for pos, h in unique_matches:
    ch_num = "1"
    for chap_pos, chap in chapters:
        if pos > chap_pos:
            ch_num = chap
            
    num_only = h.split()[0].rstrip('.')
    key = f"{ch_num}_{num_only}"
    if key in chapter_aware_toc:
        filtered_matches.append((pos, chapter_aware_toc[key]))
        
unique_matches = filtered_matches
print(f"Filtered down to {len(unique_matches)} valid headings based on TOC.")


# Sort by position
chapters = sorted(chapter_positions, key=lambda x: x[0])
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
    
    # Determine chapter
    ch_num = "1"
    for chap_pos, chap in chapters:
        if start_pos > chap_pos:
            ch_num = chap
            
    if ch_num == "1":
        continue # handled by ch1_extracted.jsonl
        
    end_pos = unique_matches[i+1][0] if i + 1 < len(unique_matches) else len(raw_text)
    
    line_end = raw_text.find('\n', start_pos)
    if line_end == -1 or line_end > end_pos:
        line_end = start_pos
        
    text = raw_text[line_end:end_pos].strip()
    # remove any extra headings
    text = re.sub(r'(?m)^(\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Z].{3,80})$', '', text)
    
    if 'Map' in proper_heading or 'Representation purpose only' in text:
        text = ' '
        
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
        "text": text.strip(),
        "page.no": "()", 
        "has_table": has_table,
        "table_html": table_html
    })

print(f"Extracted {len(chunks)} chunks total.")

OUTPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_new.jsonl'
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
        
# Merge consecutive chunks with the same chapter AND same heading
merged = []
for c in chunks:
    if (merged and 
        merged[-1]['chapter'] == c['chapter'] and 
        merged[-1]['heading'] == c['heading']):
        existing_text = merged[-1]['text'].strip()
        new_text = c['text'].strip()
        if existing_text and new_text and new_text != ' ':
            merged[-1]['text'] = existing_text + '\n' + new_text
        elif new_text != ' ':
            merged[-1]['text'] = existing_text or new_text
    else:
        merged.append(c)

with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'w', encoding='utf-8') as f:
    for c in merged:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Merged to {len(merged)} chunks.")

# Validation
print("\nPer-chapter chunk counts:")
for ch in sorted(set(c['chapter'] for c in merged), key=int):
    count = sum(1 for c in merged if c['chapter'] == ch)
    print(f"  Chapter {ch:>2}: {count:>4} chunks")
