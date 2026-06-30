import json
import re
import sys
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl.tmp'

def clean_text(text, heading):
    original_text = text
    
    # Remove 'Para . n :' or 'Para n - ' or similar from the start
    # e.g. "Para . 4 : " or "Para 4 :" or "Para 4 - "
    text = re.sub(r'^Para\s*\.?\s*\d+\s*[:-]?\s*', '', text, flags=re.IGNORECASE)
    
    # The heading is something like "Para 4 - AUDIT FUNCTIONS OF ASSISTANT DIRECTORS"
    # We want to remove the actual title part from the start of the text.
    m = re.match(r'^Para\s*\d+\s*-\s*(.*)$', heading, flags=re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        # Clean title for regex (escape special chars)
        title_escaped = re.escape(title)
        # Remove the title from the start of the text if it's there
        # e.g., "AUDIT FUNCTIONS OF ASSISTANT DIRECTORS:- "
        pattern = r'^' + title_escaped + r'\s*[:-]*\s*'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
    return text, original_text

changed = 0
with open(file_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        text = data.get('text', '')
        heading = data.get('heading', '')
        
        cleaned, original = clean_text(text, heading)
        if cleaned != original:
            changed += 1
            # Print first 100 chars to see what changed
            print(f"Old: {repr(original[:100])}")
            print(f"New: {repr(cleaned[:100])}")
            print("-" * 40)
            
        data['text'] = cleaned
        fout.write(json.dumps(data, ensure_ascii=False) + '\n')

print(f"Total changed: {changed}")
os.replace(output_path, file_path)
