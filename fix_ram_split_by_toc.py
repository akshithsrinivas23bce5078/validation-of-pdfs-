import json
import re
import copy

toc_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\new_toc_mapping.json'
with open(toc_path, 'r', encoding='utf-8') as f:
    toc = json.load(f)

# Build a mapping from normalized regex to the canonical TOC heading
regex_to_canonical = {}
for canonical in toc.values():
    # Escape special characters, but replace spaces with \s+
    # First, split by space
    parts = canonical.split()
    if not parts:
        continue
    
    # We want to match cases where numbers might have spaces, but TOC values are usually clean.
    # E.g. "7.39 Public Private Partnership"
    # Regex: ^\s*7\.39\s+Public\s+Private\s+Partnership\s*$
    pattern_parts = [re.escape(p) for p in parts]
    pattern_str = r'^\s*' + r'\s+'.join(pattern_parts) + r'\s*$'
    regex_to_canonical[pattern_str] = canonical

# We want to find these inside the text. We can compile them all.
compiled_patterns = []
for p_str, canon in regex_to_canonical.items():
    compiled_patterns.append((re.compile(p_str, re.IGNORECASE | re.MULTILINE), canon))

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl'
with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

split_chunks = []
total_splits = 0

for chunk in chunks:
    text = chunk.get("text", "")
    
    # Find all matches of any valid heading in the text
    matches = []
    for pat, canon in compiled_patterns:
        for match in pat.finditer(text):
            matches.append((match.start(), match.end(), canon))
    
    # If no internal headings found, just append
    if not matches:
        split_chunks.append(chunk)
        continue
    
    # Sort matches by start position
    matches.sort(key=lambda x: x[0])
    
    # It's possible there are overlapping matches (very unlikely with specific headings). We filter them.
    filtered_matches = []
    last_end = -1
    for m in matches:
        if m[0] >= last_end:
            filtered_matches.append(m)
            last_end = m[1]
    
    # Split the chunk
    last_pos = 0
    current_chunk = copy.deepcopy(chunk)
    
    # The text before the first match belongs to the original chunk
    first_start = filtered_matches[0][0]
    if first_start > 0:
        prefix_text = text[:first_start].strip()
        if prefix_text:
            current_chunk["text"] = prefix_text
            split_chunks.append(current_chunk)
    
    for i, (start, end, canon) in enumerate(filtered_matches):
        next_start = filtered_matches[i+1][0] if i + 1 < len(filtered_matches) else len(text)
        body = text[end:next_start].strip()
        
        new_c = copy.deepcopy(chunk)
        new_c["heading"] = canon
        new_c["text"] = body
        # Clear table for splits? Let's just clear it to avoid duplication, or keep it if it's the only text?
        # A simple heuristic: remove table from all but the original chunk
        if "table_html" in new_c:
            new_c["has_table"] = False
            new_c["table_html"] = {}
        split_chunks.append(new_c)
        total_splits += 1

print(f"Original chunks: {len(chunks)}")
print(f"Total internal splits: {total_splits}")
print(f"New total chunks: {len(split_chunks)}")

# Write to RAM_2022_Sixth_Edition_fixed.jsonl
out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
with open(out_path, 'w', encoding='utf-8') as f:
    for c in split_chunks:
        f.write(json.dumps(c) + '\n')
