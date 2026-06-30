import fitz
import re

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU MINISTERIAL SERVICE RULES.pdf'
doc = fitz.open(pdf_path)

toc = {}
for i in range(3):
    text = doc[i].get_text()
    lines = text.split('\n')
    for j, line in enumerate(lines):
        line = line.strip()
        # Look for pattern: number followed by '.' and then some text
        match = re.match(r'^(\d+[A-Z]?)\.$', line)
        if match:
            rule_no = match.group(1)
            # the title is usually the next line or lines
            title_parts = []
            k = j + 1
            while k < len(lines):
                next_line = lines[k].strip()
                if not next_line or next_line.startswith('ANNEXURE'):
                    break
                if re.match(r'^\d+[A-Z]?\.$', next_line):
                    break
                # some lines are just '-' or page numbers
                if next_line == '-' or re.match(r'^-\s*\d+\s*-$', next_line):
                    k += 1
                    continue
                title_parts.append(next_line)
                k += 1
            if title_parts:
                toc[rule_no] = " ".join(title_parts)

print("Extracted TOC:")
for k, v in toc.items():
    print(f"Rule {k}: {v}")

import json
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\tnms_toc.json', 'w', encoding='utf-8') as f:
    json.dump(toc, f, indent=4)
