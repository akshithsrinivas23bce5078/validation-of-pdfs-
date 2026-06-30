import json
import re
import os

raw_text = open('all_raw.txt', encoding='utf-8').read()
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
current_search_pos = 20000 # Skip the main TOC at the beginning

for ch_num in range(1, 23):
    ch_num = str(ch_num)
    if ch_num not in required:
        continue
        
    req_list = required[ch_num]
    positions = []
    
    for req in req_list:
        key = f"{ch_num}_{req}"
        title = toc.get(key, req)
        
        # Build a robust regex
        words = title.split()
        if len(words) > 1:
            # Match number optionally with dot, then up to 4 words
            # Remove any trailing dots from words just in case
            sig_words = [re.escape(w.rstrip('.')) for w in words[1:5]]
            # Some words might have special chars inside in the text, but usually first few words are safe
            regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+' + r'\s+'.join(sig_words)
        else:
            regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+([A-Za-z].*)'
            
        pattern = re.compile(regex)
        match = pattern.search(raw_text, current_search_pos)
        
        if not match:
            # Fallback: Just search for the number and at least the first word
            if len(words) > 1:
                sig_words = [re.escape(words[1].rstrip('.'))]
                regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+' + r'\s+'.join(sig_words)
                pattern = re.compile(regex)
                match = pattern.search(raw_text, current_search_pos)
                
            if not match:
                # Ultimate fallback: Just the number at the start of a line
                regex = r'(?im)^\s*' + re.escape(req) + r'(?:\.)?\s+[A-Za-z]'
                pattern = re.compile(regex)
                match = pattern.search(raw_text, current_search_pos)
                
        if match:
            # We must be careful not to jump too far ahead!
            # If the match is more than 50,000 chars away, it might be a false positive in another chapter!
            if match.start() - current_search_pos > 100000:
                print(f"Warning: {key} match is suspiciously far ({match.start() - current_search_pos} chars). Accepting anyway.")
                
            heading_full = title
            pos = match.start()
            positions.append((pos, heading_full))
            current_search_pos = pos + 1
        else:
            print(f"Error: Could not find '{req}' in Chapter {ch_num}")
            
    # Now extract the text between these positions
    for i in range(len(positions)):
        pos, heading = positions[i]
        next_pos = positions[i+1][0] if i + 1 < len(positions) else len(raw_text) # Temporary next_pos
        
        # If this is the last subdivision of the chapter, we need to end it somewhere.
        # Let's cap the last subdivision at 50,000 characters or the next chapter start.
        if i + 1 == len(positions):
            # Look for the start of the next chapter or next heading
            next_ch = str(int(ch_num) + 1)
            # Find next chapter roughly
            ch_match = re.search(rf'(?im)^CHAPTER\s+{next_ch}\b', raw_text[pos:])
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

with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
print("Saved exact chunks.")
