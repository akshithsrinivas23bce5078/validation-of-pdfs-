import fitz
import json
import re

pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

bold_paras = set()
non_bold_paras = set()

for page in pdf:
    for b in page.get_text("dict")["blocks"]:
        if b['type'] == 0:
            for l in b['lines']:
                # The first word of the first span might contain the number
                line_text = "".join([s['text'] for s in l['spans']]).strip()
                m = re.match(r'^(\d{1,3})\.', line_text)
                if m:
                    para_num = m.group(1)
                    # Check the font of the first span
                    first_span = l['spans'][0]
                    is_bold = 'bold' in first_span['font'].lower() or 'black' in first_span['font'].lower()
                    if is_bold:
                        bold_paras.add(para_num)
                    else:
                        non_bold_paras.add(para_num)

print(f"Bold paras: {len(bold_paras)}")
print(f"Non-bold paras: {len(non_bold_paras)}")

with open("para_fonts.json", "w") as f:
    json.dump({"bold": list(bold_paras), "non_bold": list(non_bold_paras)}, f)
