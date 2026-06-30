import json
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for c in chunks:
    h = c['heading']
    # If it's like "1.1. MAKING OF RAM" -> we want "1.1 MAKING OF RAM"
    # Wait, the format in my script was `f"{num}. {toc_title}"`
    # So if `num` was `1.1`, it became `1.1. MAKING OF RAM`
    parts = h.split(' ', 1)
    if len(parts) == 2:
        num_part = parts[0]
        # if num_part is "1.1.", remove the trailing dot
        if num_part.count('.') > 1 and num_part.endswith('.'):
            new_num = num_part[:-1]
            c['heading'] = f"{new_num} {parts[1]}"

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
