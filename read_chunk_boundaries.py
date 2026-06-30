import json

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks[:20]):
    print(f"Chunk {i}: start_page={c.get('start_page')}, end_page={c.get('end_page')}")

print("\nLast 20 chunks:")
for i, c in enumerate(chunks[-20:]):
    print(f"Chunk {len(chunks)-20+i}: start_page={c.get('start_page')}, end_page={c.get('end_page')}")
