import json
import re

valid_chunks=[]
for l in open(r'unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl', encoding='utf-8'):
    if not l.strip(): continue
    c = json.loads(l)
    para_no = str(c.get('para_no', '')).strip()
    para_title = str(c.get('para_title', '')).strip()
    if para_no and para_title: c['heading'] = f"{para_no}. {para_title}"
    elif para_no: c['heading'] = f"{para_no}."
    else: c['heading'] = para_title
    valid_chunks.append(c)

last_para_num = 0
for c in valid_chunks:
    heading = c.get('heading', '').strip()
    m = re.match(r'^(\d{1,3})(?:\w)?[\.\s]', heading)
    if m:
        num = int(m.group(1))
        if num == 575:
            print('Found 575! last_para_num is', last_para_num)
        
        # Here is the logic from merge_all_subchunks.py:
        if num >= last_para_num and num <= last_para_num + 15:
            last_para_num = num
        else:
            if num == 575:
                print('575 FAILED the check! last_para_num:', last_para_num, 'num:', num)
