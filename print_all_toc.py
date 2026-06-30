import json

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

vals = list(toc.values())
for i, v in enumerate(vals):
    print(f"{i}: {v}")
