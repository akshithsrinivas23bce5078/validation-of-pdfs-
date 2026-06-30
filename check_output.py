import json, re

with open(r"chunks after validation\RAM_2022_Sixth_Edition.jsonl", encoding="utf-8") as f:
    chunks = [json.loads(l) for l in f]

print(f"Total chunks: {len(chunks)}\n")

print("=== Chapter 1 headings (all 17) ===")
for i, c in enumerate(chunks, 1):
    if c["chapter"] == "1":
        numbered = "[NUM]" if re.match(r'^\d+\.', c['heading']) else "     "
        table_flag = "[TABLE]" if c['has_table'] else "      "
        print(f"  [{i:>3}] {numbered} {table_flag} pg={c['page.no']:<10} {c['heading']}")

print()
print("=== Chapter 2 headings (all 13) ===")
for i, c in enumerate(chunks, 1):
    if c["chapter"] == "2":
        numbered = "[NUM]" if re.match(r'^\d+\.', c['heading']) else "     "
        print(f"  [{i:>3}] {numbered} pg={c['page.no']:<10} {c['heading']}")

print()
numbered_all = sum(1 for c in chunks if re.match(r'^\d+\.', c['heading']))
print(f"Total chunks with numbered headings (x. or x.x): {numbered_all}")
print(f"Total chunks: {len(chunks)}")
print(f"Chunks with has_table=True: {sum(1 for c in chunks if c['has_table'])}")
