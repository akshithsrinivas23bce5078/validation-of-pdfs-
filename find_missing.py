import json

with open('unvalidated chunks/TNGS_ClassXII_chunks.jsonl', 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]
    
for c in chunks:
    text = c.get('text', '')
    if 'Tenure' in text or 'Savings' in text or 'Appointment:-' in text:
        head = c.get('heading', '')
        if head: head = head[:40]
        print(f"CH={c.get('chapter')} PAGE={c.get('page.no')} HEADING={head} TEXT={text[:60]}".encode('utf-8', 'ignore').decode('utf-8', 'ignore'))
