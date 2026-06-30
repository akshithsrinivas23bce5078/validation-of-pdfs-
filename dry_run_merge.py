import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

last_para_num = 0
current_main = None

sub_chunks_found = []

for c in chunks:
    heading = c['heading'].strip()
    m = re.match(r'^(\d{1,3})(?:\w)?[\.\s]', heading)
    
    is_main = False
    
    if m:
        num = int(m.group(1))
        # Allow gaps of up to 10 just in case some paras were omitted/skipped
        if num >= last_para_num and num <= last_para_num + 15:
            last_para_num = num
            is_main = True
    
    if is_main:
        current_main = c
    else:
        if current_main:
            sub_chunks_found.append({
                "parent": current_main['heading'],
                "sub": heading
            })
        else:
            # If there's no main chunk yet, it might be the very first few chunks (e.g. chapter title). 
            # In SOM, the first real para is 1. Introduction.
            print("Found sub-chunk before any main chunk:", heading)

print(f"Total sub-chunks identified: {len(sub_chunks_found)}")

# Group by parent
from collections import defaultdict
grouped = defaultdict(list)
for item in sub_chunks_found:
    grouped[item["parent"]].append(item["sub"])

for parent, subs in list(grouped.items())[:10]:
    print(f"\nParent: {parent}")
    for s in subs[:5]:
        print(f"  - {s}")
    if len(subs) > 5:
        print(f"  ... and {len(subs)-5} more")
        
print("\nSome other parents:", list(grouped.keys())[-10:])
