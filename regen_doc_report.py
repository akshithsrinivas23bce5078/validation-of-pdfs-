import json

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

report = []
report.append('# Final Doc_ID & DOC_NAME Validation Report')
report.append('\n| Chunk Index | DOC_NAME | Heading | Unique Doc ID |')
report.append('|---|---|---|---|')

for i, c in enumerate(chunks):
    report.append(f"| {i+1} | {c['DOC_NAME']} | {c['heading']} | `{c['doc_id']}` |")

with open(r'C:\Users\Akshith Srinivas\.gemini\antigravity-ide\brain\cee9d04a-5045-4770-8e3c-ca872b2eb43b\doc_id_validation_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print("Regenerated the doc_id report!")
