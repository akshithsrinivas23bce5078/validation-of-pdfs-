import json

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

new_chunks = []
for c in chunks:
    if "3.8 Strategic initiative #7:" in c["heading"] or "3.8" in c["heading"]:
        text = c["text"]
        
        split_3_9 = "3.9 Strategic initiative 8: Care for the vulnerable sections of society"
        split_3_10 = "3.10 Strategic initiative 9: Signature projects"
        
        if split_3_9 in text and split_3_10 in text:
            part_8, rest = text.split(split_3_9)
            part_9, part_10 = rest.split(split_3_10)
            
            # Update 3.8
            c["text"] = part_8.strip()
            new_chunks.append(c)
            
            # Create 3.9
            c_9 = c.copy()
            c_9["heading"] = "3.9 Strategic initiative 8: Care for the vulnerable sections of society"
            c_9["text"] = split_3_9 + " " + part_9.strip()
            new_chunks.append(c_9)
            
            # Create 3.10
            c_10 = c.copy()
            c_10["heading"] = "3.10 Strategic initiative 9: Signature projects"
            c_10["text"] = split_3_10 + " " + part_10.strip()
            new_chunks.append(c_10)
        else:
            print("WARNING: Could not find split strings in text!")
            new_chunks.append(c)
    else:
        new_chunks.append(c)

with open(filepath, "w", encoding="utf-8") as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print(f"Successfully split 3.8. New total chunks: {len(new_chunks)}")
