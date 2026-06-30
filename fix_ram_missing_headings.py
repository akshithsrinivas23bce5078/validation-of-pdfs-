import json
import re
import copy

input_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl"
output_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl"

with open(input_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

new_chunks = []

# Regex to match headings like "2.1.2 Organizational set up" at the start of a line
# Note: heading usually starts with digits, a dot, digits, (optional dot and digits), space, and text, ending with newline
heading_pattern = re.compile(r'(?:^|\n)(\d+\.\d+(?:\.\d+)*\s+[A-Z][^\n]{3,100}?)\s*\n')

for chunk in chunks:
    text = chunk.get("text", "")
    
    # We will find all matches
    # But wait, if the chunk already starts with the text, the first part might be the heading.
    # We should split the text using the pattern.
    
    # Let's find all headings in the text
    matches = list(heading_pattern.finditer(text))
    
    if not matches:
        new_chunks.append(chunk)
        continue
        
    # We found internal headings! We need to split the chunk.
    # If the first match is not at the very beginning, the text before the first match belongs to the original chunk
    
    last_idx = 0
    current_chunk = copy.deepcopy(chunk)
    
    # If the text before the first match is non-empty, we keep the original chunk for that text
    first_match_start = matches[0].start()
    if first_match_start > 0:
        prefix_text = text[:first_match_start].strip()
        if prefix_text:
            current_chunk["text"] = prefix_text
            new_chunks.append(current_chunk)
        else:
            # prefix is just whitespace, ignore
            pass
    
    # Now for each match, create a new chunk
    for i, match in enumerate(matches):
        heading_text = match.group(1).strip()
        start_pos = match.end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        body_text = text[start_pos:end_pos].strip()
        
        new_c = copy.deepcopy(chunk)
        new_c["heading"] = heading_text
        new_c["text"] = body_text
        # We should clear table_html if it was already used? Or maybe not, but it's safer to clear it if it doesn't apply.
        # For simplicity, we just keep it in the first split or where it makes sense.
        # Let's clear has_table for the split chunks if the original had a table but it's probably in only one of them.
        # Actually, let's keep it as is, or clear it for subsequent parts.
        if "table_html" in new_c and i > 0:
             # Just a heuristic: the table usually belongs to one part. If we split, we might duplicate it.
             new_c["has_table"] = False
             new_c["table_html"] = {}
             
        new_chunks.append(new_c)

print(f"Original chunks: {len(chunks)}")
print(f"New chunks: {len(new_chunks)}")

with open(output_file, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c) + "\n")
