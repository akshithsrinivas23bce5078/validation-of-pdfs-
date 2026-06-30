import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

corrected = 0
failed = []

for c in chunks:
    text = c['text']
    
    # We want to match the true heading at the beginning of the text.
    pattern = r'^\s*(?:Para\s*\.?\s*)?(\d+)[\.\)]?\s*([A-Z0-9\s\.\-\/\(\)&_,]{3,200}?)(?::|:-|\n|\s+(?=[A-Z][a-z])|\s+(?=[a-z])|\s+(?=\d+[\.\)]))'
    
    m = re.search(pattern, text)
    if m:
        end_pos = m.end()
        heading_text = m.group(2).strip()
        para_num = m.group(1)
        
        # Verify it's actually uppercase
        alpha_chars = [char for char in heading_text if char.isalpha()]
        upper_chars = [char for char in alpha_chars if char.isupper()]
        
        if len(alpha_chars) == 0 or len(upper_chars) / len(alpha_chars) >= 0.8:
            # We found the true heading!
            true_heading = f"Para {para_num} - {heading_text}"
            c['heading'] = true_heading
            
            # Now strip it from the text
            remaining = text[end_pos:]
            strip_match = re.match(r'^[\s:;\-.,/()]*', remaining)
            if strip_match:
                end_pos += strip_match.end()
            
            c['text'] = text[end_pos:].strip()
            corrected += 1
            continue

    # Fallback
    heading_str = c.get('heading', '')
    if '-' in heading_str:
        title_part = heading_str.split('-', 1)[1].strip()
        if title_part:
            match_title = re.search(re.escape(title_part), text[:150], re.IGNORECASE)
            if match_title:
                end_pos = match_title.end()
                remaining = text[end_pos:]
                strip_match = re.match(r'^[\s:;\-.,/()]*', remaining)
                if strip_match:
                    end_pos += strip_match.end()
                c['text'] = text[end_pos:].strip()
                
                # We ALSO strip the para number if it's there
                c['text'] = re.sub(r'^\s*\d+[\.\)]\s*', '', c['text']).strip()
                corrected += 1
                continue
                
    # If even fallback fails, just strip the para number from the start
    c['text'] = re.sub(r'^\s*\d+[\.\)]\s*', '', c['text']).strip()
    failed.append(c['heading'])

print(f"Corrected {corrected} out of {len(chunks)} chunks.")
if failed:
    print(f"Failed to extract true heading for {len(failed)} chunks.")
    
# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
