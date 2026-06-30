import json
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_SECRETARIAT_SERVICE_RULES_validated.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        d = json.loads(line)
        if d.get('heading', '').startswith('8.'):
            d['heading'] = "8. Pattern of appointment of Assistant Section Officers in the Departments of Secretariat other than the Law Department, Tamil Development, Culture and Religious Endowments Department (Translations) and Governor's Secretariat."
        f_out.write(json.dumps(d, ensure_ascii=False) + '\n')

os.replace(output_path, file_path)
print("Updated heading 8 successfully.")
