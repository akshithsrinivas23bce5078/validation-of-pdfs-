import json

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

fails = [('1',5), ('2',3), ('2',33), ('2',64), ('2',115), ('4',7), ('4',23), ('4',32), ('4',37), ('4',91), ('4',111)]

for c in chunks:
    if (str(c['chapter']), c['para']) in fails:
        print(f"Ch{c['chapter']} Para {c['para']}:")
        print(f"  H: {c['heading']}")
        print(f"  T: {c['text'][:150]}\n")
