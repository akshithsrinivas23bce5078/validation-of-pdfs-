"""
Third pass: Manual corrections for remaining 21 truncated headings.
These headings span multiple text blocks in the PDF and can't be auto-extracted.
We'll read the PDF page text near each heading to complete them.
"""
import json
import sys
import re
import os
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'

doc = fitz.open(pdf_path)

# For each problematic paragraph, search for it in PDF and print surrounding text
problem_paras = [48, 60, 92, 109, 110, 141, 209, 246, 251, 252, 254, 260, 269, 297, 318, 334, 347, 433, 496, 503, 570]

for pn in problem_paras:
    pattern = f"{pn}."
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue
            
            # Check if this block contains our paragraph number
            block_text = ""
            bold_parts = []
            for line in block["lines"]:
                for span in line["spans"]:
                    block_text += span["text"]
                    if "bold" in span["font"].lower() or "Bold" in span["font"]:
                        bold_parts.append(span["text"])
            
            if re.match(rf'^\*?{pn}[\.\s]', block_text.strip()):
                full_bold = " ".join(bold_parts).strip()
                full_bold = re.sub(r'\s+', ' ', full_bold)
                print(f"\n=== Para {pn} (Page {page_num+1}) ===")
                print(f"  Full bold text: {full_bold[:200]}")
                print(f"  Block text start: {block_text.strip()[:200]}")
                break
        else:
            continue
        break

doc.close()
