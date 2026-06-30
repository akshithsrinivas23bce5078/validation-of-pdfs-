import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz
import re

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
doc = fitz.open(pdf_path)

out = open(r'c:\Users\Akshith Srinivas\chunk-validator-one\som_pdf_headings.txt', 'w', encoding='utf-8')

# Pattern: starts with number, or *number
heading_pattern = re.compile(r'^\*?\d+')

for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = ""
            is_bold = False
            for span in line["spans"]:
                line_text += span["text"]
                if "bold" in span["font"].lower() or "Bold" in span["font"]:
                    is_bold = True
            
            line_text = line_text.strip()
            # Match bold lines starting with a number (paragraph heading pattern)
            if is_bold and heading_pattern.match(line_text) and len(line_text) > 2:
                # Only take the heading portion (first line, up to a long dash or period)
                # Truncate for readability
                display = line_text[:120]
                print(f"Page {page_num+1:3d} | {display}", file=out)

doc.close()
out.close()
print("Done. Written to som_pdf_headings.txt")
