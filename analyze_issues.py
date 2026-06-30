import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

# 1. Find split words (e.g., "representa Tion", "enterpr Ise")
# Pattern: Lowercase letter, space, Uppercase letter, lowercase letters
split_word_pattern = re.compile(r'([a-z])\s([A-Z][a-z]+)')

split_words = set()
for c in chunks:
    # Check heading
    heading = c.get('heading', '')
    for match in split_word_pattern.finditer(heading):
        word = match.group(0)
        split_words.add(word)
        
    text = c.get('text', '')
    for match in split_word_pattern.finditer(text):
        word = match.group(0)
        # Filter out common legitimate sequences like "a Book" or "the Railway"
        # We want things where the parts don't make sense as separate words.
        # But wait, in English "is The", "a Car" match this pattern.
        # So we should only look at words in the heading, or specific known ones.
        pass

print("Split words found in headings:")
for w in sorted(list(split_words)):
    print(w)

print("\nChecking chunks 480 to 510 for heading vs text mismatch...")
for i in range(480, 510):
    c = chunks[i]
    print(f"Index {i} | Ch {c['chapter']} | Heading: {c['heading']} | Text starts: {c['text'][:50]}")
