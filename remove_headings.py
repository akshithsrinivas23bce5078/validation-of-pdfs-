import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_SECRETARIAT_SERVICE_RULES_validated.jsonl'
output_path = file_path + '.tmp'

# Regex to match the leading numbering and heading like "1. Definitions.— "
pattern = re.compile(r'^.*?\.\u2014\s*')

count = 0
with open(file_path, 'r', encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        data = json.loads(line)
        if 'text' in data:
            original_text = data['text']
            new_text = pattern.sub('', original_text, count=1)
            if new_text != original_text:
                data['text'] = new_text
                count += 1
        f_out.write(json.dumps(data, ensure_ascii=False) + '\n')

os.replace(output_path, file_path)
print(f"Processed {count} lines.")
