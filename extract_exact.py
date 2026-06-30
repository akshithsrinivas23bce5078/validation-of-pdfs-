import json
import re
import os

raw_text = open('all_raw.txt', encoding='utf-8').read()
required = json.load(open('user_required_subdivisions.json', encoding='utf-8'))
tables = json.load(open('extracted_tables.json', encoding='utf-8'))

# Clean text for table matching
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
            
            # Simple overlap score
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

# Find chapter boundaries
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
chapter_bounds = {}
for i in range(len(chapters)):
    start = chapters[i][0]
    end = chapters[i+1][0] if i + 1 < len(chapters) else len(raw_text)
    ch_num = chapters[i][1]
    chapter_bounds[ch_num] = (start, end)

chunks = []

for ch_num in range(1, 23):
    ch_num = str(ch_num)
    if ch_num not in required or ch_num not in chapter_bounds:
        continue
        
    start_pos, end_pos = chapter_bounds[ch_num]
    ch_text = raw_text[start_pos:end_pos]
    
    req_list = required[ch_num]
    
    # We find the start of each subdivision sequentially within the chapter text
    positions = []
    current_search_pos = 0
    
    for req in req_list:
        # Regex to find exactly `req. ` or `req ` at the start of a line
        escaped_req = re.escape(req)
        pattern = re.compile(rf'(?m)^\s*{escaped_req}(?:\.)?\s+([A-Z].*)$', re.IGNORECASE)
        match = pattern.search(ch_text, current_search_pos)
        
        if not match:
            # Try a looser pattern if there are typos
            pattern = re.compile(rf'(?m)^\s*{escaped_req}(?:\.)?\s*(.*)$', re.IGNORECASE)
            match = pattern.search(ch_text, current_search_pos)
            
        if match:
            heading_title = match.group(1).strip()
            heading_full = f"{req}. {heading_title}"
            pos = match.start()
            positions.append((pos, heading_full))
            current_search_pos = pos + 1
        else:
            print(f"Warning: Could not find '{req}' in Chapter {ch_num}")
            
    # Now extract the text between these positions
    for i in range(len(positions)):
        pos, heading = positions[i]
        next_pos = positions[i+1][0] if i + 1 < len(positions) else len(ch_text)
        
        text_content = ch_text[pos:next_pos].strip()
        
        # Inject tables
        t = find_table_for_chunk(text_content)
        has_table = False
        table_html_val = {}
        if t:
            has_table = True
            table_html_val = {"html": t.get("html", "")}
            
        chunk_data = {
            "chapter": ch_num,
            "title": f"Chapter {ch_num}", # Could add actual title if needed
            "heading": heading,
            "text": text_content,
            "page.no": "()", # Can't accurately get page without complex mapping, defaulting to ()
            "has_table": has_table,
            "table_html": table_html_val
        }
        chunks.append(chunk_data)

print(f"Extracted {len(chunks)} chunks.")

with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
print("Saved exact chunks.")
