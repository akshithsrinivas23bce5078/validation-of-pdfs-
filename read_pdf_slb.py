import fitz
import json

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Handbook_slb_wsss.pdf'
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
for i in range(min(5, len(doc))):
    page = doc[i]
    text = page.get_text()
    print(f"\n--- Page {i+1} ---")
    print(text[:500])

# check for tables
table_count = 0
for i in range(len(doc)):
    page = doc[i]
    tables = page.find_tables()
    if tables and tables.tables:
        print(f"Page {i+1} has {len(tables.tables)} tables")
        table_count += len(tables.tables)
print(f"Total tables found: {table_count}")
