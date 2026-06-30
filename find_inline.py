import fitz
import re
import json

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

# Find all paragraph numbers in the PDF that are followed by ".-" or ".\u2014" (em dash) on the same line, or where the text just continues.
# A simpler way: Just extract all text from PDF, find all "(\d{1,3}\.[^\n]*?\.\u2014)"
pdf_text = ""
for page in pdf:
    pdf_text += page.get_text() + "\n"

inline_paras = []
for m in re.finditer(r'\n(\d{1,3}\.[^\n]*?\.[\-\u2014])', pdf_text):
    para_text = m.group(1)
    num = re.match(r'^(\d{1,3})\.', para_text).group(1)
    inline_paras.append(num)

print(f"Found {len(inline_paras)} inline paras with em-dash: {inline_paras}")

# What about paras like 577?
for m in re.finditer(r'\n(\d{1,3}\.[^\n]*?)(?:\n)', pdf_text):
    para_text = m.group(1).strip()
    num_match = re.match(r'^(\d{1,3})\.', para_text)
    if num_match:
        num = num_match.group(1)
        # If the line ends with a lower case letter or doesn't look like a title
        if re.search(r'[a-z]$', para_text) and num not in inline_paras:
             # It might be a split sentence like 577
             pass

