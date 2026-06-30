import fitz

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TAMIL NADU SECRETARIAT SERVICE RULES.pdf'
doc = fitz.open(pdf_path)

for i in range(len(doc)):
    page = doc[i]
    tabs = page.find_tables(strategy="lines_strict")
    if not tabs.tables:
        tabs = page.find_tables(strategy="text")
    for j, tab in enumerate(tabs):
        print(f"Page {i+1} Table {j+1}:")
        print(tab.extract())
