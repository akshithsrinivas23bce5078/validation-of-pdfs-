import json

with open('debug_ch21_22.json', 'r', encoding='utf-8') as f:
    raw_21_22 = json.load(f)

text_21 = ''
for c in raw_21_22:
    if c.get('chapter') == '21' or 'RDSO' in str(c.get('title', '')):
        t = c.get('text', '')
        try:
            t = t.encode('latin1').decode('unicode_escape').encode('latin1').decode('utf-8')
        except:
            pass
        t = t.replace('\u2013', '-').replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"').replace('\u2018', "'").replace('\u00a0', ' ')
        text_21 += t + '\n'

ch21_headings = [
    ('1. Introduction', '1. INTRODUCTION'),
    ('2. Functions of RDSO', '2. FUNCTIONS OF RDSO'),
    ('3. Organizational Set Up', '3. ORGANIZATIONAL SET UP'),
    ('4. System Of Audit', '4. SYSTEM OF AUDIT'),
    ('5. Local Audit/Inspections', '5. LOCAL AUDIT/INSPECTIONS'),
    ('6. Use Of It Applications In Rdso', '6. USE OF IT APPLICATIONS IN RDSO'),
    ('7. Audit Focus Areas - Check List', '7. AUDIT FOCUS AREAS'),
    ('8. Functions And Roles Of The Directorates', '8. FUNCTIONS AND ROLES OF THE DIRECTORATES')
]

ch21_text_blocks = {}
current_idx = text_21.find(ch21_headings[0][1])
if current_idx == -1: current_idx = 0
for i in range(len(ch21_headings)):
    name, search_str = ch21_headings[i]
    if i < len(ch21_headings) - 1:
        next_search_str = ch21_headings[i+1][1]
        next_idx = text_21.find(next_search_str, current_idx)
        print(f'{name} -> {search_str} found at {current_idx}, next at {next_idx}')
        ch21_text_blocks[name] = text_21[current_idx:next_idx].strip()
        current_idx = next_idx
    else:
        print(f'{name} -> {search_str} found at {current_idx}, next at END')
        ch21_text_blocks[name] = text_21[current_idx:].strip()

text_8 = ch21_text_blocks['8. Functions And Roles Of The Directorates']
print(f'Length of text_8: {len(text_8)}')
