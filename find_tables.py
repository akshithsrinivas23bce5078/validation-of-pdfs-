import pdfplumber

pdf_path = r'assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf'

tables_info = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        if tables:
            print(f"Page {i+1}: {len(tables)} tables found")
            for j, t in enumerate(tables):
                tables_info.append({"page": i+1, "rows": len(t), "cols": len(t[0]) if t else 0})
                print(f"  Table {j+1}: {len(t)} rows")
