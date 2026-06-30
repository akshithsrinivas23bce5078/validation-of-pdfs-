import fitz
import json

pdf = fitz.open(r"assigned pdfs\The Secretariat Office Manual.pdf")

bold_text = []
for page in pdf:
    for b in page.get_text("dict")["blocks"]:
        if b['type'] == 0:
            for l in b['lines']:
                for s in l['spans']:
                    if 'bold' in s['font'].lower() or 'black' in s['font'].lower():
                        bold_text.append(s['text'].strip())

bold_str = " ".join(bold_text)

with open(r"unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

not_bold_headings = []
for c in chunks:
    h = c.get('heading', '').strip()
    if h and h != "null" and h != " ":
        # check if h is in the bold text
        # h might be split across spans, so just check a substring
        h_clean = h.replace("\u2014", "").strip()
        if h_clean[:10] not in bold_str:
            not_bold_headings.append(h)

print(f"Found {len(not_bold_headings)} headings that are not bold in the PDF out of {len(chunks)} chunks.")
print(not_bold_headings[:20])

