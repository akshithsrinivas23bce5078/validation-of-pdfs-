import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

removed_count = 0
failed = []

for c in chunks:
    heading = c['heading']
    text = c['text']
    
    # Extract the title part from heading (after "Para X - ")
    title_part = heading
    m = re.match(r'Para\s+\d+\s*[-–—]\s*', heading)
    if m:
        title_part = heading[m.end():]
    
    if not title_part or len(title_part.strip()) < 3:
        failed.append((c['chapter'], c['para'], heading, "Title too short"))
        continue
    
    # Get significant words from the title (3+ chars, alphanumeric only)
    title_words = re.findall(r'[A-Za-z]{3,}', title_part)
    if not title_words:
        failed.append((c['chapter'], c['para'], heading, "No title words"))
        continue
    
    # The text typically starts with patterns like:
    # "7. PROFESSION TAX: ..."
    # "Para . 4 : AUDIT FUNCTIONS OF ASSISTANT DIRECTORS:- ..."
    # "1. GENESIS OF THE DEPARTMENT:- ..."
    # "2) GENERAL PRINCIPLES OF AUDIT ..."
    
    # Strategy: Try to find the LAST title word in the first 300 chars of text.
    # Everything up to and including that word (plus trailing punctuation) is the "heading" to remove.
    
    search_area = text[:400]
    
    # Find the last title word's position in the search area
    last_word = title_words[-1]
    
    # Search case-insensitively for the last title word
    pattern = re.compile(re.escape(last_word), re.IGNORECASE)
    matches = list(pattern.finditer(search_area))
    
    if not matches:
        # Try with fewer words
        for tw in reversed(title_words[:-1]):
            matches = list(re.compile(re.escape(tw), re.IGNORECASE).finditer(search_area))
            if matches:
                break
    
    if not matches:
        failed.append((c['chapter'], c['para'], heading, "Last title word not found in text"))
        continue
    
    # Use the FIRST occurrence of the last title word
    last_match = matches[0]
    end_pos = last_match.end()
    
    # But verify that MOST title words appear before this position
    # (to avoid matching a random occurrence deep in the body)
    text_before = search_area[:end_pos].upper()
    words_found = sum(1 for w in title_words if w.upper() in text_before)
    
    if words_found < len(title_words) * 0.5:
        # Less than half the title words found before this point — likely wrong match
        failed.append((c['chapter'], c['para'], heading, f"Only {words_found}/{len(title_words)} words found"))
        continue
    
    # Skip trailing punctuation/whitespace after the heading (like ":- ", ": ", ".- ", etc.)
    remaining = text[end_pos:]
    strip_match = re.match(r'^[\s:;\-–—.,/()]*', remaining)
    if strip_match:
        end_pos += strip_match.end()
    
    new_text = text[end_pos:].strip()
    
    if new_text and len(new_text) > 10:
        c['text'] = new_text
        removed_count += 1
    else:
        failed.append((c['chapter'], c['para'], heading, f"Resulting text too short ({len(new_text)} chars)"))

print(f"Removed heading from text in {removed_count} out of {len(chunks)} chunks.")
print(f"Failed: {len(failed)}")

if failed:
    print("\n=== FAILED CHUNKS ===")
    for ch, para, heading, reason in failed:
        print(f"  Ch{ch} Para {para}: {heading} -> {reason}")

# Preview
print("\n=== PREVIEW (first 10 chunks) ===\n")
for c in chunks[:10]:
    print(f"HEADING: {c['heading']}")
    print(f"TEXT:    {c['text'][:120]}")
    print()

# Save
with open(val_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print("Saved.")
