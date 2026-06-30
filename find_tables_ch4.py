import fitz
import json

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')

tables_found = []

for p in range(400, 515):
    if p - 1 < len(doc):
        page = doc[p-1]
        tabs = page.find_tables()
        if tabs and len(tabs.tables) > 0:
            tables_found.append((p, len(tabs.tables)))
            
print("Tables found in Chapter 4 (page, count):", tables_found)
