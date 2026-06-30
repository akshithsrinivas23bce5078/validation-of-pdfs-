import json
import re
import copy

toc_path = r"C:\Users\Akshith Srinivas\chunk-validator-one\ram_toc_from_log.txt"
with open(toc_path, 'r', encoding='utf-8') as f:
    toc_lines = [line.strip() for line in f if line.strip()]

# Clean up TOC lines and create regex patterns
toc_patterns = []
for line in toc_lines:
    # Match patterns that start with numbers like "2.1.1 "
    m = re.match(r'^(\d+(?:\.\d+)*)\s+(.*)', line)
    if m:
        num = m.group(1)
        title = m.group(2)
        # remove page numbers at the end like " .. 14"
        title = re.sub(r'\.{2,}\s*\d+$', '', title).strip()
        
        # Create a regex pattern that matches the number and the first few words of the title
        words = [w for w in re.split(r'\W+', title) if len(w) > 0]
        if len(words) > 5:
            words = words[:5] # use first 5 words to avoid line break weirdness
            
        pattern_str = r'(?:^|\n)\s*(' + re.escape(num) + r'\s+' + r'\s*'.join(re.escape(w) for w in words) + r'.*?)\s*\n'
        toc_patterns.append((num, re.compile(pattern_str, re.IGNORECASE)))

input_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl"
output_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl"

with open(input_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

new_chunks = []

# To avoid matching the same pattern multiple times or incorrectly,
# we can just use a generic regex for numbered headings that matches standard numbering formats
# Generic regex is actually much more reliable because the TOC might have slight differences
generic_pattern = re.compile(r'(?:^|\n)(\d+\.\d+(?:\.\d+)*\s+[A-Z][^\n]{3,150}?)\s*\n')

for chunk in chunks:
    text = chunk.get("text", "")
    
    matches = list(generic_pattern.finditer(text))
    
    if not matches:
        new_chunks.append(chunk)
        continue
        
    # filter matches to only those whose numbers exist in TOC
    valid_matches = []
    for m in matches:
        heading_candidate = m.group(1).strip()
        num_match = re.match(r'^(\d+(?:\.\d+)*)', heading_candidate)
        if num_match:
            num = num_match.group(1)
            # check if this num is in TOC or looks very much like a heading (e.g. 3 parts)
            # Actually, standardizing on \d+\.\d+\.\d+ is very safe for RAM
            if num.count('.') >= 1:
                valid_matches.append(m)
                
    if not valid_matches:
        new_chunks.append(chunk)
        continue
        
    first_match_start = valid_matches[0].start()
    
    current_chunk = copy.deepcopy(chunk)
    prefix_text = text[:first_match_start].strip()
    current_chunk["text"] = prefix_text
    new_chunks.append(current_chunk)
    
    for i, match in enumerate(valid_matches):
        heading_text = match.group(1).strip()
        # If there's a newline within the heading? The regex `[^\n]` prevents it.
        # But wait, earlier we saw "2.1.4 ... \n Principal Directors". It's fine if the rest of the heading falls into the text.
        start_pos = match.end()
        end_pos = valid_matches[i+1].start() if i + 1 < len(valid_matches) else len(text)
        
        body_text = text[start_pos:end_pos].strip()
        
        new_c = copy.deepcopy(chunk)
        new_c["heading"] = heading_text
        new_c["text"] = body_text
        if "table_html" in new_c and i >= 0:
             # Just a heuristic to not duplicate tables
             new_c["has_table"] = False
             new_c["table_html"] = {}
             
        new_chunks.append(new_c)

print(f"Original chunks: {len(chunks)}")
print(f"New chunks: {len(new_chunks)}")

# Write to a temporary file to verify
with open(input_file.replace('.jsonl', '_fixed.jsonl'), 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c) + "\n")
