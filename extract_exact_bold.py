import fitz
import json
import re

pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

# Map of para_num -> bold_text
bold_headings = {}

for page in pdf:
    for b in page.get_text("dict")["blocks"]:
        if b['type'] == 0:
            for l in b['lines']:
                line_text = "".join([s['text'] for s in l['spans']]).strip()
                m = re.match(r'^(\d{1,3})\.', line_text)
                if m:
                    para_num = m.group(1)
                    
                    # Accumulate bold spans
                    bold_parts = []
                    for s in l['spans']:
                        text = s['text']
                        if not text.strip():
                            bold_parts.append(text)
                            continue
                        
                        is_bold = 'bold' in s['font'].lower() or 'black' in s['font'].lower()
                        if is_bold:
                            bold_parts.append(text)
                        else:
                            break
                            
                    # Clean up
                    full_bold = "".join(bold_parts).strip()
                    # Only accept if it actually starts with the para num
                    if full_bold.startswith(para_num + "."):
                        bold_headings[para_num] = full_bold

print(f"Extracted {len(bold_headings)} exact bold headings from PDF.")
# print some to verify
for k in list(bold_headings.keys())[:10]:
    print(k, ":", bold_headings[k])

with open("exact_bold_headings.json", "w", encoding="utf-8") as f:
    json.dump(bold_headings, f, ensure_ascii=False)
