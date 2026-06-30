import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# Manual replacements for the remaining 11 chunks
manual_fixes = {
    ('1', 5): r'^\s*5\.\s*AUDIT IN THE O/O THE ASSISTANT DIRECTORS OF LF AUDIT\.\s*',
    ('2', 3): r'^\s*3\.\s*THE EXISTING POSITION OF MUNICIPALITIES \(GRADEWISE\) IS AS FOLLOWS\.\s*',
    ('2', 33): None, # "planning section..." - doesn't have a heading to remove at the start.
    ('2', 64): r'^\s*64\.\s*PRELIMINARY:-\s*',
    ('2', 115): r'^\s*115\)\s*EXECUTION OF WORKS-:\s*',
    ('4', 7): r'^\s*7\.\s*Application of Resources\s*',
    ('4', 23): r'^\s*23\.\s*Other Remunerative Enterprises:\s*', # Wait, Para 23 heading is "Statutory government grants" but text says "Other Remunerative Enterprises". Let's just strip "23. Other Remunerative Enterprises:"
    ('4', 32): r'^\s*32\.\s*\(Central Government\)\s*-\s*Member of Parliament Local Area Development Scheme\s*',
    ('4', 37): r'^\s*37\.\s*Appointment\s*',
    ('4', 91): r'^\s*91\.\s*Inaugural functions and foundations stone laying functions to:\s*',
    ('4', 111): r'^\s*111\.\s*Pass Book-\s*'
}

for c in chunks:
    key = (str(c['chapter']), c['para'])
    if key in manual_fixes:
        pattern = manual_fixes[key]
        if pattern:
            c['text'] = re.sub(pattern, '', c['text']).strip()

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Manual fixes applied.")
