import json
import random
import string

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\TN_Vision_2023(PHASE 1).jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

doc_id = "TNV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

new_chunk = {
    "DOC_NAME": "TN_Vision_2023(PHASE 1).pdf",
    "doc_id": doc_id,
    "chapter": "2",
    "title": "Key outcomes of the Vision",
    "heading": "2. Key outcomes of the Vision",
    "text": "This section describes the key outcomes (themes) that the Vision envisages to attain. Each theme is a goal in itself and is also entwined with other themes, and they have to be pursued together in unison to realise the overall vision.",
    "page.no": "(29)",
    "has_table": False,
    "table_html": {}
}

chunks.insert(1, new_chunk)

with open(filepath, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=True) + "\n")

print(f"Successfully inserted '2. Key outcomes of the Vision' with doc_id {doc_id} at index 1!")
