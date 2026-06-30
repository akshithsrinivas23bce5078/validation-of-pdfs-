import json
import fitz
import re

pdf_path = r"assigned pdfs\Secretariat Office Manual.pdf"
jsonl_path = r"chunks after validation\SECRETARIAT_OFFICE_MANUAL_validated.jsonl"
unval_path = r"unvalidated chunks\Secretariat_Office_Manual_chunks.jsonl"

def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

# 1. Process PDF
pdf = fitz.open(pdf_path)
pdf_text = ""
for page in pdf:
    pdf_text += page.get_text() + " "
    
pdf_words = count_words(pdf_text)

# 2. Process Validated JSONL
with open(jsonl_path, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
    
jsonl_text = ""
exact_headings_count = 0
empty_headings_count = 0
tables_count = sum([c['has_table'] for c in chunks])

for c in chunks:
    # combine heading and text for coverage
    jsonl_text += c.get('heading', '') + " " + c.get('text', '') + " "
    
    if c.get('heading', '').strip():
        exact_headings_count += 1
    else:
        empty_headings_count += 1

jsonl_words = count_words(jsonl_text)

# 3. Process Unvalidated JSONL
with open(unval_path, "r", encoding="utf-8") as f:
    unval_chunks = [json.loads(line) for line in f if line.strip()]

coverage_percentage = (jsonl_words / pdf_words) * 100 if pdf_words > 0 else 0

report = {
    "pdf_words": pdf_words,
    "jsonl_words": jsonl_words,
    "coverage_percentage": round(coverage_percentage, 2),
    "total_unvalidated_chunks": len(unval_chunks),
    "total_validated_chunks": len(chunks),
    "chunks_merged": len(unval_chunks) - len(chunks),
    "exact_headings_count": exact_headings_count,
    "empty_headings_count": empty_headings_count,
    "tables_injected": tables_count
}

print(json.dumps(report, indent=2))
