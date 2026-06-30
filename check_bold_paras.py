import fitz
import json
import re

pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

bold_paras = []
non_bold_paras = []

for page in pdf:
    for b in page.get_text("dict")["blocks"]:
        if b['type'] == 0:
            for l in b['lines']:
                for s in l['spans']:
                    text = s['text'].strip()
                    if re.match(r'^\d{1,3}\.', text):
                        is_bold = 'bold' in s['font'].lower() or 'black' in s['font'].lower()
                        if is_bold:
                            bold_paras.append(text)
                        else:
                            non_bold_paras.append(text)

print(f"Found {len(bold_paras)} bold paragraphs.")
print(f"Found {len(non_bold_paras)} non-bold paragraphs.")
print("Some non-bold paras:", non_bold_paras[:20])
print("Some bold paras:", bold_paras[:20])

