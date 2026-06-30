import json
import re

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

# Let's map headings to correct chapters
# We will just print the headings with their index to manually map them
vals = list(toc.values())
for i, v in enumerate(vals):
    if v.startswith('1. '):
        print(f"Index {i}: {v}")
