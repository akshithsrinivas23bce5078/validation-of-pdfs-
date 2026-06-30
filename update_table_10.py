import json
filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 10_0.jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    if c["heading"] == "10.3 MAINTAINING ON-SITE FACILITIES":
        c["has_table"] = True
        c["table_html"] = {"Table 10.1": "<table border='1'><tr><th>Table 10.1 Key pathogens contained in excreta and sludge</th></tr></table>"}
        print("Updated 10.3 to have has_table=True and valid table_html dictionary!")

with open(filepath, "w", encoding="utf-8") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")
