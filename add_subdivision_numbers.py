import json

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben.jsonl'
output_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\17__Introduction_Accounting_Manual_Part_1_Wes_State_Audit_West_Ben_numbered.jsonl'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

current_chapter = None
sub_id = 1
last_heading_original = None
last_heading_numbered = None

for c in chunks:
    chapter = c.get('chapter')
    heading = c.get('heading')
    
    # Reset sub_id if chapter changes
    if chapter != current_chapter:
        current_chapter = chapter
        sub_id = 1
        last_heading_original = None
        last_heading_numbered = None

    if heading is not None:
        if heading != last_heading_original:
            # New heading in this chapter
            last_heading_original = heading
            prefix = f"{chapter}.{sub_id} "
            
            # Check if heading already starts with the prefix (e.g. 2.1 ) to avoid double prefixing
            if heading.startswith(prefix):
                last_heading_numbered = heading
            else:
                last_heading_numbered = prefix + heading
            
            sub_id += 1
        
        # Apply the numbered heading
        c['heading'] = last_heading_numbered

with open(output_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Processed {len(chunks)} chunks and added subdivision numbers.")
