import json
import re

def clean_text(t):
    return re.sub(r'\s+', ' ', t).strip()

def chunk_page_to_int(p_str):
    nums = re.findall(r'\d+', str(p_str))
    return int(nums[0]) if nums else 0

def merge_texts(t1, t2):
    if not t1: return t2
    if not t2: return t1
    
    max_len = min(len(t1), len(t2), 300)
    # Check exact match
    for i in range(max_len, 20, -1):
        if t1[-i:] == t2[:i]:
            return t1 + t2[i:]
            
    # Check match ignoring whitespace
    for i in range(max_len, 20, -1):
        if t1[-i:].replace(' ','') == t2[:i].replace(' ',''):
            return t1 + t2[i:]
            
    return t1 + ' ' + t2

with open('parsed_toc.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

input_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated.jsonl'
with open(input_path, 'r', encoding='utf-8') as f:
    raw_chunks = [json.loads(line) for line in f]

merged_chunks = []
global_doc_id = "LFAD-CABFE45CDA"

for ch in ['1', '2', '3', '4']:
    c_chunks = [c for c in raw_chunks if str(c['chapter']) == ch]
    paras = toc[ch]
    
    if not paras:
        continue
        
    current_para_idx = 0
    current_merged = {
        "DOC_NAME": "Local Fund Audit Depart Manual Vol - II",
        "doc_id": global_doc_id,
        "chapter": ch,
        "title": c_chunks[0]['title'] if c_chunks else f"Chapter {ch}",
        "heading": f"Para {paras[current_para_idx]['para']} - {paras[current_para_idx]['title']}",
        "text": "",
        "page_no": f"({paras[current_para_idx]['page']})",
        "has_table": False,
        "table_html": ""
    }
    
    current_text = ""
    
    for c in c_chunks:
        c_page = chunk_page_to_int(c['page_no'])
        c_text = c['text']
        c_heading = c['heading']
        
        # Check if we should transition to the next paragraph
        transition = False
        if current_para_idx + 1 < len(paras):
            next_p = paras[current_para_idx + 1]
            next_page = next_p['page']
            
            if c_page > next_page:
                transition = True
            elif c_page == next_page:
                para_num_str = str(next_p['para'])
                if re.match(r'^' + para_num_str + r'[\.\)\s]', c_heading, re.IGNORECASE) or \
                   re.search(r'Para\s*-?\s*' + para_num_str, c_heading, re.IGNORECASE):
                    transition = True
                else:
                    if re.match(r'^' + para_num_str + r'[\.\)\s]', c_text, re.IGNORECASE):
                        transition = True
                        
        if transition:
            current_merged["text"] = current_text.strip()
            merged_chunks.append(current_merged)
            
            current_para_idx += 1
            current_text = ""
            
            # In case we skipped multiple paragraphs
            while current_para_idx + 1 < len(paras) and c_page > paras[current_para_idx + 1]['page']:
                empty_para = {
                    "DOC_NAME": "Local Fund Audit Depart Manual Vol - II",
                    "doc_id": global_doc_id,
                    "chapter": ch,
                    "title": c_chunks[0]['title'] if c_chunks else f"Chapter {ch}",
                    "heading": f"Para {paras[current_para_idx]['para']} - {paras[current_para_idx]['title']}",
                    "text": "",
                    "page_no": f"({paras[current_para_idx]['page']})",
                    "has_table": False,
                    "table_html": ""
                }
                merged_chunks.append(empty_para)
                current_para_idx += 1
                
            current_merged = {
                "DOC_NAME": "Local Fund Audit Depart Manual Vol - II",
                "doc_id": global_doc_id,
                "chapter": ch,
                "title": c_chunks[0]['title'] if c_chunks else f"Chapter {ch}",
                "heading": f"Para {paras[current_para_idx]['para']} - {paras[current_para_idx]['title']}",
                "text": "",
                "page_no": f"({paras[current_para_idx]['page']})",
                "has_table": c['has_table'],
                "table_html": c['table_html'] if c['has_table'] else ""
            }
            
        current_text = merge_texts(current_text, c_text)
        if c.get('has_table'):
            current_merged['has_table'] = True
            current_merged['table_html'] += "\n" + c['table_html']
            
    # Append the last one
    current_merged["text"] = current_text.strip()
    merged_chunks.append(current_merged)
    
    current_para_idx += 1
    while current_para_idx < len(paras):
        empty_para = {
            "DOC_NAME": "Local Fund Audit Depart Manual Vol - II",
            "doc_id": global_doc_id,
            "chapter": ch,
            "title": c_chunks[0]['title'] if c_chunks else f"Chapter {ch}",
            "heading": f"Para {paras[current_para_idx]['para']} - {paras[current_para_idx]['title']}",
            "text": "",
            "page_no": f"({paras[current_para_idx]['page']})",
            "has_table": False,
            "table_html": ""
        }
        merged_chunks.append(empty_para)
        current_para_idx += 1

output_path = r'chunks after validation\Local Fund Audit Depart Manual  Vol - II_validated_paragraphs.jsonl'
with open(output_path, 'w', encoding='utf-8') as f:
    for c in merged_chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

print(f"Total merged chunks: {len(merged_chunks)}")

for ch in ['1', '2', '3', '4']:
    count = len([c for c in merged_chunks if c['chapter'] == ch])
    print(f"Chapter {ch}: {count} chunks")
