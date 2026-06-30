import fitz
import re

unbold_paras = []
pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

for page_num in range(len(pdf)):
    page = pdf[page_num]
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b['type'] == 0:
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    m = re.match(r'^(\d{1,3})\.$', text)
                    if m:
                        font = s["font"].lower()
                        # If font is not bold
                        if 'bold' not in font and 'black' not in font:
                            unbold_paras.append(m.group(1))

print("Unbold paragraphs found:", unbold_paras)
