import json
from collections import Counter

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TAMIL_NADU_MINISTERIAL_SERVICE_RULES.jsonl'
sections = Counter()
rule_nos = set()
with open(filepath, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        c = json.loads(line)
        sections[c.get('section')] += 1
        rule_nos.add(c.get('rule_no'))

print("Sections:", sections)
print("Total Chunks:", sum(sections.values()))
print("Rule numbers:", sorted(list(rule_nos)))
