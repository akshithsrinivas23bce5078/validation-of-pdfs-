import fitz
import json

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

# Build a mapping from paragraph number to whether it's bold
para_bold_map = {}

import re

for page_num in range(len(pdf)):
    page = pdf[page_num]
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b.get('type') == 0:
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    m = re.match(r'^(\d{1,3})\.', text)
                    if m:
                        para_num = m.group(1)
                        font = s["font"].lower()
                        is_bold = 'bold' in font or 'black' in font
                        if para_num not in para_bold_map:
                            para_bold_map[para_num] = []
                        para_bold_map[para_num].append(is_bold)

unbolded_paras = []
for k, v in para_bold_map.items():
    # If the majority of times it appears it's NOT bold
    if v.count(False) > v.count(True):
        unbolded_paras.append(k)

print(f"Total paras identified: {len(para_bold_map)}")
print(f"Total unbolded paras: {len(unbolded_paras)}")
print(f"Unbolded paras: {unbolded_paras}")
