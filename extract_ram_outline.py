import fitz

pdf_path = r"C:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\RAM 2022 Sixth Edition.pdf"
doc = fitz.open(pdf_path)
toc = doc.get_toc()

with open(r"C:\Users\Akshith Srinivas\chunk-validator-one\ram_toc.txt", "w", encoding="utf-8") as f:
    for item in toc:
        f.write(f"{item[0]} | {item[1]} | {item[2]}\n")

print(f"Extracted {len(toc)} outline items.")
