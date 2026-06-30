"""
Split Para 18 into multiple chunks for each definition.
"""
import json
import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

jsonl_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\The Secretariat Office Manual.jsonl'
output_path = jsonl_path + '.tmp'

with open(jsonl_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Para 18 is at index 17
d18 = json.loads(lines[17])
text = d18['text']

# List of definitions to split by (in order of appearance)
split_points = [
    "Arising reference.",
    "*Branch",
    "Business Rules",
    "Case",
    "Circulation.",
    "Current.",
    "Current file",
    "Demi-official correspondence.",
    "Department",
    "Disposal",
    "Drafting",
    "Enclosure.",
    "Flagging",
    "Foreign despatch",
    "General despatch",
    "Issue",
    "Linked case.",
    "New case.",
    "Note.",
    "Note file",
    "Official correspondence.",
    "Old case.",
    "Put-up papers",
    "Referencing",
    "Registry.",
    "Routine note.",
    "Secretariat is",
    "Secretariat instructions",
    "Section is",
    "Sectional notes",
    "Tappal.",
    "Unofficial correspondence.",
    "$e-Office.",
    "$Digital Signature."
]

# We need a robust way to find these split points in the text because of potential unicode characters like '—'
# Let's find the exact indices of these split points
indices = []
for sp in split_points:
    # Use regex to find the split point, allowing for unicode dashes or spaces after it
    # We'll just look for the text
    pattern = re.escape(sp)
    match = re.search(pattern, text)
    if match:
        indices.append((match.start(), sp))
    else:
        print(f"WARNING: Could not find '{sp}' in text")

# Ensure indices are sorted
indices.sort(key=lambda x: x[0])

# Add the end of text as the final index
indices.append((len(text), "END"))

chunks_to_insert = []

# The introductory text before the first definition
intro_text = text[:indices[0][0]].strip()
intro_text = intro_text.replace("Garveen of Mohideen Abdul Khader. of", "The following are").strip()
d18['text'] = intro_text
d18['heading'] = "18."
chunks_to_insert.append(d18)

# Create chunks for each definition
for i in range(len(indices) - 1):
    start_idx = indices[i][0]
    end_idx = indices[i+1][0]
    
    term_text = text[start_idx:end_idx].strip()
    
    # We want the heading to be "18. [Term].-"
    term_name = indices[i][1]
    
    # Clean up the term name for heading
    clean_term = term_name
    if clean_term.endswith("."):
        clean_term = clean_term[:-1]
    if clean_term.endswith(" is"):
        clean_term = clean_term[:-3]
    
    heading = f"18. {clean_term}.-"
    
    new_chunk = dict(d18)
    new_chunk['heading'] = heading
    new_chunk['text'] = term_text
    chunks_to_insert.append(new_chunk)

# Replace line 17 with the new chunks
new_lines = lines[:17]
for chunk in chunks_to_insert:
    new_lines.append(json.dumps(chunk, ensure_ascii=False) + '\n')
new_lines.extend(lines[18:])

with open(output_path, 'w', encoding='utf-8') as fout:
    fout.writelines(new_lines)

os.replace(output_path, jsonl_path)
print(f"Successfully split Para 18 into {len(chunks_to_insert)} separate definition chunks.")
