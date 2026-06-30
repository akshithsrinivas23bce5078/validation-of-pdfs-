import json
import re
import sys

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl.tmp'

def extract_title(text):
    # Try to find a delimiter
    m = re.match(r'^(.*?)(?::|-|The checks|It should be|A petty cash book|This Register|The receipt side|The pension|As per Director|The Procedure|This register|According to|To ensure|The teaching)', text, re.IGNORECASE)
    if m:
        title = m.group(1).strip()
        # Clean up trailing punctuation
        title = re.sub(r'[\.:-]+$', '', title).strip()
        return title
    return text[:30].strip()

with open(file_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        heading = data.get('heading', '')
        
        m = re.match(r'^Para (\d+) - (\d+)\.?$', heading)
        if m:
            prefix = m.group(1)
            suffix = m.group(2)
            # e.g., prefix 1, suffix 08 => 108
            new_num = prefix + suffix
            title = extract_title(data.get('text', ''))
            new_heading = f"Para {new_num} - {title}"
            print(f"Replacing '{heading}' with '{new_heading}'")
            data['heading'] = new_heading
            
        fout.write(json.dumps(data) + '\n')

import os
os.replace(output_path, file_path)
