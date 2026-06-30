import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0
failed = []

for c in chunks:
    text = c['text']
    
    # We want to match:
    # 1. Optional spaces, Para, Para number
    # 2. Uppercase heading text (up to 200 chars)
    # 3. Punctuation mark (:, -, ., \n)
    
    pattern = r'^\s*(?:Para\s*\.?\s*)?(?:\d+[\.\-\)]\s*)?([A-Z0-9\s\.\-\/\(\)&_]{3,200}?)(?::|-|\.|:-|\n)'
    
    m = re.search(pattern, text)
    if m:
        end_pos = m.end()
        # Verify that what we matched is actually mostly uppercase
        matched_str = text[:end_pos]
        alpha_chars = [char for char in matched_str if char.isalpha()]
        upper_chars = [char for char in alpha_chars if char.isupper()]
        
        # If at least 80% of alphabetic characters in the match are uppercase, it's a heading
        if len(alpha_chars) == 0 or len(upper_chars) / len(alpha_chars) >= 0.8:
            if end_pos <= 200:
                # Strip leading whitespace/punctuation from the remaining text
                remaining = text[end_pos:]
                strip_match = re.match(r'^[\s:;\-.,/()]*', remaining)
                if strip_match:
                    end_pos += strip_match.end()
                
                c['text'] = text[end_pos:].strip()
                removed_count += 1
                continue

    failed.append(c['heading'])

print(f"Removed heading from text in {removed_count} out of {len(chunks)} chunks.")
if failed:
    print(f"Failed to strip {len(failed)} chunks.")

# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
