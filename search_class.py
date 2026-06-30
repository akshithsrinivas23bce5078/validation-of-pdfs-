import fitz
import re

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')
text = ""
for page in doc[15:100]:
    text += page.get_text() + "\n"

for m in re.finditer(r'.{0,50}Classification.{0,50}', text, re.IGNORECASE | re.DOTALL):
    print(repr(m.group(0)))
