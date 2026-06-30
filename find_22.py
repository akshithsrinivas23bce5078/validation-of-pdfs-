import json, re
with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    chunks = json.load(f)
text_22 = ''
for c in chunks:
    ch = str(c.get('chapter', ''))
    if ch == '22' or 'E-Office' in str(c.get('title', '')):
        text_22 += c.get('text', '') + '\n'

search_terms = [
    "INTRODUCTION",
    "ENTERPRISE-WIDE",
    "EMPOWERING THE",
    "WEB-BASED SOLUTION",
    "FUNCTIONALITIES",
    "COMPLIANCE AUDIT",
    "EVALUATION OF",
    "ADEQUACY OF"
]

for t in search_terms:
    idx = text_22.upper().find(t)
    if idx != -1:
        print(f"Found {t} at {idx}")
    else:
        print(f"MISSING {t}")
