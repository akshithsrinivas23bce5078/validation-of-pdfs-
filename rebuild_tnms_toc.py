import json
import re
from collections import defaultdict

# The Exact Table of Contents cleaned
exact_toc = {
    "1": "Constitution",
    "2": "Categories and posts to which direct recruitment may be made",
    "3": "Method of recruitment Special",
    "4": "Promotion",
    "5": "Promotion to Selection Post",
    "6": "Promotion in different Offices",
    "7": "Appointment of J.A. in Agricultural Department",
    "8": "Omitted",
    "9": "Transfers between categories",
    "10": "Appointing Authority",
    "11": "Departmental Unit Recruitment",
    "12": "List of approved Candidates - categories and posts concerned",
    "13": "List of approved candidates - Preparation",
    "13A": "Preparation of annual list of approved candidates",
    "14": "List of approved candidates unallotted",
    "15": "Permanent allotment of candidates to Departmental Unit and their appointment",
    "16": "Candidates allotted to but not actually employed in the Departmental Unit",
    "17": "List of probationers for Administrative Units - Service Book",
    "18": "Discharge and reappointment of probationers and approved probationers",
    "19": "Candidates discharged from Survey Parties - Reappointment",
    "20": "Transfer of probationers and approved probationers",
    "21": "Allotment of candidates with special qualifications",
    "22": "Failure of approved candidates, discharged probationers and approved probationers to join duty when required",
    "23": "Competent authority",
    "24": "Separate List of approved candidates",
    "25": "Qualifications - sex",
    "26": "Reservation of appointment",
    "27": "Deleted",
    "28": "General qualifications as to Age",
    "29": "Minimum General Educational Qualification",
    "30": "Special Qualifications",
    "31": "Securities",
    "32": "Probation",
    "33": "Probationers desiring courses of study not connected with probation",
    "34": "Special Tests to be passed or training to be undergone or other qualification to be acquired by persons appointed to the service",
    "35": "Special tests to be passed or training to be undergone or other qualifications to be acquired by persons after promotion",
    "36": "Order of appointment, discharge, reappointment, appointment as full member and promotion one unit",
    "37": "Promotion or transfer as Assistants or Junior Assistants",
    "38": "Special provisions",
    "39": "Special recruitment in 1952",
    "39A": "Special recruitment in 1955",
    "39B": "Special recruitment in 1957",
    "39C": "Special recruitment in October 1957",
    "39D": "Special recruitment in 1959",
    "39E": "Special recruitment in October 1959",
    "39F": "Special recruitment of temporary Junior Assistants and Settlement Inspectors in the Settlement Department",
    "39G": "Special recruitment in 1962",
    "39H": "Special recruitment of temporary Junior Assistant in Survey and Land Record Department",
    "39I": "Special recruitment of temporary staff in Survey Department governed by the Survey and Land Records Subordinate (Temporary) Service Rules",
    "39J": "Special recruitment of temporary Junior Assistant and Typists in the Survey and Land Records Department",
    "39K": "Special Recruitment of temporary Junior Assistant and Typist in the Survey and Land Records Department",
    "39L": "Special recruitment of temporary Junior Assistant and Typist in the Survey and Land Records Department."
}

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_MINISTERIAL_SERVICE_RULES.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Filter Annexure
valid_chunks = [c for c in chunks if c.get('section') != 'Annexure']

# We must accumulate text based on current valid TOC rule
accumulated_text = defaultdict(list)
current_rule = "1"
first_page_no = defaultdict(str)

def get_numeric_val(rule_str):
    num = re.sub(r'\D', '', rule_str)
    return int(num) if num else 999

for c in valid_chunks:
    rule_no = c.get('rule_no', '')
    
    # Check if rule_no is an exact match in our TOC
    if rule_no in exact_toc:
        current_rule = rule_no
    else:
        # Check if the stripped version (e.g. '8A' -> '8') is in TOC
        base_rule = rule_no[0] if rule_no else ''
        if base_rule in exact_toc:
            # We map 5A, 5B, 5C to 5 as they are not in TOC
            # We map 1A, 2A to 1 and 2
            current_rule = base_rule
        # If we can't find it, we just keep appending to whatever the current_rule is
    
    if not first_page_no[current_rule]:
        first_page_no[current_rule] = c.get('page_no', '(1-1)')
        
    accumulated_text[current_rule].append(c.get('text', ''))

out_chunks = []
doc_id = valid_chunks[0].get('doc_id', 'TNMS-12345').upper()

# Order the keys according to numeric value and letter
def sort_key(rule_str):
    num_part = re.sub(r'\D', '', rule_str)
    num = int(num_part) if num_part else 999
    letter_part = re.sub(r'\d', '', rule_str)
    return (num, letter_part)

for rule_no in sorted(list(accumulated_text.keys()), key=sort_key):
    toc_title = exact_toc[rule_no]
    heading = f"{rule_no}. {toc_title}"
    
    full_text = "\n".join(accumulated_text[rule_no])
    
    # Strip the TOC title from the beginning of the text
    esc_title = re.escape(toc_title)
    esc_rule = re.escape(rule_no)
    pattern = rf"^(?:{esc_rule}\.\s*)?(?:{esc_title})[.\-—\s]*"
    new_text = re.sub(pattern, "", full_text, count=1, flags=re.IGNORECASE)
    
    if not new_text.strip():
        new_text = full_text  # fallback
    
    has_table = False
    table_html = "{}"
    
    table_match = re.split(r'\bTABLE\b', new_text, maxsplit=1, flags=re.IGNORECASE)
    if len(table_match) > 1:
        has_table = True
        table_content = table_match[1].strip()
        table_html = f"<table border='1'>\n<tbody>\n<tr>\n<td><pre>\nTABLE\n{table_content}\n</pre></td>\n</tr>\n</tbody>\n</table>"

    chunk = {
        "DOC_NAME": "TAMIL_NADU_MINISTERIAL_SERVICE_RULES",
        "doc_id": doc_id,
        "chapter": "1",
        "title": "TAMIL NADU MINISTERIAL SERVICE RULES",
        "heading": heading,
        "text": new_text.strip(),
        "page.no": first_page_no[rule_no],
        "has_table": has_table,
        "table_html": table_html
    }
    out_chunks.append(chunk)

out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TAMIL_NADU_MINISTERIAL_SERVICE_RULES_validated.jsonl'
import os
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as f:
    for c in out_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Generated {len(out_chunks)} chunks perfectly matching the TOC in {out_path}.")
