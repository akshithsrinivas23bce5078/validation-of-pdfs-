"""
Second pass: Fix truncated headings by extracting FULL heading text from PDF.
Uses multi-line bold text aggregation to get the complete title.
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

doc = fitz.open(pdf_path)

# Extract ALL bold text per page, then parse headings more carefully
pdf_headings_full = {}  # para_key -> full heading title

for page_num in range(len(doc)):
    page = doc[page_num]
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if "lines" not in block:
            continue
        
        # Aggregate all bold text in this block
        bold_text_parts = []
        for line in block["lines"]:
            for span in line["spans"]:
                if "bold" in span["font"].lower() or "Bold" in span["font"]:
                    bold_text_parts.append(span["text"])
        
        if not bold_text_parts:
            continue
        
        bold_text = " ".join(bold_text_parts).strip()
        bold_text = re.sub(r'\s+', ' ', bold_text)
        
        # Check if this bold block starts with a paragraph number
        m = re.match(r'^\*?(\d+(?:\.\w+)?)[.\s]', bold_text)
        if not m:
            continue
        
        para_key = m.group(1)
        
        # Extract the heading title:
        # Pattern: "N. Title Text.— body text..." or "N. Title Text.—"
        # We want everything up to and including the em-dash
        
        # First try: find em-dash separator
        emdash_match = re.search(r'[\u2014\u2015—]', bold_text)
        if emdash_match:
            title = bold_text[:emdash_match.start()].strip()
        else:
            # No em-dash - use the full bold text as title
            title = bold_text.strip()
        
        # Remove leading asterisk
        title = re.sub(r'^\*\s*', '', title).strip()
        
        # Clean up: remove trailing period if followed by nothing
        title = title.rstrip('.')
        
        # Add standard suffix
        title = title + '.-'
        
        # Normalize dashes
        title = title.replace('\u2014', '-').replace('\u2015', '-').replace('—', '-')
        
        # Don't overwrite if we already have a good one (first occurrence wins)
        if para_key not in pdf_headings_full:
            pdf_headings_full[para_key] = title

doc.close()

# Now fix the specific truncated headings
# Read the current JSONL
with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Identify which headings need fixing
fixes = {}
for i, line in enumerate(lines):
    d = json.loads(line)
    h = d.get('heading', '').strip()
    
    m = re.match(r'^\*?(\d+(?:\.\w+)?)[.\s]', h)
    if not m:
        continue
    para_key = m.group(1)
    
    needs_fix = False
    
    # Check truncated (ends with preposition + .-)
    if re.search(r'\b(of|the|in|to|a|an|on|by|or|and|for|from)\.-$', h):
        needs_fix = True
    # Bare heading like "76.-"
    elif re.match(r'^\*?\d+(?:\.\w+)?\.-$', h):
        needs_fix = True
    # Bad ending with comma
    elif ',.-' in h:
        needs_fix = True
    
    if needs_fix and para_key in pdf_headings_full:
        pdf_h = pdf_headings_full[para_key]
        # Only update if the PDF heading is actually better
        if len(pdf_h) > len(h) or (re.match(r'^\d+\.-$', h) and len(pdf_h) > 5):
            fixes[i] = (h, pdf_h, para_key)

# Apply fixes
for i, (old_h, new_h, para_key) in fixes.items():
    d = json.loads(lines[i])
    d['heading'] = new_h
    lines[i] = json.dumps(d, ensure_ascii=False) + '\n'

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)

print(f"Fixed {len(fixes)} truncated/bare headings:")
for i, (old_h, new_h, para_key) in sorted(fixes.items()):
    print(f"  Line {i+1}: '{old_h}' -> '{new_h}'")
