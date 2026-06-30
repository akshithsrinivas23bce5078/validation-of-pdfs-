"""
Comprehensive heading correction for The Secretariat Office Manual JSONL.
Reads bold headings from the PDF and updates bare/incomplete headings in the JSONL.
"""
import json
import sys
import re
import os
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

# ========== STEP 1: Extract PDF headings ==========
doc = fitz.open(pdf_path)
heading_pattern = re.compile(r'^\*?(\d+(?:\.\w+)?)[.\s]')

pdf_headings = {}  # para_num_str -> heading title (just the title part)

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
            if not (is_bold and heading_pattern.match(line_text) and len(line_text) > 2):
                continue
                
            m = re.match(r'^\*?(\d+(?:\.\w+)?)[.\s]', line_text)
            if not m:
                continue
            para_key = m.group(1)
            
            # Extract just the heading title portion (before body text starts)
            # Remove the leading * and number
            raw = re.sub(r'^\*?', '', line_text).strip()
            
            # Find the heading title - it ends at the em-dash followed by body text
            # Pattern: "N. Title.— Body text..."
            # We want: "N. Title.-"
            
            # Try to find title ending pattern: ".—" or "—" or ".— "
            title_match = re.match(r'^(\d+(?:\.\w+)?\.\s*.+?)[.\s]*[\u2014\u2015—]', raw)
            if title_match:
                title = title_match.group(1).strip()
                # Normalize dash
                title = title + '.-'
            else:
                # No em-dash found - the whole line might be the heading
                # Truncate at reasonable length (some headings span into text)
                title = raw.split('.')[0] + '.' if '.' in raw else raw
                # If it's very long, it's probably heading + body text
                if len(raw) > 80:
                    title = raw[:80].rsplit(' ', 1)[0] + '.-'
                else:
                    title = raw.rstrip('.-').strip() + '.-'
            
            # Clean up
            title = title.replace('\u2014', '-').replace('\u2015', '-').replace('—', '-')
            title = title.replace('.-.-', '.-')
            
            if para_key not in pdf_headings:
                pdf_headings[para_key] = title

doc.close()
print(f"Extracted {len(pdf_headings)} headings from PDF")

# ========== STEP 2: Update JSONL headings ==========
with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_count = 0
details = []

for i in range(len(lines)):
    d = json.loads(lines[i])
    h = d.get('heading', '').strip()
    
    # Extract para number from current heading
    m = re.match(r'^\*?(\d+(?:\.\w+)?)[.\s]', h)
    if not m:
        continue
    para_key = m.group(1)
    
    # Check if heading is bare (just number, or number + period)
    is_bare = re.match(r'^\*?\d+(?:\.\w+)?\.\s*$', h)
    
    # Get PDF heading
    pdf_h = pdf_headings.get(para_key, None)
    if not pdf_h:
        continue
    
    # If the JSONL heading is bare (just a number), replace with PDF heading
    if is_bare:
        old_h = h
        d['heading'] = pdf_h
        lines[i] = json.dumps(d, ensure_ascii=False) + '\n'
        fixed_count += 1
        details.append(f"  Line {i+1}: '{old_h}' -> '{pdf_h}'")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)

print(f"\nFixed {fixed_count} bare headings")
for d in details[:30]:
    print(d)
if len(details) > 30:
    print(f"  ... and {len(details)-30} more")
