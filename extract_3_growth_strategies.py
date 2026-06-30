import json

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

new_chunks = []
for c in chunks:
    if "3.1 Overall Fiscal strategy" in c["heading"] or "3.1" in c["heading"]:
        text = c["text"]
        
        # In the PDF, "3. Growth Strategies" appears before "3.1 Overall fiscal strategy"
        split_marker = "3.1 Overall fiscal strategy"
        
        # Sometimes case might vary in the extracted text
        split_marker_lower = split_marker.lower()
        text_lower = text.lower()
        
        if split_marker_lower in text_lower:
            split_idx = text_lower.find(split_marker_lower)
            
            # Text before the marker is "3. Growth Strategies"
            part_growth = text[:split_idx].strip()
            # Text after the marker is "3.1 Overall fiscal strategy"
            part_3_1 = text[split_idx:].strip()
            
            # Remove "3. Growth Strategies" from the start of part_growth if it exists,
            # so we don't duplicate it in the text since we'll set it as heading?
            # Actually, the user wants the text according to the PDF.
            
            # Create new chunk for 3. Growth Strategies
            c_growth = c.copy()
            c_growth["heading"] = "3. Growth Strategies"
            c_growth["text"] = part_growth
            c_growth["has_table"] = False # No table in this small intro
            c_growth["table_html"] = {}
            new_chunks.append(c_growth)
            
            # Keep the existing table in 3.1 if it exists
            c["text"] = part_3_1
            new_chunks.append(c)
        else:
            print("WARNING: Could not find split marker for 3.1!")
            new_chunks.append(c)
    else:
        new_chunks.append(c)

with open(filepath, "w", encoding="utf-8") as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print(f"Successfully separated 3. Growth Strategies. New total chunks: {len(new_chunks)}")
