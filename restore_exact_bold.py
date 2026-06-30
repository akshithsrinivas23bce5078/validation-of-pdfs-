import json
import re

with open("exact_bold_headings.json", "r", encoding="utf-8") as f:
    bold_headings = json.load(f)

validated_file = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
with open(validated_file, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

restored = 0
for c in chunks:
    t = c.get('text', '').strip()
    m = re.match(r'^(\d{1,3})\.', t)
    if m:
        para_num = m.group(1)
        if para_num in bold_headings:
            exact_h = bold_headings[para_num]
            # Some cleaning on exact_h
            # The PDF sometimes extracts with extra spaces or different dashes
            # Let's clean both exact_h and t
            exact_h_clean = re.sub(r'\s+', ' ', exact_h).replace('\u2014', '-').replace('\u2015', '-').strip()
            # If exact_h ends with ".-", it might just be "." in exact_h_clean
            
            # Remove trailing dash from exact_h if present, since we want to handle the dash separately
            exact_h_clean = re.sub(r'[\.\-\s]+$', '', exact_h_clean)
            
            # Let's find how much of t to strip
            t_clean = re.sub(r'\s+', ' ', t).replace('\u2014', '-').replace('\u2015', '-').strip()
            
            if t_clean.startswith(exact_h_clean):
                # We need to find the boundary in the original t string!
                # Instead of trying to slice the original based on the cleaned length,
                # let's just use regex to match the exact_h dynamically.
                
                # build a regex pattern from exact_h
                words = re.split(r'\s+', exact_h.strip())
                pattern_str = r'\s*[\.\-\u2014\u2015]*\s*'.join([re.escape(w.strip('.-')) for w in words if w.strip('.-')])
                pattern_str = r'^' + pattern_str + r'\s*[\.\-\u2014\u2015]*\s*'
                
                m2 = re.match(pattern_str, t, re.IGNORECASE)
                if m2:
                    h_part = m2.group(0).strip()
                    c['heading'] = h_part
                    c['text'] = t[m2.end():].strip()
                    restored += 1
                else:
                    # fallback
                    c['heading'] = exact_h
                    c['text'] = t
            else:
                c['heading'] = exact_h
                c['text'] = t
        else:
            c['heading'] = " "
    else:
        c['heading'] = " "

with open(validated_file, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Restored {restored} bold headings using exact PDF matching.")
