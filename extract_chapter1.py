import re
import json

def norm(s):
    return re.sub(r'[^A-Z0-9]+', '', s.upper())

user_headings = [
    "1. Background", "1.1 Making Of Ram", "1.2 Structure Of Ram", "1.3 Features Of Ram",
    "1.4 New Initiatives", "2. Departmental Regulations", 
    "2.1 Constitution Of The Railway Audit Branch", "3. Organizational Set Up",
    "3.1 Composition Of Railway Board", "3.2 List Of Indian Railway Zones, Their Headquarters And Divisions",
    "3.3 All India Railway Map With Jurisdiction & Headquarters Only", 
    "3.4 Broad Distribution Of Work Among Board Members", "4. General Duties Of The Railway Audit Branch",
    "4.1 Functions Of Cag", "4.2 Functions Of Railway Audit Wing", "4.3 Duties Of Directors General Of Audit/Principal Directors Of Audit",
    "5. Types Of Audit", "5.1 Financial Audit", "5.2 Compliance Audit", "5.3 Performance Audit",
    "6. Communication From Audit", "6.1 Specific Reports", "6.2 Audit Notes", "6.3 Inspection Reports",
    "7. Disposal Of Audit/Inspection Reports", "7.1 Special Letters And Notes Or Objections Or Factual Statement"
]

norm_headings = {norm(h): h for h in user_headings}
# Special case for 3. Organizational Set Up which is "3. ORGANIZATIONAL STRUCTURE OF MINISTRY OF RAILWAYS" in text
norm_headings[norm("3. ORGANIZATIONAL STRUCTURE OF MINISTRY OF RAILWAYS")] = "3. Organizational Set Up"

with open('ch1_raw.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Clean up
raw_text = re.sub(r'(?m)^Railway Audit Manual\s*$\n^\s*\d+\s*$\n^For internal use of IA&AD\s*$', '', raw_text)
raw_text = re.sub(r'(?m)^Chapter 1.*?Manual\s*$\n^\s*\d+\s*$\n^For internal use of IA&AD\s*$', '', raw_text)
raw_text = re.sub(r'^\s*\d*\s*For internal use of IA&AD\s*CHAPTER 1.*?MANUAL\s*', '', raw_text, flags=re.DOTALL)
raw_text = re.sub(r'\n\s*\d+\s*Refer Headquarters.*?\n', '\n', raw_text)
raw_text = re.sub(r'\n\s*\d+\s*Ministry of Railways.*?\n', '\n', raw_text)
raw_text = re.sub(r'\n\s*\d+\s*Representation purpose only.*?scale\s*\n', '\n', raw_text)

# We will match ANY line starting with a number, then normalize and check if it's in norm_headings
pattern = r'(?m)^\s*(\d+(?:\.\d+)*)\.?\s+(.+?)(?:\n|$)'
matches = list(re.finditer(pattern, raw_text))

valid_matches = []
for m in matches:
    num = m.group(1).strip()
    title = m.group(2).strip()
    
    # Try the full string
    test_norm = norm(f"{num} {title}")
    
    # Fuzzy match: does test_norm START with a valid heading norm?
    # Because sometimes title has extra text like "6.1 Specific Reports - related to more important..."
    best_match = None
    for k, v in norm_headings.items():
        if test_norm.startswith(k) or k.startswith(test_norm):
            best_match = v
            break
            
    if best_match:
        valid_matches.append((m.start(), best_match))

# Add "Organizational set up" fallback
if not any(v == "3. Organizational Set Up" for _, v in valid_matches):
    m = re.search(r'(?i)Organizational set up', raw_text)
    if m:
        valid_matches.append((m.start(), "3. Organizational Set Up"))
if not any(v == "3.3 All India Railway Map With Jurisdiction & Headquarters Only" for _, v in valid_matches):
    m = re.search(r'(?i)All India\s*Railway Map', raw_text)
    if m:
        valid_matches.append((m.start(), "3.3 All India Railway Map With Jurisdiction & Headquarters Only"))

valid_matches.sort(key=lambda x: x[0])

# Filter duplicates
unique_matches = []
seen = set()
for start_pos, h in valid_matches:
    if h not in seen:
        unique_matches.append((start_pos, h))
        seen.add(h)

chunks = []
for i in range(len(unique_matches)):
    start_pos, proper_heading = unique_matches[i]
    end_pos = unique_matches[i+1][0] if i + 1 < len(unique_matches) else len(raw_text)
    
    # Text starts after the heading line ends
    line_end = raw_text.find('\n', start_pos)
    if line_end == -1 or line_end > end_pos:
        line_end = start_pos
        
    text = raw_text[line_end:end_pos].strip()
    
    if 'Map' in proper_heading or 'Representation purpose only' in text:
        text = ' '
        
    chunks.append({
        "DOC_NAME": "RAM 2022 Sixth Edition",
        "doc_id": "RAM-9A7560D8FA",
        "chapter": "1",
        "title": "Introduction to Railway Audit Manual",
        "heading": proper_heading,
        "text": text,
        "page.no": "(31-46)", 
        "has_table": False,
        "table_html": {}
    })

print(f"Extracted {len(chunks)} chunks.")
for c in chunks:
    print(c['heading'])

with open('ch1_extracted.jsonl', 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c) + '\n')
