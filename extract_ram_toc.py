import fitz
import re
import json

pdf_path = r"C:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\RAM 2022 Sixth Edition.pdf"
doc = fitz.open(pdf_path)

# Extract TOC from pages 2 to 14
toc_headings = []
for p in range(1, 15):
    page = doc[p]
    text = page.get_text()
    for line in text.split('\n'):
        # match patterns like "2.1.1 History of Railway Audit .........3"
        m = re.match(r'^(\d+(?:\.\d+)*)\s+([^.]*?)\s*\.{3,}', line.strip())
        if m:
            num = m.group(1).strip()
            title = m.group(2).strip()
            toc_headings.append(f"{num} {title}")

# Let's save TOC headings to see what we are dealing with
with open(r"C:\Users\Akshith Srinivas\chunk-validator-one\ram_toc.txt", "w", encoding="utf-8") as f:
    for h in toc_headings:
        f.write(h + "\n")

print(f"Extracted {len(toc_headings)} TOC headings.")
