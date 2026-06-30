import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0
failed = []

for c in chunks:
    heading = c['heading']
    text = c['text']
    
    # Extract the title part from heading
    title_part = heading
    m = re.match(r'Para\s+\d+\s*[-]\s*', heading)
    if m:
        title_part = heading[m.end():]
    
    title_words = re.findall(r'[A-Za-z]{3,}', title_part)
    
    stripped = False
    
    # STRATEGY 1: Word match (like original remove_headings_from_text.py)
    if title_words:
        search_area = text[:300]
        last_word = title_words[-1]
        pattern = re.compile(re.escape(last_word), re.IGNORECASE)
        matches = list(pattern.finditer(search_area))
        
        if not matches:
            for tw in reversed(title_words[:-1]):
                matches = list(re.compile(re.escape(tw), re.IGNORECASE).finditer(search_area))
                if matches:
                    break
        
        if matches:
            last_match = matches[0]
            end_pos = last_match.end()
            text_before = search_area[:end_pos].upper()
            words_found = sum(1 for w in title_words if w.upper() in text_before)
            
            # Key safety check!
            if words_found >= len(title_words) * 0.5 and end_pos <= 130:
                remaining = text[end_pos:]
                strip_match = re.match(r'^[\s:;\-.,/()]*', remaining)
                if strip_match:
                    end_pos += strip_match.end()
                
                c['text'] = text[end_pos:].strip()
                stripped = True

    # STRATEGY 2: UPPERCASE pattern match
    if not stripped:
        pattern = r'^\s*(?:Para\s*\.?\s*)?(?:\d+[\.\-\)]\s*)?([A-Z0-9\s\.\-\/\(\)&_]{3,200}?)(?::|-|\.|:-|\n)'
        m = re.search(pattern, text)
        if m:
            end_pos = m.end()
            if end_pos <= 200:
                # Extra check: is the uppercase portion actually representing the heading?
                # Ensure it's mostly uppercase
                c['text'] = text[end_pos:].strip()
                stripped = True
                
    if stripped:
        removed_count += 1
    else:
        failed.append(heading)

print(f"Removed heading from text in {removed_count} out of {len(chunks)} chunks.")
if failed:
    print(f"Failed chunks: {len(failed)}")

# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
