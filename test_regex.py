import json
import fitz
import re

doc = fitz.open(r'assigned pdfs\RAM 2022 Sixth Edition.pdf')
text = '\n'.join(doc[i].get_text() for i in range(30, 200))

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

ch1_5 = [c for c in chunks if int(c['chapter']) <= 5]
not_found = 0

for c in ch1_5:
    h = re.sub(r'\s+', ' ', c['heading']).strip()
    p = r'\s+'.join(map(re.escape, h.split()))
    if not re.search(r'(?:^|\n)\s*' + p + r'\s', text, re.IGNORECASE):
        # Fallback to prefix matching
        prefix_match = re.match(r'^(\d+(?:\.\d+)*\.?)?\s*(.*)', h)
        found = False
        if prefix_match and prefix_match.group(1):
            prefix = prefix_match.group(1)
            escaped_prefix = re.escape(prefix)
            if re.search(r'(?:^|\n)\s*' + escaped_prefix + r'[.\s]+[A-Z]', text, re.IGNORECASE):
                found = True
            elif re.search(r'(?:^|\n)\s*' + escaped_prefix + r'\s', text, re.IGNORECASE):
                found = True
        
        if not found:
            not_found += 1
            print(f'Not found: {h}')

print(f'Total missing in 1-5: {not_found}/{len(ch1_5)}')
