import fitz
import re

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\17. Introduction Accounting Manual Part_1 Wes_State Audit West Ben.pdf')
text = chr(10).join([page.get_text() for page in doc])

# Extract all definitions from Chapter 8
# Note: we look for numbers 1 to 125 followed by dot, then newline, then heading, then colon
matches = re.findall(r'\n(\d+)\.\n(.*?):\s', text, flags=re.DOTALL)
for m in matches[:5]:
    num, heading = m
    print(f"{num}. {heading.strip().replace(chr(10), ' ')}")

# Map them into a dict
heading_dict = {}
for m in matches:
    num, heading = m
    heading_str = heading.strip().replace(chr(10), ' ')
    heading_dict[num] = heading_str

import json
val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

corrected = 0
for c in chunks:
    if str(c['chapter']) == '8' and 'text' in c:
        m = re.match(r'^8\.(\d+)\s+(.*)', c['text'])
        if m:
            num = m.group(1)
            rest = m.group(2)
            
            if num in heading_dict:
                true_heading = heading_dict[num]
                
                # We need to remove the true_heading from `rest`
                # Since whitespace might differ, we do a case-insensitive, space-insensitive strip
                # Or just literal replace
                # True heading might be "Account"
                # rest might be "Account A formal record..."
                
                heading_pattern = re.escape(true_heading).replace(r'\ ', r'\s+')
                new_rest = re.sub('^' + heading_pattern + r'\s*', '', rest, flags=re.IGNORECASE)
                
                if new_rest != rest:
                    c['heading'] = true_heading
                    c['text'] = new_rest
                    corrected += 1

print(f"Corrected {corrected} definitions in Chapter 8")

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
