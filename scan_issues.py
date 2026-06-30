import json
import re

with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Maintenance manual of WAG-9 vol. III_PDA West Central Rai.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(l) for l in f]

KNOWN_BAD = [
    r'TheWA G-9',
    r'Com pressor',
    r'Indian Railways WAG-9',
    r'Indian Railways\s*$',
    r'\(4\}',
    r'Reservoirs\s*$',
    r"'l,",
    r'C603\d{3}',
    r"pipe'",
    r'\{3\)',
    r'r- - -',
    r'IQ\]',
    r'0804',
    r've hicle',
    r'locomo tive',
    r'stan dards',
]

print('REMAINING ISSUES:')
found = 0
for i, c in enumerate(chunks, 1):
    text = c['text']
    issues = []
    for pat in KNOWN_BAD:
        m = re.search(pat, text)
        if m:
            start = max(0, m.start()-25)
            end = min(len(text), m.end()+25)
            issues.append(f'  [{pat}]: ...{repr(text[start:end])}...')
    if issues:
        found += 1
        print(f'Chunk {i} ({c["heading"]}):')
        for iss in issues:
            print(iss)

print(f'\nTotal chunks with remaining issues: {found}')
