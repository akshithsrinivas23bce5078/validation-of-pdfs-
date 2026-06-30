import json

lines = [json.loads(l) for l in open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', encoding='utf-8')]

prev_ch = None
for c in lines[:50]:
    ch = c['chapter']
    if ch != prev_ch:
        print(f"=== CHAPTER {ch} ===")
        prev_ch = ch
    print(f"  {c['heading']}")
