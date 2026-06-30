"""
Extract the footnotes (* and $) from the definition chunks and append them at the end of Para 18.
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix Line 20 (index 19)
d_branch = json.loads(lines[19])
# old text: "*Branch is the term used to denote the Branches, viz., Central Record Branch. * vide G.O.Ms.No.236, P&AR (A) Department, dated. 27-12-1999"
d_branch['heading'] = "Branch.-"
d_branch['text'] = "Branch is the term used to denote the Branches, viz., Central Record Branch."
lines[19] = json.dumps(d_branch, ensure_ascii=False) + '\n'

# Fix Line 52 (index 51)
d_digital = json.loads(lines[51])
# old text might be: "Digital Signature.—Digital Signature Certificates (DSC) is a e-sign feature available for approving of the notes/drafts by the Approving Authority in the e-Office work flow.  [Inserted in G.O.Ms.No.16, P &AR(A) Department, dated 06.02.2020]"
text_digital = d_digital['text']
split_idx = text_digital.find('[Inserted in G.O.Ms.No.16')
if split_idx != -1:
    d_digital['text'] = text_digital[:split_idx].strip()
else:
    # Handle just in case
    d_digital['text'] = text_digital.split('[Inserted')[0].strip()
lines[51] = json.dumps(d_digital, ensure_ascii=False) + '\n'

# Create the two new chunks to insert
d_star = dict(d_branch)
d_star['heading'] = "*.-"
d_star['text'] = "* vide G.O.Ms.No.236, P&AR (A) Department, dated. 27-12-1999"

d_dollar = dict(d_digital)
d_dollar['heading'] = "$.-"
d_dollar['text'] = "$ [Inserted in G.O.Ms.No.16, P &AR(A) Department, dated 06.02.2020]"

# Insert them after line 52 (index 52)
lines.insert(52, json.dumps(d_star, ensure_ascii=False) + '\n')
lines.insert(53, json.dumps(d_dollar, ensure_ascii=False) + '\n')

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print("Successfully extracted footnotes to the end of Para 18.")
