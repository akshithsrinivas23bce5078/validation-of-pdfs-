import json

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\tngscr_rules_1973_160625_validated.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\tngscr_rules_1973_160625_validated_fixed.jsonl'

fixed_count = 0
with open(file_path, 'r', encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        data = json.loads(line)
        if data['has_table'] and data['table_html'] in ('{}', '', None):
            data['has_table'] = False
            fixed_count += 1
        f_out.write(json.dumps(data) + '\n')

print(f"Fixed {fixed_count} inconsistencies.")

import os
os.replace(output_path, file_path)
print("File successfully replaced.")
