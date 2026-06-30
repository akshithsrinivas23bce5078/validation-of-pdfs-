import json
with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)
for k, v in toc.items():
    if k >= "400":
        print(f"Index {k}: {v}")
