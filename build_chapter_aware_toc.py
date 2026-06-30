"""
build_chapter_aware_toc.py
Generates a chapter_toc.json: { "2": [...headings...], "3": [...], ... }
by grouping the flat toc_mapping.json by chapter boundaries.

The toc_mapping.json is organized by chapter order (Chapter 1 headings come first,
then Chapter 2, etc.). We identify chapter boundaries by detecting the first
"1. Something" heading that follows a chapter transition.
"""
import json
import re

toc = json.load(open('toc_mapping.json', encoding='utf-8'))

# Chapter title keywords that signal start of each chapter
# These are the "1. Brief About..." style headings that appear at the top of each chapter
CHAPTER_ANCHORS = [
    # Ch1 starts with "1. Background"
    ("1", "BACKGROUND"),
    # Ch2 starts with "1. Brief On General Administration..."
    ("2", "BRIEFONGENERALADMINISTRATIONANDVIGILANCEDEPARTMENTOFRAILWAY"),
    # Ch3 starts with "1. Brief About The Accounts Department"
    ("3", "BRIEFABOUTTHEACCOUNTSDEPARTMENT"),
    # Ch4 starts with "1. Brief About The Department" (Personnel)
    ("4", "BRIEFABOUTTHEDEPARTMENT"),
    # Ch5 starts at "2. Organisation Hierarchy Of Medical Department"  
    ("5", "ORGANISATIONHIERARCHYOFMEDICALDEPARTMENT"),
    # Ch6 starts at "2. Organisational Structure Of Civil Engineering Department"
    ("6", "ORGANISATIONALSTRUCTUREOFCIVILENGINEERINGDEPARTMENT"),
    # Ch7: "1. Preparation And Approval Of Drawings And Estimates"
    ("7", "PREPARATIONANDAPPROVALOFDRAWINGSANDESTIMATES"),
    # Ch8: "1. About The Department" (Commercial)
    ("8", "ABOUTTHEDEPARTMENT"),
    # Ch9: "1. Introduct Ion" (Operating)
    ("9", "INTRODUCTION"),
    # Ch10: "2. Organisation Hierarchy Of Electrical Engineering Department"
    ("10", "ORGANISATIONHIERARCHYOFELECTRICALENGINEERINGDEPARTMENT"),
    # Ch11: "1. Brief About Signal & Telecommunication Department"
    ("11", "BRIEFABOUTSIGNALTELECOMMUNICATIONDEPARTMENT"),
    # Ch12: "2. Organisational Setup Of Mechanical Engineering Department"
    ("12", "ORGANISATIONALSETUPOFMECHANICALENGINEERINGDEPARTMENT"),
    # Ch13: "1. Brief About The Production Units"
    ("13", "BRIEFABOUTTHEPRODUCTIONUNITS"),
    # Ch14: "2. Organisation Hierarchy Of Stores Department"
    ("14", "ORGANISATIONHIERARCHYOFSTOREDEPARTMENT"),
    # Ch15: "2. Organisational Hirarchy" (Safety)
    ("15", "ORGANISATIONALHIRARCHY"),
    # Ch16: "2. Organisation Hierarchy Of Security Department"
    ("16", "ORGANISATIONHIERARCHYOFSECURITYDEPARTMENT"),
    # Ch17: "1. Introduc Tion" (CRIS)
    ("17", "INTRODUC TION"),
    # Ch18: "2. Organisation Hierarchy Of RLDA"
    ("18", "ORGANISATIONHIERARCHYOFRLDA"),
    # Ch19: "1. Introduction" (RSPB)
    ("19", "INTRODUCTION"),
    # Ch20: "2. Audit Jurisdiction" (PSUs)
    ("20", "AUDITJURISDICTION"),
    # Ch21: "2. Functions Of RDSO"
    ("21", "FUNCTIONSOFRDSO"),
    # Ch22: "2. E-Office"
    ("22", "EOFFICE"),
]

def norm(s):
    return re.sub(r'[^A-Z0-9]+', '', s.upper())

# Build list of (norm_key, chapter_value)
toc_items = [(norm(k), v) for k, v in toc.items()]

# Find anchor positions
anchor_positions = {}
for ch, anchor_norm in CHAPTER_ANCHORS:
    for i, (nk, v) in enumerate(toc_items):
        if nk == anchor_norm:
            anchor_positions[i] = ch
            break
    else:
        # Try partial match
        for i, (nk, v) in enumerate(toc_items):
            if anchor_norm in nk or nk in anchor_norm:
                if i not in anchor_positions:
                    anchor_positions[i] = ch
                    break

# Sort by position
sorted_anchors = sorted(anchor_positions.items())
print("Anchor positions:")
for pos, ch in sorted_anchors:
    print(f"  Chapter {ch}: position {pos} -> {toc_items[pos][1]}")

# Now assign each TOC item to a chapter
chapter_toc = {}
current_chapter = "1"
anchor_idx_map = dict(sorted_anchors)  # position -> chapter

for i, (nk, v) in enumerate(toc_items):
    if i in anchor_idx_map:
        current_chapter = anchor_idx_map[i]
    
    if current_chapter not in chapter_toc:
        chapter_toc[current_chapter] = []
    chapter_toc[current_chapter].append(v)

print("\nChapter TOC sizes:")
for ch, items in sorted(chapter_toc.items(), key=lambda x: int(x[0])):
    print(f"  Chapter {ch}: {len(items)} headings")
    for h in items[:5]:
        print(f"    {h}")

# Save
with open('chapter_toc.json', 'w', encoding='utf-8') as f:
    json.dump(chapter_toc, f, indent=2, ensure_ascii=False)
print("\nSaved chapter_toc.json")
