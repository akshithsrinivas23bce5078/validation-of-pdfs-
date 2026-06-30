import pdfplumber
import re

unbold_paras = []

with pdfplumber.open(r"assigned pdfs\The Secretariat Office Manual.pdf") as pdf:
    for page in pdf.pages:
        words = page.extract_words(extra_attrs=['fontname'])
        for i, w in enumerate(words):
            text = w['text']
            m = re.match(r'^(\d{1,3})\.$', text)
            if m:
                # Check if the font is bold
                font = w.get('fontname', '').lower()
                if 'bold' not in font and 'black' not in font:
                    unbold_paras.append(m.group(1))

print("Unbold paragraphs found:", unbold_paras)
