"""
Split chunk 86 (which contains both 81.A and 81.B text) into two separate chunks.
Clean the embedded headings out of the text.
"""
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

d87 = json.loads(lines[86])
text = d87['text']

# Split the text into 81.A and 81.B parts
part_A = text.split("C. Confirmation of oral Instructions 81.B. Oral Orders on behalf of or from Ministers")[0]
part_B = text.split("C. Confirmation of oral Instructions 81.B. Oral Orders on behalf of or from Ministers")[1]

# Clean part A (remove the embedded heading)
part_A = part_A.replace("C. Confirmation of oral Instructions 81.A. Oral instructions by higher officers ", "").strip()
part_B = part_B.strip()

# Update 81.A chunk (lines[86])
d87['heading'] = "81.A. Oral instructions by higher officers.-"
d87['text'] = part_A
lines[86] = json.dumps(d87, ensure_ascii=False) + '\n'

# Create new 81.B chunk
d87_B = dict(d87)
d87_B['heading'] = "81.B. Oral Orders on behalf of or from Ministers.-"
d87_B['text'] = part_B
# d87_B will be inserted right after 81.A

lines.insert(87, json.dumps(d87_B, ensure_ascii=False) + '\n')

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print("Successfully split 81.A and 81.B into separate chunks and cleaned the text.")
