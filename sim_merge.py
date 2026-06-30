import json
import re

import validate_som_schema

# validate_som_schema already output to SECRETARIAT_OFFICE_MANUAL_validated.jsonl.
# BUT wait! I shouldn't run it and overwrite my carefully restored bold headings!
# I will just write a script to simulate the merge.
