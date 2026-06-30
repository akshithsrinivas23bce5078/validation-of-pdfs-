import json
with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)
keys = list(toc.keys())
for i in range(len(keys)-30, len(keys)):
    print(keys[i])
