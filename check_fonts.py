import pdfplumber

with pdfplumber.open(r"assigned pdfs\The Secretariat Office Manual.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        words = page.extract_words()
        for w in words:
            if w['text'] == "578.":
                print(f"Page {i+1}: '578.' font is {w['fontname']}")
            elif w['text'] == "579.":
                print(f"Page {i+1}: '579.' font is {w['fontname']}")
            elif w['text'] == "577.":
                print(f"Page {i+1}: '577.' font is {w['fontname']}")
