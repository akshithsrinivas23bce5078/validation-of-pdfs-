import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

missing_defs = {
    "8.1": "Account",
    "8.2": "Accounting Entry",
    "8.3": "Account Payable",
    "8.83": "Ledger",
    "8.84": "Leasehold lands",
    "8.100": "Outstanding expenses",
    "8.101": "Prepaid expenses",
    "8.102": "Prior period expenses",
    "8.103": "Provisions",
    "8.104": "Provision for Expense",
    "8.105": "Provision for Unrealised Revenue",
    "8.106": "Prudence",
    "8.107": "Qualifying Fixed Asset",
    "8.108": "Receipt",
    "8.109": "Receipts and payment Statement",
    "8.120": "Sundry Creditors",
    "8.121": "Surplus",
    "8.122": "Trial balance",
    "8.123": "Useful life",
    "8.124": "Voucher",
    "8.125": "Work in progress"
}

# General specific headings for other chapters
other_headings = {
    "0": "List of Acronyms",
    "2.2": "Objectives of the uniform Accounting Manual",
    "5": "Difference between Single- entry cash basis and double entry accrual basis of accounting AND DOUBLE ENTRY ACCRUAL BASIS OF ACCOUNTING",
    "9": "General Principle of double entry accrual basis of accounting ACCRUAL BASIS OF ACCOUNTING",
    "10": "Procedure for review and change in the manual MANUAL",
    "11": "Change Request form",
    "12": "Clarification request form"
}

corrected = 0
for c in chunks:
    text = c['text']
    heading_found = False
    
    # Check if it's one of the missing Chapter 8 defs
    if str(c['chapter']) == '8':
        m = re.match(r'^8\.(\d+)\s+(.*)', text)
        if m:
            num = "8." + m.group(1)
            rest = m.group(2)
            if num in missing_defs:
                true_heading = missing_defs[num]
                heading_pattern = re.escape(true_heading).replace(r'\ ', r'\s+')
                new_rest = re.sub('^' + heading_pattern + r'[\s:]*', '', rest, flags=re.IGNORECASE)
                c['heading'] = true_heading
                c['text'] = new_rest
                corrected += 1
                heading_found = True
    
    if not heading_found and not c['heading']:
        # Check for specific headings in other_headings
        for prefix, h_text in other_headings.items():
            if text.startswith(prefix + " ") or text.startswith(prefix + ")") or text.startswith(prefix + " \t") or text == prefix:
                true_heading = h_text
                # strip prefix and true heading
                rest = text[len(prefix):].lstrip(') \t.')
                heading_pattern = re.escape(true_heading).replace(r'\ ', r'\s+')
                new_rest = re.sub('^' + heading_pattern + r'[\s:]*', '', rest, flags=re.IGNORECASE)
                
                # Exception: For Change Request Form and Clarification Request Form, the text has parentheses
                if prefix in ["11", "12"]:
                    new_rest = rest
                    new_rest = new_rest.replace("Change Request form", "", 1).strip()
                    new_rest = new_rest.replace("Clarification request form", "", 1).strip()
                    
                c['heading'] = true_heading
                c['text'] = new_rest
                corrected += 1
                heading_found = True
                break
                
    if not heading_found and not c['heading']:
        # For paragraphs like "1.1 The ULBs...", just strip the number
        m = re.match(r'^(\d+(?:\.\d+)*)[\.\)]?\s+(.*)', text)
        if m:
            c['text'] = m.group(2)
            corrected += 1

print(f"Corrected {corrected} chunks")

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
