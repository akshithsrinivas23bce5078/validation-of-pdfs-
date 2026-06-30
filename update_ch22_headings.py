import json
import os

INPUT_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
TEMP_FILE = r'chunks after validation\RAM_2022_Sixth_Edition_fixed_temp.jsonl'

text_6 = """eLeave is a centralized system for maintenance of leave record. It is a simple intuitive workflow based system to apply for leave online, track the status of applied leave, to provide details of leaves taken, balance leaves etc. Approval of leave is enabled through the automated hierarchical channel of submission and leave is routed as per the hierarchy pre-defined in the work flow.
The system facilitates users to apply for leave, check their updated leave balance, check their approved workflow i.e. the hierarchy through which their leave moves, to extend/curtail/cancel their sanctioned leaves, to track their leaves by getting notification/alert regarding sanctioned/approved leaves via SMS/Email etc.
The module generates various reports such as Report containing details of all types of leaves including those of subordinates pertaining to a specific period of time, Report containing leave history along with status of leaves applied etc.
The eLeave system helps to eliminate the paper based applications and facilitates faster and time bound processing."""

text_7 = """Knowledge Management System (KMS) component of eOffice is a Central Repository of Documents from where the users can publish as well as access the information. KMS controls the life cycle of documents, enabling users to create, upload and manage electronic documents that can be viewed, searched, shared and published. It also facilitates tracking of the different versions of modified documents by different users (Tracking history). It contains a dynamic workflow to keep document in various stages."""

text_8 = """eOffice’s ‘Collaboration and Messaging Services’ helps users to communicate effectively and share information in real time. It has three sub-components i.e. Appointment, Instant Messaging Services and e-Talk.
The ‘Appointment’ section facilitates in performing various activities like scheduling appointments, meetings, events, convention etc.
The Instant Messaging Services (IMS) section provides users a functionality through which they can exchange messages over the eOffice portal in real time.
The eTalk (Instant Chat application) section is an effective communication on the usage of words and facilitates a team to work together over a geographical distance and let internal users, systems and departments to communicate."""

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    chunks = [json.loads(line) for line in f]

updated = 0
for i, c in enumerate(chunks):
    if c.get('chapter') == '22':
        heading = c.get('heading', '')
        if heading.startswith('6.'):
            chunks[i]['heading'] = "6. LEAVE MANAGEMENT SYSTEM"
            chunks[i]['text'] = text_6
            updated += 1
        elif heading.startswith('7.'):
            chunks[i]['heading'] = "7. KNOWLEDGE MANAGEMENT SYSTEM"
            chunks[i]['text'] = text_7
            updated += 1
        elif heading.startswith('8.'):
            chunks[i]['heading'] = "8. COLLABORATION AND MESSAGING SERVICES"
            chunks[i]['text'] = text_8
            updated += 1

with open(TEMP_FILE, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + '\n')

os.replace(TEMP_FILE, INPUT_FILE)
print(f"Updated {updated} chunks in Chapter 22.")
