import json

with open('parsed_toc.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)
    
val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]
    
for c in chunks:
    ch = str(c['chapter'])
    para = c['para']
    for t in toc.get(ch, []):
        if t['para'] == para:
            # Reconstruct the original heading string that fix_alignment_lfad_v4.py expects
            c['heading'] = f"Para {para} - {t['title']}"
            break

with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')
