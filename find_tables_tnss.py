import fitz

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU SECRETARIAT SERVICE RULES.pdf'
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
for i in range(len(doc)):
    page = doc[i]
    tabs = page.find_tables()
    if len(tabs.tables) > 0:
        print(f"Page {i+1} has {len(tabs.tables)} tables")
