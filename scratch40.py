"""
Fix the MAJOR mismatch: Line 97 has "90.A 90. Current File.-" which incorrectly merges
two headings. Per the PDF:
  - Para 90: "90. Current File.-"
  - Para 90.A: The brown sheet wrapper instruction
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix Line 97 (index 96): "90.A 90. Current File.-" -> "90. Current File.-"
d = json.loads(lines[96])
old_h = d['heading']
d['heading'] = "90. Current File.-"
lines[96] = json.dumps(d, ensure_ascii=False) + '\n'
print(f"Line 97: '{old_h}' -> '{d['heading']}'")

# Fix Line 98 (index 97): heading should be "90.A" not the full brown sheet text
d2 = json.loads(lines[97])
old_h2 = d2['heading']
d2['heading'] = '90.A.'
lines[97] = json.dumps(d2, ensure_ascii=False) + '\n'
print(f"Line 98: '{old_h2[:60]}...' -> '{d2['heading']}'")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print("\nDone!")
