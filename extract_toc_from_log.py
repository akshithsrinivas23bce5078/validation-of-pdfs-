import re
import json

log_path = r"C:\Users\Akshith Srinivas\.gemini\antigravity-ide\brain\27e840ff-ce64-4110-a71f-b85f4d9a5a62\.system_generated\tasks\task-34.log"

toc_items = []
with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Pattern to catch lines like: "Page 2: [10.0 Calibri] 1. BACKGROUND ................................................................................................................................ 1"
    # or "Page 2: [9.0 Calibri] 2.1.1" followed by "History of Railway Audit"
    m = re.match(r'^Page \d+: \[\d+\.\d+ .*?\] (.*?)$', line.strip())
    if m:
        text = m.group(1).strip()
        if re.match(r'^\d+(\.\d+)*$', text): # just numbers
            # Look ahead for the title
            next_m = re.match(r'^Page \d+: \[\d+\.\d+ .*?\] (.*?)$', lines[i+1].strip())
            if next_m:
                title = next_m.group(1).split('.......')[0].strip()
                toc_items.append(f"{text} {title}")
        elif re.match(r'^\d+(\.\d+)*\s+', text):
            # numbers and title on the same line
            clean_text = text.split('.......')[0].strip()
            # remove page number at the end if any
            clean_text = re.sub(r'\s+\d+$', '', clean_text).strip()
            toc_items.append(clean_text)

with open(r"C:\Users\Akshith Srinivas\chunk-validator-one\ram_toc_from_log.txt", "w", encoding="utf-8") as f:
    for t in toc_items:
        f.write(t + "\n")
