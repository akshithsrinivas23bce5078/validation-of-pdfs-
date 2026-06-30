import json
import re
import os

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
output_path = file_path + '.tmp'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changed = 0

# A list of para numbers where the text acts as the grammar subject of the sentence.
# We DO NOT want to strip the heading from the text here.
subject_paras = {
    23, 43, 44, 77, 131, 5, 16, 20, 60, 4, 8, 64, 71, 72, 76, 91, 110, 61, 62, 51, 27, 11, 33
}

def normalize(s):
    # Remove all non-alphanumeric characters and extra spaces to make comparison robust
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

for i in range(len(lines)):
    data = json.loads(lines[i])
    t = data.get('text', '').strip()
    h = data.get('heading', '')
    p = data.get('para', 0)
    
    if p in subject_paras:
        continue
        
    original_t = t
    
    # 1. Strip para numbers like "85 ) " or "85."
    t = re.sub(rf'^{p}\s*[\)\.\-]*\s*', '', t, flags=re.IGNORECASE).strip()
    
    # 2. Extract core heading
    core_heading = re.sub(r'^Para\s+\d+\s*-\s*', '', h, flags=re.IGNORECASE).strip()
    
    # 3. Aggressively strip the core heading from the beginning of the text
    # Since text might have slight variations, let's extract the first N words of the text
    # and compare it against the core heading.
    
    if core_heading:
        # Create a regex pattern from the core heading that allows optional whitespace/punctuation between words
        words = re.findall(r'[a-zA-Z0-9]+', core_heading)
        if words:
            # Build pattern: word1[^\w]*word2[^\w]*...
            pattern_str = r'^[^\w]*' + r'[^\w]*'.join([re.escape(w) for w in words]) + r'[^\w]*'
            
            # Find match at the start
            match = re.match(pattern_str, t, flags=re.IGNORECASE)
            if match:
                t = t[match.end():].strip()
                # Check for remaining stray punctuation or bullets
                t = re.sub(r'^[:;\-\.\)_]+\s*', '', t).strip()

    if t != original_t:
        data['text'] = t
        lines[i] = json.dumps(data, ensure_ascii=False) + '\n'
        changed += 1
        print(f"Para {p}:")
        print(f"  Old: {original_t[:60]}...")
        print(f"  New: {t[:60]}...\n")

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(lines)
    
os.replace(output_path, file_path)
print(f"Total aggressive heading strips: {changed}")
