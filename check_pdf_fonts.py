import fitz

pdf = fitz.open(r'assigned pdfs\TNGS_ClassXII_11032022.pdf')
page = pdf[2] # page 3
for b in page.get_text('dict')['blocks']:
    if b['type'] == 0:
        for l in b['lines']:
            for s in l['spans']:
                print(f"font: {s['font']}, size: {s['size']}, text: {s['text']}")
