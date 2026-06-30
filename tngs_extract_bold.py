import fitz
import json
import re

pdf = fitz.open(r'assigned pdfs\TNGS_ClassXII_11032022.pdf')

bold_texts = []
for page_num, page in enumerate(pdf):
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if b['type'] == 0:
            for l in b['lines']:
                line_text = ""
                is_bold = False
                for s in l['spans']:
                    if 'Bold' in s['font']:
                        is_bold = True
                    line_text += s['text']
                if is_bold:
                    clean_text = line_text.strip()
                    if clean_text:
                        bold_texts.append(clean_text)

with open("tngs_bold_texts.json", "w", encoding="utf-8") as f:
    json.dump(bold_texts, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(bold_texts)} bold lines.")
