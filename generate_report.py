import json
import collections

input_file = "chunks after validation/TNGS_ClassXII_validated.jsonl"

def generate_report():
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return

    total_chunks = len(lines)
    valid_chunks = 0
    errors = []
    
    chapter_counts = collections.Counter()
    headings_by_chapter = collections.defaultdict(list)
    table_count = 0
    
    expected_keys = ["DOC_NAME", "doc_id", "chapter", "title", "heading", "text", "page.no", "has_table", "table_html"]

    for i, line in enumerate(lines):
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"Line {i+1}: Invalid JSON.")
            continue
            
        # Check key order
        keys = list(chunk.keys())
        if keys != expected_keys:
            errors.append(f"Line {i+1}: Incorrect key order or missing keys. Expected {expected_keys}, got {keys}")
            
        # Check empty values
        for k in ["DOC_NAME", "doc_id", "chapter", "title", "heading", "text"]:
            if not chunk.get(k):
                errors.append(f"Line {i+1}: Field '{k}' is empty.")
                
        chapter = chunk.get("chapter", "UNKNOWN")
        heading = chunk.get("heading", "UNKNOWN")
        
        chapter_counts[chapter] += 1
        headings_by_chapter[chapter].append(heading)
        
        if chunk.get("has_table") is True:
            table_count += 1
            if not chunk.get("table_html") or chunk.get("table_html") == "{}":
                errors.append(f"Line {i+1}: has_table is true but table_html is empty.")
                
        valid_chunks += 1

    # Format the report
    report = []
    report.append("# Validation Report: TNGS_ClassXII_validated.jsonl\n")
    report.append("## Overview")
    report.append(f"- **Total Chunks**: {total_chunks}")
    report.append(f"- **Valid JSON Chunks**: {valid_chunks}")
    report.append(f"- **Chunks with Tables**: {table_count}")
    report.append(f"- **Errors Found**: {len(errors)}")
    
    report.append("\n## Schema Validation")
    if not errors:
        report.append("✅ All chunks conform to the expected schema and key order:")
        report.append("`[\"DOC_NAME\", \"doc_id\", \"chapter\", \"title\", \"heading\", \"text\", \"page.no\", \"has_table\", \"table_html\"]`")
    else:
        report.append("❌ Errors:")
        for e in errors[:10]:
            report.append(f"  - {e}")
        if len(errors) > 10:
            report.append(f"  - ... and {len(errors) - 10} more.")
            
    report.append("\n## Content Breakdown by Chapter")
    for chapter in sorted(chapter_counts.keys()):
        report.append(f"### {chapter} ({chapter_counts[chapter]} chunks)")
        for h in headings_by_chapter[chapter]:
            report.append(f"- {h}")

    print("\n".join(report))

generate_report()
