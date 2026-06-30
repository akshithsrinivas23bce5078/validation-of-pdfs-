import json
import re

filepath = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\Chapter 1_2.jsonl'
with open(filepath, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f if line.strip()]

# The missing x.y headers from the PDF
missing_headers = {
    "1.2": "1.2 BASIC CONSIDERATIONS OF O&M",
    "1.3": "1.3 OUTLINES OF O&M",
    "1.4": "1.4 ORGANIZATION OF O&M",
    "1.5": "1.5 COMMUNITY AWARENESS AND PARTICIPATION",
    "1.6": "1.6 POTENTIAL RISK WITH RESPECT TO SEWERAGE SYSTEM",
    "1.7": "1.7 SEWERAGE LEDGER",
    "1.8": "1.8 BUDGET ESTIMATION FOR O&M",
    "1.9": "1.9 SUMMARY",
    "1.10": "1.10 RELATIONSHIP BETWEEN PART-A (ENGINEERING), PART-B (OPERATION AND MAINTENANCE), AND PART-C (MANAGEMENT) OF MANUAL"
}

new_chunks = []
current_parent_chunk = None
current_parent_prefix = None

def get_prefix(heading):
    m = re.match(r'^(\d+\.\d+)', heading)
    if m: return m.group(1)
    return None

def is_xyz(heading):
    return bool(re.match(r'^\d+\.\d+\.\d+', heading))

for c in chunks:
    heading = c.get('heading', '')
    
    # E.g. heading is "1.2.1 Laws..."
    if is_xyz(heading):
        prefix = get_prefix(heading) # "1.2"
        
        # If we are not already building this parent chunk, start it
        if current_parent_prefix != prefix:
            if current_parent_chunk:
                new_chunks.append(current_parent_chunk)
            
            current_parent_prefix = prefix
            
            # Initialize new parent chunk
            current_parent_chunk = c.copy()
            current_parent_chunk['heading'] = missing_headers.get(prefix, f"{prefix} MISSING HEADER")
            # Text starts with the child's heading + text
            current_parent_chunk['text'] = f"{heading}\n{c.get('text', '')}"
            
        else:
            # We are already building the parent, just append text
            current_parent_chunk['text'] += f"\n\n{heading}\n{c.get('text', '')}"
            
    else:
        # It's an x.y heading or top level like INTRODUCTION or 1.1
        # E.g. "1.1 NEED FOR O&M" or "1.7 SEWERAGE LEDGER"
        
        prefix = get_prefix(heading) if re.match(r'^\d+\.\d+\s', heading) else heading
        
        if current_parent_prefix == prefix and current_parent_chunk is not None:
            # This happens if there's a 1.7 chunk then 1.7.1 chunk
            # But wait, in the array 1.7 comes first!
            # If a parent chunk comes BEFORE children, my logic would see it here, set it as current,
            # then the children would fall into `is_xyz` and match the prefix!
            pass 
        
        # Actually, let's just handle it properly.
        if current_parent_chunk:
            new_chunks.append(current_parent_chunk)
            current_parent_chunk = None
            current_parent_prefix = None
            
        # Is it a parent that has children coming up? Like 1.7 SEWERAGE LEDGER
        if re.match(r'^\d+\.\d+', heading):
            current_parent_prefix = get_prefix(heading)
            current_parent_chunk = c.copy()
            # If the heading in JSONL is incomplete like "1.10 RELATIONSHIP BETWEEN PART-A (ENGINEERING), PART-B (OPERATION AND", 
            # we should fix it with missing_headers
            fixed_heading = missing_headers.get(current_parent_prefix, heading)
            current_parent_chunk['heading'] = fixed_heading
            
            # If it had text, keep it. Wait, the 1.10 had text split?
            # 1.10 text starts with "MAINTENANCE), AND PART-C (MANAGEMENT) OF MANUAL The present manual..."
            # That's because the heading was split. We need to merge that text.
            if current_parent_prefix == "1.10" and heading != fixed_heading:
                # the actual heading got split into text
                # We fixed the heading, now we just keep the text as is.
                pass
                
        else:
            # Top level, like "INTRODUCTION"
            new_chunks.append(c)

# Append last chunk
if current_parent_chunk:
    new_chunks.append(current_parent_chunk)

with open(filepath, 'w', encoding='utf-8') as f:
    for c in new_chunks:
        f.write(json.dumps(c, ensure_ascii=True) + '\n')

print(f"Merged into {len(new_chunks)} chunks.")
