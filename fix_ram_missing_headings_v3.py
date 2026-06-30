import json
import re
import copy

input_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl"
output_file = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl"

with open(input_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# To match exactly like "2.1.4 Administrative control..." across newlines,
# let's define a pattern for the start of a numbered heading.
# A heading starts with "X.Y.Z " at the beginning of a line.
start_pattern = re.compile(r'(?:^|\n)(\d+\.\d+(?:\.\d+)*\s+)')

new_chunks = []

for chunk in chunks:
    text = chunk.get("text", "")
    
    matches = list(start_pattern.finditer(text))
    
    valid_matches = []
    for m in matches:
        num_str = m.group(1).strip()
        num = num_str.split()[0]
        # Only consider it a missing heading if it has at least one dot
        if num.count('.') >= 1:
            # check what follows the number
            following_text = text[m.end():]
            # It must start with a capital letter
            if re.match(r'^[A-Z]', following_text):
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
        num_str = match.group(1).strip()
        start_pos = match.end()
        end_pos = valid_matches[i+1].start() if i + 1 < len(valid_matches) else len(text)
        
        chunk_text_raw = text[start_pos:end_pos].strip()
        
        # We need to extract the heading text. Usually the first line or two.
        # Let's say the heading is everything up to the first double newline, or if there is no double newline, just the first line.
        # But wait, looking at chunk 3:
        # "2.1.2 Organizational set up  \nOrganization al set up of the Railway Audit  Branch:"
        # Here, the heading is the first line.
        # "2.1.4 Administrative control and jurisdiction of Director s General  of Audi t/ \nPrincipal  Directors of Audit    \nDirector s General..."
        # Here the heading is the first two lines.
        # We can extract the heading by matching lines that don't look like sentences (no punctuation at end).
        
        lines = chunk_text_raw.split('\n')
        heading_lines = []
        body_lines = []
        heading_done = False
        
        for line in lines:
            line_str = line.strip()
            if not heading_done:
                if not line_str:
                    continue # empty line, skip
                heading_lines.append(line_str)
                # If line ends with a period, colon, or we have collected enough lines, we stop.
                # Actually, "Audit t/" ends with "/", "Audit" ends with nothing.
                # Usually headings are short. Let's just say if the line ends with a sentence terminator (. ! ?) it's body text.
                # Wait, "History of Railway Audit" doesn't.
                # If the next line starts with a capital letter and the current line doesn't end with a continuing character like /, and, or etc.
                # A simpler rule: just take the first line as heading, UNLESS it ends with "of", "and", "/", "-", etc.
                if re.search(r'(of|and|/|-)$', line_str, re.IGNORECASE):
                    # continue collecting heading
                    pass
                else:
                    heading_done = True
            else:
                body_lines.append(line_str)
                
        heading_text = num_str + " " + " ".join(heading_lines)
        body_text = "\n".join(body_lines).strip()
        
        new_c = copy.deepcopy(chunk)
        new_c["heading"] = heading_text
        new_c["text"] = body_text
        if "table_html" in new_c and i >= 0:
             new_c["has_table"] = False
             new_c["table_html"] = {}
             
        new_chunks.append(new_c)

print(f"Original chunks: {len(chunks)}")
print(f"New chunks: {len(new_chunks)}")

with open(output_file, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c) + "\n")
