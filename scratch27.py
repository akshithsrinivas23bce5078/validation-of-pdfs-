import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

replacements = {
    r'\bL oan\b': 'Loan',
    r'\bA mbulance\b': 'Ambulance',
    r'\bP anchayat\b': 'Panchayat',
    r'\bM unicipality\b': 'Municipality',
    r'\bD epartment\b': 'Department',
    r'\bG overnment\b': 'Government',
    r'\bE xpenditure\b': 'Expenditure',
    r'\bR egister\b': 'Register',
    r'\bC ouncil\b': 'Council',
    r'\bS uperintendent\b': 'Superintendent',
    r'\bO fficer\b': 'Officer',
    r'\bT own\b': 'Town',
    r'\bE xecutive\b': 'Executive',
    r'\bE ngineer\b': 'Engineer',
    r'\bA ssistant\b': 'Assistant',
    r'\bM aintenance\b': 'Maintenance',
    r'\bC ollection\b': 'Collection',
    r'\bR evenue\b': 'Revenue',
    r'\bD irector\b': 'Director',
    r'\bS tate\b': 'State',
    r'\bP ublic\b': 'Public',
    r'\bS cheme\b': 'Scheme',
    r'\bT amil\b': 'Tamil',
    r'\bN adu\b': 'Nadu',
    r'\bI ndian\b': 'Indian',
    r'\bM edical\b': 'Medical',
    r'\bA udit\b': 'Audit',
    r'\bC orporation\b': 'Corporation',
    r'\bC harges\b': 'Charges',
    r'\bR ules\b': 'Rules',
    r'\bA uthority\b': 'Authority',
    r'\bP ower\b': 'Power',
    r'\bT ransport\b': 'Transport',
    r'\bC ontingencies\b': 'Contingencies',
    r'\bE ducation\b': 'Education',
    r'\bS ervice\b': 'Service',
    r'\bS upply\b': 'Supply',
    r'\bM aterials\b': 'Materials',
    r'\bP urchase\b': 'Purchase',
    r'\bG rant\b': 'Grant',
    r'\bF und\b': 'Fund',
    r'\bC ommittee\b': 'Committee',
    r'\bB oard\b': 'Board',
    r'\bB ank\b': 'Bank',
    r'\bP ost\b': 'Post',
    r'\bF ee\b': 'Fee'
}

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

total_changes = 0

for i in range(len(lines)):
    data = json.loads(lines[i])
    original_text = data.get('text', '')
    original_table = data.get('table_html', '')
    
    t = original_text
    table = original_table
    
    for pattern, repl in replacements.items():
        t = re.sub(pattern, repl, t)
        table = re.sub(pattern, repl, table)
        
    if t != original_text or table != original_table:
        data['text'] = t
        data['table_html'] = table
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        total_changes += 1

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"Fixed space-split OCR typos in {total_changes} chunks.")
