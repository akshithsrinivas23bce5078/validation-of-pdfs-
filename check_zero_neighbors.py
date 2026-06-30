import json

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for i, c in enumerate(chunks):
    if len(c.get('text', '')) == 0:
        print(f"Index {i}: {c['heading']}")
        
        # Look at the chunks before and after
        if i > 0:
            print(f"  Prev: {chunks[i-1]['heading']} (len={len(chunks[i-1].get('text',''))})")
        print(f"  Curr: {c['heading']} (len={len(c.get('text',''))})")
        if i < len(chunks)-1:
            print(f"  Next: {chunks[i+1]['heading']} (len={len(chunks[i+1].get('text',''))})")
        print()
