import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0

for c in chunks:
    text = c['text']
    
    # We want to match:
    # 1. Optional spaces, Para, Para number
    # 2. Uppercase heading text (up to 200 chars)
    # 3. Punctuation mark (:, -, ., \n)
    # 4. Must NOT be followed immediately by a lowercase letter without space/newline break
    
    pattern = r'^\s*(?:Para\s*\.?\s*)?(?:\d+[\.\-\)]\s*)?([A-Z0-9\s\.\-\/\(\)&_]{3,200}?)(?::|-|\.|:-|\n)(?!\s*[a-z])'
    
    match = re.search(pattern, text)
    if match:
        end_pos = match.end()
        # Ensure we didn't match something crazy long
        if end_pos <= 250:
            c['text'] = text[end_pos:].lstrip()
            removed_count += 1
    else:
        # Some headings might not have a clear trailing punctuation.
        # Fallback: exact match of the uppercase heading from the PDF extraction
        pass

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Regex heading removal applied to {removed_count} chunks.")
