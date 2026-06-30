import json
import re

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Load the inline paras identified by find_inline.py
with open("inline_paras.json", "r", encoding="utf-8") as f:
    inline_paras = json.load(f)

fixed_count = 0

for c in chunks:
    h = c.get('heading', '').strip()
    t = c.get('text', '').strip()
    
    if not h or h == "null" or h == " ":
        continue
        
    # Get the paragraph number if any
    m = re.match(r'^(\d{1,3})\.', h)
    para_num = m.group(1) if m else None
    
    # Condition 1: Inline heading (found from PDF)
    is_inline = para_num in inline_paras
    
    # Condition 2: Split sentence (heading is long or ends in lower case)
    is_split = len(h.split()) > 10 or bool(re.search(r'[a-z]$', h))
    
    # Condition 3: Missing bold in PDF (user mentioned "doesnt start with bold")
    # To be safe, let's just use the two objective conditions.
    
    if is_inline or is_split:
        if is_inline and not is_split:
            # Reconstruct the em-dash
            if not h.endswith("."):
                h += "."
            new_text = f"{h}\u2014 {t}" if t else f"{h}\u2014"
        else:
            # Reconstruct the space
            new_text = f"{h} {t}" if t else h
            
        c['heading'] = " "
        c['text'] = new_text
        fixed_count += 1

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Fixed {fixed_count} chunks with inline or split headings.")
