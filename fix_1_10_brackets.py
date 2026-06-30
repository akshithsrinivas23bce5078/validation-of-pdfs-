import json
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 1_2.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c['heading'].startswith("1.10"):
        # We will just completely rewrite the text property for the heading to be perfectly clean.
        # The heading should be: "1.10 RELATIONSHIP BETWEEN PART-A (ENGINEERING), PART-B (OPERATION AND MAINTENANCE), AND PART-C (MANAGEMENT) OF MANUAL"
        heading_full = "1.10 RELATIONSHIP BETWEEN PART-A (ENGINEERING), PART-B (OPERATION AND MAINTENANCE), AND PART-C (MANAGEMENT) OF MANUAL"
        
        # The original text started with "MAINTENANCE), AND PART-C (MANAGEMENT) OF MANUAL The present manual..."
        # Or something similar. Let's just find "The present manual" and keep everything after.
        text = c['text']
        match = re.search(r'(The present manual.*)', text, re.DOTALL)
        if match:
            clean_text = heading_full + "\n" + match.group(1)
            c['text'] = clean_text

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + '\n')

print("Fixed formatting in 1.10 chunk definitively.")
