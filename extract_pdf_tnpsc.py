import fitz

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\TNPSC_AF_Rule_2022.pdf'
doc = fitz.open(pdf_path)

with open('tnpsc_pdf_dump.txt', 'w', encoding='utf-8') as f:
    for i in range(len(doc)):
        f.write(f'--- Page {i+1} ---\n')
        f.write(doc[i].get_text())
        f.write('\n\n')
