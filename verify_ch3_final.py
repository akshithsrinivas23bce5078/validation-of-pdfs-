import json
import re

val_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(val_path, 'r', encoding='utf-8') as f:
    val_chunks = [json.loads(line) for line in f]

ch3 = [c for c in val_chunks if str(c['chapter']) == '3']
print(f"Total Chapter 3 chunks: {len(ch3)}")
print(f"Para range: {ch3[0]['para']} to {ch3[-1]['para']}")
print()

issues = []
for c in ch3:
    text = c['text']
    para = c['para']
    heading = c['heading']
    
    if '-' in heading:
        title_part = heading.split('-', 1)[1].strip()
    else:
        title_part = heading
    
    title_words = [w for w in re.split(r'\W+', title_part) if len(w) >= 4]
    
    # Check 1: Text should start with the paragraph number
    starts_with_num = re.match(r'\s*' + re.escape(str(para)) + r'\b', text)
    
    # Check 2: At least one title word should appear in the first 120 chars
    first_120 = text[:120].upper()
    has_title = any(w.upper() in first_120 for w in title_words) if title_words else True
    
    # Check 3: Text should not be empty
    is_empty = len(text.strip()) < 10
    
    status = "OK"
    if not starts_with_num:
        status = "BAD START"
        issues.append(f"Para {para}: doesn't start with para number")
    elif not has_title:
        status = "TITLE MISSING"
        issues.append(f"Para {para}: title word not in first 120 chars")
    elif is_empty:
        status = "EMPTY"
        issues.append(f"Para {para}: too short")
    
    print(f"[{status:>14}] Para {para:>2}: {text[:70]}")

print(f"\n{'='*50}")
print(f"Issues found: {len(issues)}")
for i in issues:
    print(f"  {i}")
