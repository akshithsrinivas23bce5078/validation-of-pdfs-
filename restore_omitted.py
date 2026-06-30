import json
import re

unval_file = r"unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl"
orig_texts = {}
with open(unval_file, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip(): continue
        c = json.loads(line)
        para_no = str(c.get('para_no', '')).strip()
        m = re.match(r'^(\d{1,3})', para_no)
        if m:
            num = m.group(1)
            if num not in orig_texts:
                orig_texts[num] = c.get('text', '').strip()

val_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(val_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

restored_count = 0
for c in chunks:
    if c.get('text', '') == ' ':
        h = c.get('heading', '').strip()
        m = re.match(r'^(\d{1,3})', h)
        if m:
            para_num = m.group(1)
            if para_num in orig_texts:
                c['text'] = orig_texts[para_num]
                restored_count += 1

with open(val_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Restored text for {restored_count} omitted chunks.")
