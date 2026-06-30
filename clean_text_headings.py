import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"

with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

updated_chunks = []
modified_count = 0

for c in chunks:
    heading = c.get("heading", "").strip()
    text = c.get("text", "").strip()
    
    # Check if omitted text
    if "Omitted" in text or "omitted" in text:
        # Keep as is
        updated_chunks.append(c)
        continue
    
    if heading and text.startswith(heading):
        # Remove heading from text
        new_text = text[len(heading):]
        # Strip leading punctuation like . — -
        # Using regex to remove leading spaces, dots, em-dashes, en-dashes, hyphens
        new_text = re.sub(r'^[\s\.\—\-\–]+', '', new_text)
        
        c["text"] = new_text
        modified_count += 1
    else:
        # Try a more lenient match: maybe heading without the trailing dot matches the start
        h_no_dot = heading.rstrip('.')
        if h_no_dot and text.startswith(h_no_dot):
            new_text = text[len(h_no_dot):]
            new_text = re.sub(r'^[\s\.\—\-\–]+', '', new_text)
            c["text"] = new_text
            modified_count += 1

    updated_chunks.append(c)

with open(filepath, "w", encoding="utf-8") as f:
    for c in updated_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Modified {modified_count} chunks. Omitted texts were skipped.")
