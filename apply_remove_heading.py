import json
import re
import shutil

def clean_alpha(text):
    return re.sub(r'[^a-zA-Z]', '', text).lower()

def remove_heading_prefix(heading, text):
    original_text = text
    head_alpha = clean_alpha(heading)
    
    # 1. Look for common delimiters within the first 150 characters
    match = re.search(r'^(.+?)(?:\.\-|:\-|\.\-\-|\:|\n)(.*)', text, re.DOTALL)
    if match:
        prefix = match.group(1).strip()
        rest = match.group(2).lstrip('.-: \n\t❖')
        
        pref_alpha = clean_alpha(prefix)
        
        # Special check for "7. Tenure..."
        if head_alpha.startswith('tenure') or 'tenure' in pref_alpha:
            if 'tenure' in pref_alpha:
                return rest

        # Check if they are somewhat similar.
        if pref_alpha and head_alpha and (pref_alpha in head_alpha or head_alpha in pref_alpha):
            return rest
            
        # Also check if pref_alpha contains the first main word of heading
        first_word = re.sub(r'^\d+[A-Z]*\.\s*', '', heading).strip().split()
        if first_word:
            first_word_alpha = clean_alpha(first_word[0])
            if first_word_alpha and first_word_alpha in pref_alpha and len(prefix) < 150:
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
        
    # 5. Fallback: find the delimiter and if the prefix has heading words
    match = re.match(r'^(.*?)(?:\.\-|:\-|\.\-\-)(.*)', text, re.DOTALL)
    if match:
        prefix = match.group(1).strip()
        rest = match.group(2).lstrip('.-: \n\t❖')
        pref_words = set(re.findall(r'\w+', prefix.lower()))
        head_words = set(re.findall(r'\w+', heading.lower()))
        if len(pref_words.intersection(head_words)) >= 1 and len(prefix) < 100:
            return rest
            
    return original_text

input_file = 'chunks after validation/TNGS_ClassXII_validated.jsonl'
backup_file = 'chunks after validation/TNGS_ClassXII_validated.jsonl.bak'
shutil.copy2(input_file, backup_file)

with open(input_file, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

for c in chunks:
    heading = c.get('heading')
    text = c.get('text')
    c['text'] = remove_heading_prefix(heading, text)

# Write back in desired order
with open(input_file, 'w', encoding='utf-8') as f:
    for c in chunks:
        ordered_c = {
            "DOC_NAME": c.get("DOC_NAME"),
            "doc_id": c.get("doc_id"),
            "chapter": c.get("chapter"),
            "title": c.get("title"),
            "heading": c.get("heading"),
            "text": c.get("text"),
            "page.no": c.get("page.no"),
            "has_table": c.get("has_table"),
            "table_html": c.get("table_html")
        }
        f.write(json.dumps(ordered_c, ensure_ascii=False) + '\n')

print(f"Successfully processed {len(chunks)} chunks and removed headings from text.")
