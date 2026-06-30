import fitz
import re

doc = fitz.open(r"c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\19. Opening Balance Sheet Accounting Manual P_State Audit West Ben.pdf")
text = "\n".join([doc[i].get_text() for i in range(15, 23)])

for match in re.finditer(r'(?s)(21\..*?)(?=22\.)', text):
    print("MATCH 21:", match.group(1))

for match in re.finditer(r'(?s)(25\..*?)(?=26\.)', text):
    print("MATCH 25:", match.group(1))
    
for match in re.finditer(r'(?s)(29\..*?)(?=30\.)', text):
    print("MATCH 29:", match.group(1))
