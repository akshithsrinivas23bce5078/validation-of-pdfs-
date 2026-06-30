import fitz

doc = fitz.open(r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\Local Fund Audit Depart Manual  Vol - II.pdf')
text = ""
for page in doc[300:400]: # chapter 3 should be roughly around here
    text += page.get_text() + "\n"

# Search for "Deposits" and "Advances"
import re
for match in re.finditer(r'.{0,100}Advances.{0,100}', text, re.IGNORECASE | re.DOTALL):
    print(match.group(0).encode('ascii', 'ignore').decode('ascii'))
    print("---")
