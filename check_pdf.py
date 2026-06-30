import PyPDF2
import re

pdf_path = r"assigned pdfs\RAM 2022 Sixth Edition.pdf"
reader = PyPDF2.PdfReader(pdf_path)

# Print first few pages to find the TOC
for i in range(10, 15):
    text = reader.pages[i].extract_text()
    if "BACKGROUND" in text or "MAKING OF RAM" in text or "CONTENTS" in text:
        print(f"--- PAGE {i} ---")
        print(text[:500])
        print("...")
