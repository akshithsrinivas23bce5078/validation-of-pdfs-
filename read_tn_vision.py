import json
import os

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\unvalidated chunks\TN_Vision_2023(PHASE 1).jsonl"
if not os.path.exists(filepath):
    print("File not found:", filepath)
else:
    with open(filepath, "r", encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f if line.strip()]

    print(f"Total chunks: {len(chunks)}")
    for i, c in enumerate(chunks[:30]):
        print(f"Chunk {i}: chapter={c.get('chapter')} | title={c.get('title')} | heading={c.get('heading')}")
