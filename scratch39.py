"""
Third pass: Manual corrections for 21 remaining heading issues.
Based on PDF inspection, some headings have full bold titles (need completing),
while others only have the number bold (should revert to bare number).
"""
import json
import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

# Corrections based on PDF bold text inspection
# Format: line_number (1-indexed) -> correct heading
corrections = {
    # Headings with actual bold titles - complete them
    48:  "48. Numbering of arising references and papers received by section without current number.-",
    60:  "60. Entry in column 5 of current sent by one officer through one or more other officers.-",
    92:  "92. Need to record year in addition to date and month in Notes, Drafts, etc.-",
    109: "109. Reading of previous correspondence at the head of an Order.-",
    110: "110. Method of Communication of General rulings and Orders on particular cases in the same draft.-",
    269: "269. Printing in half-margin not ordinarily to be resorted to.-",
    503: "503. Subsidiary Cash Book - Maintenance of.-",
    
    # Headings where ONLY the number is bold in the PDF (no title)
    # These were incorrectly given body text as titles - revert to bare number
    141: "141.",
    209: "209.",
    246: "246.",
    251: "251.",
    252: "252.",
    254: "254.",
    260: "260.",
    297: "297.",
    318: "318.",
    334: "334.",
    347: "347.",
    433: "433.",
    496: "496.",
    570: "570.",
}

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed = 0
for i in range(len(lines)):
    d = json.loads(lines[i])
    h = d.get('heading', '').strip()
    
    # Extract para number
    m = re.match(r'^\*?(\d+)[\.\s]', h)
    if not m:
        continue
    para_num = int(m.group(1))
    
    if para_num in corrections:
        new_h = corrections[para_num]
        if h != new_h:
            old_h = h
            d['heading'] = new_h
            lines[i] = json.dumps(d, ensure_ascii=False) + '\n'
            print(f"  Line {i+1}: '{old_h}' -> '{new_h}'")
            fixed += 1
            # Remove from dict to avoid duplicate application
            del corrections[para_num]

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)

os.replace(output_path, jsonl_path)
print(f"\nTotal fixed: {fixed}")
