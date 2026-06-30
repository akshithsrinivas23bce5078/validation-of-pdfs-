import json

with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for d in data:
    heading = str(d.get('heading', ''))
    text = str(d.get('text', ''))[:100].replace('\n', ' ')
    print(f"{d.get('chapter', '')} - {heading}: {text}")
