import fitz

pdf = fitz.open(r'assigned pdfs\TNGS_ClassXII_11032022.pdf')
page = pdf[17] # page 18
for b in page.get_text('dict')['blocks']:
    if b['type'] == 0:
        for l in b['lines']:
            for s in l['spans']:
                if 'Bold' in s['font']:
                    print(f"BOLD: {s['text']}")
