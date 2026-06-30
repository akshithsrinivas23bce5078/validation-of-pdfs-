"""
Fix Para 81 sub-headings (lines 85-87).
Line 85 has fragment text "C. Confirmation of oral Instructions" with heading "81."
Line 86 has actual para 81 content with incomplete heading 
Line 87 has 81.A + 81.B content with wrong heading "81."
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 85 (index 84): This has just "C. Confirmation of oral Instructions" as text
# and heading "81. Duty of Officers at all levels to take note of previous.-"
# This is a stray fragment - the text "C. Confirmation..." is actually part of 81.C
# Let's check if this is redundant with line 88 (81.C)
d85 = json.loads(lines[84])
print(f"Line 85 heading: {d85['heading']}")
print(f"Line 85 text: {d85['text'][:80]}")

# Line 86 (index 85): Contains actual para 81 content
d86 = json.loads(lines[85])
old_h86 = d86['heading']
d86['heading'] = "81. Duty of Officers at all levels to take note of previous discussions and orders while dealing with references.-"
lines[85] = json.dumps(d86, ensure_ascii=False) + '\n'
print(f"\nLine 86: '{old_h86}' -> '{d86['heading']}'")

# Line 87 (index 86): Contains 81.A + 81.B text with wrong heading
d87 = json.loads(lines[86])
old_h87 = d87['heading']
d87['heading'] = "81.A. Oral instructions by higher officers.-"
lines[86] = json.dumps(d87, ensure_ascii=False) + '\n'
print(f"Line 87: '{old_h87}' -> '{d87['heading']}'")

# Line 85 is a stray fragment. Its text "C. Confirmation of oral Instructions" 
# is just a section divider that belongs to 81.C (line 88). 
# Remove the truncated heading since this chunk is a fragment
d85['heading'] = "81."
d85['text'] = "C. Confirmation of oral Instructions"
lines[84] = json.dumps(d85, ensure_ascii=False) + '\n'
print(f"Line 85: kept as fragment with heading '81.'")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print("\nDone!")
