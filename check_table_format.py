import json
filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 2_1.jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c.get("has_table"):
        print("Chunk " + c["heading"] + " table_html type: " + str(type(c["table_html"])))
        print(str(c["table_html"])[:100])
        break
