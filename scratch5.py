import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl.tmp'

with open(file_path, 'r', encoding='utf-8') as fin, open(output_path, 'w', encoding='utf-8') as fout:
    for line in fin:
        data = json.loads(line)
        heading = data.get('heading', '')
        
        # Remove parentheses and replace unicode replacement character in heading
        if ')' in heading or '(' in heading or '\ufffd' in heading:
            new_heading = heading.replace(')', '').replace('(', '').replace('\ufffd', '-')
            # Also clean up any leading spaces that might have been left if ')' was at the start
            new_heading = new_heading.replace(' -  ', ' - ').replace('  ', ' ')
            data['heading'] = new_heading
            print(f"Updated heading: {new_heading}")
            
        # Write with ensure_ascii=False to convert all \uXXXX sequences to UTF-8 chars
        fout.write(json.dumps(data, ensure_ascii=False) + '\n')

os.replace(output_path, file_path)
