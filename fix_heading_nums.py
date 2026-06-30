"""
Fix heading numbers that got lost when we extracted text and replaced the heading.
The heading text was replaced with the found text line, losing the X.Y prefix.
"""
import json
import re

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

def extract_heading_num(heading):
    if not heading: return None
    m = re.match(r'^(\d+(?:\.\d+)?)', heading.strip())
    return m.group(1) if m else None

user_seq = {
    '1': ['1', '1.1', '1.2', '1.3', '1.4'],
    '2': ['1', '2', '3', '3.1', '3.2', '4', '5', '6', '7', '7.1', '7.2', '7.3'],
    '3': ['1', '2', '2.1', '2.2', '2.3', '3', '3.1', '3.2', '3.3', '4', '5', '5.1', '5.2', '5.3', '6', '7', '8', '9', '9.1', '9.2', '9.3', '9.4', '9.5', '9.6', '9.7', '9.8', '9.9', '9.10'],
    '4': ['1', '2', '3', '3.1', '3.2', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14'],
    '5': ['1', '2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20'],
    '6': ['1', '2', '2.1', '2.2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '7.24', '7.25', '7.26', '7.27', '7.28', '7.29', '7.30', '7.31', '7.32', '7.33', '7.34', '7.35', '7.36', '7.37', '7.38', '7.39'],
    '7': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17'],
    '8': ['1', '2', '2.1', '2.2', '2.3', '2.4', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '8'],
    '9': ['1', '1.1', '1.2', '2', '2.1', '2.2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '6.4', '6.5', '6.6', '6.7', '7', '7.1', '7.2', '7.3', '8', '8.1', '8.2', '8.3'],
    '10': ['1', '2', '2.1', '2.2', '2.3', '2.4', '2.5', '3', '4', '5', '5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10', '5.11', '5.12', '5.13', '5.14', '5.15'],
    '11': ['1', '2', '2.1', '2.2', '2.3', '2.4', '3', '3.1', '3.2', '3.3', '4', '5', '5.1', '5.2', '5.3', '6', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '8', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '8.10', '8.11', '8.12', '8.13'],
    '12': ['1', '1.1', '2', '2.1', '2.2', '2.3', '2.4', '3', '3.1', '3.2', '3.3', '3.4', '4', '5', '6', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '7.24', '7.25', '8'],
    '13': ['1', '2', '3', '4'],
    '14': ['1', '2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '6.1', '6.2', '6.3', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21'],
    '15': ['1', '2', '2.1', '2.2', '2.3', '3', '3.1', '3.2', '3.3', '3.4', '4', '4.1', '4.2', '4.3', '4.4', '4.5', '4.6', '5', '5.1', '5.2', '6', '7', '7.1', '7.2', '7.3'],
    '16': ['1', '2', '3', '3.1', '3.2', '3.3', '4', '5', '6', '7', '7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '8'],
    '17': ['1', '2', '3', '4', '5', '6', '6.1', '7', '8'],
    '18': ['1', '2', '3', '4', '5', '6', '7', '7.1', '7.2'],
    '19': ['1', '2', '3', '3.1', '3.2', '4', '5', '6'],
    '20': ['1', '2', '3', '4', '5', '5.1', '5.2'],
    '21': ['1', '2', '3', '4', '5', '6', '7', '8', '8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '8.10', '8.11', '8.12', '8.13', '8.14', '8.15', '8.16', '8.17', '8.18', '8.19', '8.20', '8.21', '8.22', '8.23', '8.24'],
    '22': ['1', '2', '2.1', '2.2', '3', '4', '5', '5.1', '5.2', '6', '7', '8']
}

# For each chapter, check if heading numbers match
# If a heading doesn't start with the expected number, prepend it
fixed = 0
for ch_num in sorted(user_seq.keys(), key=int):
    expected = user_seq[ch_num]
    ch_chunks = [(i, c) for i, c in enumerate(chunks) if c.get('chapter') == ch_num]
    
    if len(ch_chunks) != len(expected):
        print(f"Ch {ch_num}: chunk count {len(ch_chunks)} != expected {len(expected)}")
        continue
    
    for j, (idx, chunk) in enumerate(ch_chunks):
        expected_num = expected[j]
        actual_num = extract_heading_num(chunk.get('heading', ''))
        
        if actual_num != expected_num:
            heading = chunk.get('heading', '')
            # The heading text lost its number prefix
            # Add the expected number prefix
            if heading and not heading.startswith(expected_num):
                # Check if heading already has a different number
                if actual_num:
                    # Replace the wrong number
                    new_heading = re.sub(r'^\d+\.?\d*\.?\s*', expected_num + ' ', heading)
                else:
                    # Prepend the number
                    new_heading = expected_num + ' ' + heading
                chunks[idx]['heading'] = new_heading
                print(f"  Ch {ch_num}: Fixed heading '{heading}' -> '{new_heading}'")
                fixed += 1

# Write back
with open(INPUT_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"\nFixed {fixed} heading numbers")

# Verify
print("\n=== Verification ===")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

all_ok = True
for ch_num in sorted(user_seq.keys(), key=int):
    expected = user_seq[ch_num]
    actual = [extract_heading_num(c.get('heading', '')) for c in chunks if c.get('chapter') == ch_num]
    if expected == actual:
        print(f"  Ch {ch_num}: OK ({len(actual)} chunks)")
    else:
        all_ok = False
        missing = [h for h in expected if h not in actual]
        extra = [h for h in actual if h and h not in expected]
        print(f"  Ch {ch_num}: WRONG")
        if missing: print(f"    Missing: {missing}")
        if extra: print(f"    Extra: {extra}")

if all_ok:
    print("\n=== ALL CHAPTERS VERIFIED ===")
