import json
import re

toc_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\new_toc_mapping.json'
with open(toc_path, 'r', encoding='utf-8') as f:
    toc = json.load(f)

# Build a set of normalized valid headings
def norm(t):
    return re.sub(r'\s+', ' ', t.lower()).strip()

valid_headings = {norm(v): v for v in toc.values()}

# Regex to match a heading line. It must start with digits and dots at the beginning of a line.
# We also allow it if it's the very first line of the text.
heading_pattern = re.compile(r'(?:^|\n)(\d+(?:\.\d+)*\s+[A-Z][^\n]{3,120}?)(?=\n|$)')

test_text = """Some prefix text here.
2.1.2 Organizational set up
Organization al set up of the Railway Audit Branch:
2.1.3 Authority of the Comptroller and Auditor General of India
The Comptroller and Auditor General..."""

matches = list(heading_pattern.finditer(test_text))
print("Matches found:")
for m in matches:
    h = m.group(1).strip()
    print(f"[{h}] -> valid? {norm(h) in valid_headings}")

