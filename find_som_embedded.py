import json
import re

jsonl_path = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl"

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# We are looking for something like "634 A. Text.—" anywhere in the text
heading_pattern = re.compile(r'(?:^|\s+)(\d+(?:\s+[A-Za-z])?(?:\.\d+)*\.[^\n]{5,150}?(?:.—|\.-|\.\s*—|\.))(?=\s+[A-Z\(]|$)')

found_issues = []

for idx, c in enumerate(chunks):
    text = c.get('text', '')
    curr_heading = c.get('heading', '')
    
    # We find all matches in the text
    matches = list(heading_pattern.finditer(text))
    if matches:
        # Check if the match is essentially the same as current heading (already handled)
        # But wait, we stripped current headings from the start of text earlier, so any match here is likely a missed heading!
        
        for m in matches:
            found_heading = m.group(1).strip()
            
            # If the found heading is just a reference, e.g., "See para 12." or "under rule 5.", we skip
            if re.search(r'^(?:See|under|vide|in)\s+', found_heading, re.IGNORECASE):
                continue
            # Usually starts with digit
            if not re.match(r'^\d', found_heading):
                continue
            
            # If the found heading is very similar to the current heading, skip
            if found_heading in curr_heading or curr_heading in found_heading:
                continue
                
            # If it's just a number like "1." without any text, skip it (could be a list item)
            if re.match(r'^\d+\.$', found_heading):
                continue
            
            # Require at least some uppercase letter in the heading
            if not re.search(r'[A-Z]', found_heading):
                continue

            found_issues.append({
                'chunk_idx': idx,
                'curr_heading': curr_heading,
                'found_heading': found_heading,
                'context': text[max(0, m.start()-20):min(len(text), m.end()+50)]
            })

print(f"Found {len(found_issues)} potential embedded headings.")
for issue in found_issues[:20]:
    print(f"\nChunk {issue['chunk_idx']} (Heading: {issue['curr_heading']})")
    print(f"Found embedded: {issue['found_heading']}")
    print(f"Context: {issue['context']}")

