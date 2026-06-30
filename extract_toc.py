import PyPDF2
import re
import json

pdf_path = r"assigned pdfs\RAM 2022 Sixth Edition.pdf"
reader = PyPDF2.PdfReader(pdf_path)

toc_lines = []
for i in range(0, 40): # TOC pages
    text = reader.pages[i].extract_text()
    if "CONTENTS" in text or "........." in text or "CHAPTER" in text:
        toc_lines.extend(text.split('\n'))

headings = {}
for line in toc_lines:
    # Match patterns like: "1. BACKGROUND ............. 32"
    # or "1.1 MAKING OF RAM ......... 32"
    m = re.match(r'^\s*(\d+(?:\.\d+)*)\.?\s+(.+?)(?:\s+\.{3,}|\s+\d+$)', line)
    if m:
        num = m.group(1).strip()
        title = m.group(2).strip()
        # Clean title: normalize spaces
        clean_title = re.sub(r'\s+', ' ', title.upper())
        # Remove trailing dot leaders that might have slipped through
        clean_title = re.sub(r'\.{2,}.*', '', clean_title).strip()
        
        full_title = f"{num}. {title.title()}" if "." not in num else f"{num} {title.title()}"
        # Normalize spaces in full_title as well
        full_title = re.sub(r'\s+', ' ', full_title)
        
        headings[clean_title] = full_title

with open("toc_mapping.json", "w", encoding="utf-8") as f:
    json.dump(headings, f, indent=2)

print(f"Extracted {len(headings)} numbered headings from PDF TOC.")
for k in ["BACKGROUND", "MAKING OF RAM", "STRUCTURE OF RAM", "FEATURES OF RAM"]:
    print(f"{k}: {headings.get(k)}")

