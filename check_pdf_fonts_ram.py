import fitz

pdf_path = r"C:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\RAM 2022 Sixth Edition.pdf"
doc = fitz.open(pdf_path)

headings = []

for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    # Check if font is bold or size is larger
                    # Let's just print a few to see the structure of chapters 1 & 2
                    if page_num < 15: # Just first few pages
                        print(f"Page {page_num+1}: [{span['size']:.1f} {span['font']}] {text}")

