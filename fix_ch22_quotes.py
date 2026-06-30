import json
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

for c in chunks:
    if c.get('chapter') == '22':
        h = c.get('heading', '')
        if h.startswith('8.'):
            text = c['text']
            # Re-assign the text from text_8 without smart quotes
            text_8 = """eOffice's 'Collaboration and Messaging Services' helps users to communicate effectively and share information in real time. It has three sub-components i.e. Appointment, Instant Messaging Services and e-Talk.
The 'Appointment' section facilitates in performing various activities like scheduling appointments, meetings, events, convention etc.
The Instant Messaging Services (IMS) section provides users a functionality through which they can exchange messages over the eOffice portal in real time.
The eTalk (Instant Chat application) section is an effective communication on the usage of words and facilitates a team to work together over a geographical distance and let internal users, systems and departments to communicate."""
            c['text'] = text_8

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print("Fixed smart quotes in Chapter 22 heading 8.")
