import json
import re

filepath = r"c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl"
with open(filepath, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    heading = c['heading']
    text = c['text']
    
    # Let's search for the heading directly
    if heading.lower() in text.lower():
        idx = text.lower().find(heading.lower())
        snippet = text[max(0, idx-30):min(len(text), idx+len(heading)+50)]
        print(f"Heading [{heading}] FOUND exactly:\n...{snippet}...\n")
    else:
        # Try finding the chapter number
        match = re.search(r'^(\d+(\.\d+)?)', heading)
        if match:
            num = match.group(1)
            # Find the number in text
            idx = text.find(num)
            if idx != -1:
                snippet = text[max(0, idx-10):min(len(text), idx+100)]
                print(f"Heading [{heading}] NOT EXACT, but found number '{num}':\n...{snippet}...\n")
            else:
                print(f"Heading [{heading}] NOT FOUND AT ALL in text.\n")
        else:
            print(f"Heading [{heading}] NOT FOUND AT ALL in text.\n")
