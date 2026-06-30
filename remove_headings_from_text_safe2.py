import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0

def clean_str(s):
    return re.sub(r'[\W_]+', '', s).lower()

for c in chunks:
    text = c['text']
    heading = c.get('heading', '')
    if not heading: continue
    
    # Extract the title part from heading (e.g. "Transparency In Tender Rules 2000" from "Para 114 - Transparency...")
    title_part = heading.split('-', 1)[-1].strip() if '-' in heading else heading
    title_clean = clean_str(title_part)
    
    if not title_clean: continue
    
    # We look at the first 200 characters of text
    prefix = text[:300]
    prefix_clean = clean_str(prefix)
    
    # Find the title in the cleaned prefix
    idx = prefix_clean.find(title_clean)
    
    if idx != -1:
        # We found the title! The end index in prefix_clean is:
        end_clean_idx = idx + len(title_clean)
        
        # Now map end_clean_idx back to the original text
        mapped_idx = 0
        clean_count = 0
        for i, ch in enumerate(prefix):
            if re.match(r'[\W_]', ch):
                pass
            else:
                clean_count += 1
            if clean_count == end_clean_idx:
                mapped_idx = i + 1
                break
                
        # mapped_idx is the end of the matched title.
        # Now find the end of the heading punctuation (. : \n)
        rem_text = text[mapped_idx:mapped_idx+50]
        delim_match = re.search(r'(:|:-|\.|\n)', rem_text)
        if delim_match:
            final_end = mapped_idx + delim_match.end()
        else:
            final_end = mapped_idx
            
        # Ensure we didn't match too deep (e.g. > 150 chars in mapped_idx means we might have stripped actual text)
        if mapped_idx <= 150:
            c['text'] = text[final_end:].lstrip()
            removed_count += 1
    else:
        # Fallback for slight typos like "RULES" vs "RULE"
        # We can just match the first 3 words of the title
        words = [w for w in re.findall(r'[a-z0-9]{4,}', title_part.lower()) if w not in ('the', 'and', 'for', 'with')]
        if len(words) >= 2:
            first_two = ''.join(words[:2])
            idx = prefix_clean.find(first_two)
            if idx != -1 and idx <= 50:
                end_clean_idx = idx + len(first_two)
                mapped_idx = 0
                clean_count = 0
                for i, ch in enumerate(prefix):
                    if re.match(r'[\W_]', ch) is None:
                        clean_count += 1
                    if clean_count == end_clean_idx:
                        mapped_idx = i + 1
                        break
                rem_text = text[mapped_idx:mapped_idx+100]
                delim_match = re.search(r'(:|:-|\.|\n)', rem_text)
                final_end = mapped_idx + delim_match.end() if delim_match else mapped_idx
                if final_end <= 150:
                    c['text'] = text[final_end:].lstrip()
                    removed_count += 1

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Safe heading removal applied to {removed_count} chunks.")
