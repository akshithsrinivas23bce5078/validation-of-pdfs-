"""
Post-fix verification: Re-compare PDF vs JSONL headings after the first pass.
Focus on remaining issues and headings that got truncated badly.
"""
import json
import sys
import re
import fitz

sys.stdout.reconfigure(encoding='utf-8')

pdf_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\assigned pdfs\The Secretariat Office Manual.pdf'
jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'

# Read JSONL headings
with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find headings that are still problematic
issues = []
for i, line in enumerate(lines):
    d = json.loads(line)
    h = d.get('heading', '').strip()
    
    # Check for issues:
    # 1. Heading ending with ".-" right after a comma or preposition (truncated mid-sentence)
    if re.search(r'\b(of|the|in|to|a|an|on|by|or|and|for|from)\.-$', h):
        issues.append((i+1, 'TRUNCATED', h))
    # 2. Heading is just "N.-" (bare with no title at all)
    elif re.match(r'^\*?\d+(?:\.\w+)?\.-$', h):
        issues.append((i+1, 'BARE', h))
    # 3. Heading has doubled period-dash: ",.—" patterns
    elif ',.-' in h or ',.—' in h:
        issues.append((i+1, 'BAD_ENDING', h))

print(f"Found {len(issues)} remaining issues:")
for line_num, issue_type, heading in issues:
    print(f"  Line {line_num} [{issue_type}]: {heading}")
