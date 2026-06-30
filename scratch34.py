import json
import sys
import re
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'

# 1. Extract PDF headings
doc = fitz.open(pdf_path)
heading_pattern = re.compile(r'^\*?(\d+[\.\s])')

pdf_headings = {}  # para_num -> full heading text

for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            line_text = ""
            is_bold = False
            for span in line["spans"]:
                line_text += span["text"]
                if "bold" in span["font"].lower() or "Bold" in span["font"]:
                    is_bold = True
            
            line_text = line_text.strip()
            if is_bold and heading_pattern.match(line_text) and len(line_text) > 2:
                # Extract paragraph number
                m = re.match(r'^\*?(\d+(?:\.\w+)?)[.\s]', line_text)
                if m:
                    para_key = m.group(1)
                    # Get just the heading part (before the em-dash and body text)
                    # Find the heading title - text up to the em-dash or first sentence
                    heading_part = line_text
                    # Truncate at the em-dash followed by body text
                    for sep in ['\u2014', '\u2015', '.—', '.— ']:
                        idx = heading_part.find(sep)
                        if idx > 0:
                            heading_part = heading_part[:idx+len(sep)].strip()
                            break
                    
                    if para_key not in pdf_headings:
                        pdf_headings[para_key] = heading_part

doc.close()

# 2. Extract JSONL headings
with open(jsonl_path, 'r', encoding='utf-8') as f:
    jsonl_lines = f.readlines()

jsonl_headings = {}  # para_num -> (line_idx, heading)
for i, line in enumerate(jsonl_lines):
    d = json.loads(line)
    h = d.get('heading', '').strip()
    # Extract para number from heading
    m = re.match(r'^\*?(\d+(?:\.\w+)?)[.\s]', h)
    if m:
        para_key = m.group(1)
        if para_key not in jsonl_headings:
            jsonl_headings[para_key] = (i+1, h)

# 3. Compare
out = open(r'c:\Users\Akshith Srinivas\chunk-validator-one\som_heading_comparison.txt', 'w', encoding='utf-8')

def normalize(s):
    """Normalize for comparison: lowercase, strip special chars"""
    s = s.replace('\u2014', '-').replace('\u2015', '-').replace('—', '-').replace('.-', '-')
    s = s.replace('*', '').replace('.', ' ').replace('-', ' ').replace('  ', ' ')
    return s.lower().strip()

all_paras = sorted(set(list(pdf_headings.keys()) + list(jsonl_headings.keys())), key=lambda x: (len(x), x))

mismatches = []
missing_in_jsonl = []
missing_in_pdf = []

for para in all_paras:
    pdf_h = pdf_headings.get(para, None)
    jsonl_entry = jsonl_headings.get(para, None)
    
    if pdf_h and not jsonl_entry:
        missing_in_jsonl.append((para, pdf_h))
    elif not pdf_h and jsonl_entry:
        missing_in_pdf.append((para, jsonl_entry))
    elif pdf_h and jsonl_entry:
        line_num, jsonl_h = jsonl_entry
        # Compare normalized versions
        pdf_norm = normalize(pdf_h)
        jsonl_norm = normalize(jsonl_h)
        if pdf_norm != jsonl_norm:
            # Check if it's just truncation vs full mismatch
            if not pdf_norm.startswith(jsonl_norm[:20]) and not jsonl_norm.startswith(pdf_norm[:20]):
                mismatches.append((para, line_num, pdf_h, jsonl_h, 'MAJOR'))
            else:
                mismatches.append((para, line_num, pdf_h, jsonl_h, 'MINOR'))

print(f"=== HEADING COMPARISON REPORT ===", file=out)
print(f"PDF headings found: {len(pdf_headings)}", file=out)
print(f"JSONL headings found: {len(jsonl_headings)}", file=out)
print(f"", file=out)

print(f"=== MISMATCHES ({len(mismatches)}) ===", file=out)
for para, line, pdf_h, jsonl_h, severity in mismatches:
    print(f"\nPara {para} (Line {line}) [{severity}]:", file=out)
    print(f"  PDF:   {pdf_h[:120]}", file=out)
    print(f"  JSONL: {jsonl_h[:120]}", file=out)

print(f"\n=== IN PDF BUT MISSING IN JSONL ({len(missing_in_jsonl)}) ===", file=out)
for para, pdf_h in missing_in_jsonl:
    print(f"  Para {para}: {pdf_h[:120]}", file=out)

print(f"\n=== IN JSONL BUT NOT IN PDF ({len(missing_in_pdf)}) ===", file=out)
for para, (line, jsonl_h) in missing_in_pdf:
    print(f"  Para {para} (Line {line}): {jsonl_h[:120]}", file=out)

out.close()
print(f"Done. Mismatches: {len(mismatches)}, Missing in JSONL: {len(missing_in_jsonl)}, Missing in PDF: {len(missing_in_pdf)}")
print("Written to som_heading_comparison.txt")
