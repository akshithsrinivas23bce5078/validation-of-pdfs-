import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0
failed = []

for c in chunks:
    text = c['text']
    
    # We strictly follow the user's formats:
    # number.heading
    # number heading
    # number) heading
    # Optional "Para " before the number.
    
    # The heading text is typically UPPERCASE.
    # We match:
    # 1. ^\s*
    # 2. (?:Para\s*\.?\s*)? -> Optional "Para "
    # 3. (\d+) -> The number
    # 4. [\.\)]?\s* -> Optional dot or closing parenthesis and spaces (matches "number.", "number)", or "number ")
    # 5. ([A-Z0-9\s\.\-\/\(\)&_]{3,150}?) -> The uppercase heading text
    # 6. (?::|-|\.|:-|\n) -> End of heading punctuation or newline
    
    pattern = r'^\s*(?:Para\s*\.?\s*)?(\d+)[\.\)]?\s*([A-Z0-9\s\.\-\/\(\)&_]{3,150}?)(?::|-|\.|:-|\n)'
    
    m = re.search(pattern, text)
    if m:
        end_pos = m.end()
        
        # Additional safety: Ensure the matched heading part is mostly uppercase
        heading_text = m.group(2)
        alpha_chars = [char for char in heading_text if char.isalpha()]
        upper_chars = [char for char in alpha_chars if char.isupper()]
        
        # If it's mostly uppercase (>= 80%)
        if len(alpha_chars) == 0 or len(upper_chars) / len(alpha_chars) >= 0.8:
            if end_pos <= 200:
                # Strip trailing whitespace and punctuation from the remaining text
                remaining = text[end_pos:]
                strip_match = re.match(r'^[\s:;\-.,/()]*', remaining)
                if strip_match:
                    end_pos += strip_match.end()
                
                c['text'] = text[end_pos:].strip()
                removed_count += 1
                continue
    
    # Fallback for exact string match from the 'heading' field
    # E.g. "Para 114 - Transparency In Tender Rules 2000"
    heading_str = c.get('heading', '')
    if '-' in heading_str:
        title_part = heading_str.split('-', 1)[1].strip()
        # Find this title case-insensitively in the first 150 chars
        if title_part:
            match_title = re.search(re.escape(title_part), text[:150], re.IGNORECASE)
            if match_title:
                end_pos = match_title.end()
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
