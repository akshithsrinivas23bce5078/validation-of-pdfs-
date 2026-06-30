import fitz

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU MINISTERIAL SERVICE RULES.pdf'
doc = fitz.open(pdf_path)

for i in range(min(10, len(doc))):
    text = doc[i].get_text()
    if 'CONTENTS' in text.upper() or 'RULE' in text.upper():
        print(f"--- Page {i+1} ---")
        print(text)
