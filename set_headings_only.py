import json
import re

with open("exact_bold_headings.json", "r", encoding="utf-8") as f:
    bold_headings = json.load(f)

validated_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(validated_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    # First, let's fix headings that have the word 'omitted'
    t = c.get('text', '').strip()
    
    m = re.match(r'^(\d{1,3})\.', t)
    if m:
        para_num = m.group(1)
        if para_num in bold_headings:
            exact_h = bold_headings[para_num]
            c['heading'] = exact_h
            # DO NOT TOUCH THE TEXT FIELD!
        else:
            c['heading'] = " "
    else:
        # Some chunks might not start with a number.
        # Check the current heading
        h = c.get('heading', '').strip()
        m_h = re.match(r'^(\d{1,3})\.', h)
        if m_h:
            para_num = m_h.group(1)
            if para_num in bold_headings:
                c['heading'] = bold_headings[para_num]
            else:
                c['heading'] = " "
        else:
            c['heading'] = " "
            
    # Also apply the 'omitted' rule that we had before
    h = c.get('heading', '').strip()
    if 'omitted' in h.lower() or 'omitted' in t.lower()[:50]:
        c['text'] = " "

with open(validated_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Updated headings successfully.")
