import json
import re

def clean_alpha(text):
    return re.sub(r'[^a-zA-Z]', '', text).lower()

def remove_heading_prefix(heading, text):
    original_text = text
    head_alpha = clean_alpha(heading)
    
    # 1. Look for common delimiters within the first 150 characters
    # Delimiters: '.-', ':-', '.--', ':', '\n'
    match = re.search(r'^(.+?)(?:\.\-|:\-|\.\-\-|\:|\n)(.*)', text, re.DOTALL)
    if match:
        prefix = match.group(1).strip()
        rest = match.group(2).lstrip('.-: \n\t❖')
        
        pref_alpha = clean_alpha(prefix)
        
        # Special check for "7. Tenure..." since it's very long and prefix is short
        if head_alpha.startswith('tenure') or 'tenure' in pref_alpha:
            if 'tenure' in pref_alpha:
                return rest

        # Check if they are somewhat similar.
        # If pref_alpha is a substring of head_alpha or vice versa, it's a match.
        # Allow some flexibility, e.g. "appointment" vs "iappointment"
        if pref_alpha and head_alpha and (pref_alpha in head_alpha or head_alpha in pref_alpha):
            return rest
            
        # Also check if pref_alpha contains the first main word of heading
        first_word = re.sub(r'^\d+[A-Z]*\.\s*', '', heading).strip().split()
        if first_word:
            first_word_alpha = clean_alpha(first_word[0])
            if first_word_alpha and first_word_alpha in pref_alpha and len(prefix) < 150:
                 # Check if the rest of the text looks like actual content (not empty)
                 if rest:
                     return rest

    # 2. Check if text starts with the heading itself
    if text.lower().startswith(heading.lower()):
        return text[len(heading):].lstrip('.-: \n\t❖')
        
    # 3. Check if text starts with the clean heading (without numbers)
    clean_heading = re.sub(r'^\d+[A-Z]*\.\s*', '', heading).strip()
    if text.lower().startswith(clean_heading.lower()):
        return text[len(clean_heading):].lstrip('.-: \n\t❖')

    # 4. Check for specific known prefixes
    if heading == "2. Appointment" and text.startswith("(i) Appointment:-"):
        return text[len("(i) Appointment:-"):].lstrip('.-: \n\t❖')
        
    # 5. Fallback: just find the delimiter and if the prefix has heading words, remove it
    match = re.match(r'^(.*?)(?:\.\-|:\-|\.\-\-)(.*)', text, re.DOTALL)
    if match:
        prefix = match.group(1).strip()
        rest = match.group(2).lstrip('.-: \n\t❖')
        pref_words = set(re.findall(r'\w+', prefix.lower()))
        head_words = set(re.findall(r'\w+', heading.lower()))
        # if there is a good overlap
        if len(pref_words.intersection(head_words)) >= 1 and len(prefix) < 100:
            return rest
            
    return original_text

with open('chunks after validation/TNGS_ClassXII_validated.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for i, c in enumerate(chunks[:20]):
    heading = c.get('heading')
    text = c.get('text')
    new_text = remove_heading_prefix(heading, text)
    print(f"--- Chunk {i} ---")
    print(f"Heading: {heading}")
    print(f"Old text: {text[:80].replace('\n', ' ')}")
    print(f"New text: {new_text[:80].replace('\n', ' ')}")
    if new_text == text:
        print("  *** NO CHANGE ***")
