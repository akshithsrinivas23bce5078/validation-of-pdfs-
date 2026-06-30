import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# Find index of "532. Casual leave and Restricted Holidays."
target_idx = -1
for i, c in enumerate(chunks):
    if c["heading"].startswith("532. Casual leave"):
        target_idx = i
        break

if target_idx != -1:
    target_chunk = chunks[target_idx]
    festivals_text = []
    
    # We need to grab the next 34 chunks and merge them
    # Let's verify they are the festivals
    end_idx = target_idx + 1
    while end_idx < len(chunks):
        h = chunks[end_idx]["heading"]
        # Check if heading starts with a number 1 to 34 and is a festival
        # If it hits 533, we stop.
        if h.startswith("533."):
            break
        
        # Append the heading (since it has the festival name) 
        festivals_text.append(h)
        end_idx += 1
        
    # Append the festivals text to target chunk
    if festivals_text:
        target_chunk["text"] += " " + " ".join(festivals_text)
        
        # Update page numbers if needed
        # We assume the pages are simple strings like "(295)"
        pages = set([target_chunk.get("page.no", "").strip("()")] + 
                    [chunks[i].get("page.no", "").strip("()") for i in range(target_idx + 1, end_idx)])
        pages = [p for p in pages if p]
        if len(pages) > 1:
            target_chunk["page.no"] = f"({min(pages)}-{max(pages)})"
            
        # Delete the festival chunks
        del chunks[target_idx + 1 : end_idx]
        
    with open(filepath, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + '\n')
            
    print(f"Merged {len(festivals_text)} festival chunks into chunk 532.")
else:
    print("Chunk 532 not found.")
