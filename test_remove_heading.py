import json
import re

with open(r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl', encoding='utf-8') as f:
    chunks = [json.loads(x) for x in f]

for i, c in enumerate(chunks[485:490]):
    text = c['text']
    heading = c['heading']
    
    # Create a regex to match the heading at the start of the text
    # We split heading into words and join with \s+
    words = re.split(r'\s+', heading.strip())
    # Escape words to avoid regex special char issues
    escaped_words = [re.escape(w) for w in words]
    pattern = r'^[\s]*' + r'[\s]+'.join(escaped_words) + r'[\s]*'
    
    new_text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    print(f"--- Chunk {485+i} ---")
    print(f"HEADING: {heading}")
    print(f"OLD TEXT: {repr(text[:100])}")
    print(f"NEW TEXT: {repr(new_text[:100])}")
