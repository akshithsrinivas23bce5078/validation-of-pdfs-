import json
import os
import glob

folder_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation'
jsonl_files = glob.glob(os.path.join(folder_path, '*.jsonl'))

replacements = {
    '\u2018': "'",  # Left single quote
    '\u2019': "'",  # Right single quote
    '\u201c': '"',  # Left double quote
    '\u201d': '"',  # Right double quote
    '\u2013': '-',  # En dash
    '\u2014': '-',  # Em dash
    '\u2022': '*',  # Bullet
    '\u00a0': ' ',  # Non-breaking space
    '\u00ad': '-',  # Soft hyphen
    '\u2026': '...', # Ellipsis
}

def clean_text(text):
    if not isinstance(text, str):
        return text
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def clean_dict(d):
    new_d = {}
    for k, v in d.items():
        if isinstance(v, str):
            new_d[k] = clean_text(v)
        elif isinstance(v, dict):
            new_d[k] = clean_dict(v)
        elif isinstance(v, list):
            new_list = []
            for item in v:
                if isinstance(item, str):
                    new_list.append(clean_text(item))
                elif isinstance(item, dict):
                    new_list.append(clean_dict(item))
                else:
                    new_list.append(item)
            new_d[k] = new_list
        else:
            new_d[k] = v
    return new_d

total_files_processed = 0
total_chunks_processed = 0

for filepath in jsonl_files:
    print(f"Processing {os.path.basename(filepath)}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    cleaned_chunks = []
    for line in lines:
        if not line.strip():
            continue
        try:
            chunk = json.loads(line)
            cleaned_chunks.append(clean_dict(chunk))
            total_chunks_processed += 1
        except Exception as e:
            print(f"Error parsing line in {os.path.basename(filepath)}: {e}")
            
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        for chunk in cleaned_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
            
    total_files_processed += 1

print(f"\nSuccessfully processed {total_files_processed} files and {total_chunks_processed} chunks.")
