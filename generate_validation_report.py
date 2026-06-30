import json

file_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\tngscr_rules_1973_160625_validated.jsonl'

required_keys = {'DOC_NAME': str, 'doc_id': str, 'chapter': str, 'title': str, 'heading': str, 'text': str, 'page_no': str, 'has_table': bool, 'table_html': str}
total_lines = 0
valid_lines = 0

issues = []

doc_names = set()
doc_ids = set()
chapters = set()
titles = set()

with open(file_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        total_lines += 1
        line_valid = True
        line_issues = []
        
        try:
            data = json.loads(line)
            
            # Check keys and types
            for key, expected_type in required_keys.items():
                if key not in data:
                    line_issues.append(f"Missing key: {key}")
                    line_valid = False
                elif not isinstance(data[key], expected_type):
                    line_issues.append(f"Invalid type for {key}: expected {expected_type.__name__}, got {type(data[key]).__name__}")
                    line_valid = False
                    
            if line_valid:
                # Check empty values for critical fields
                for key in ['DOC_NAME', 'doc_id', 'chapter', 'title', 'heading', 'text', 'page_no']:
                    if not data[key].strip():
                        line_issues.append(f"Empty value for key: {key}")
                        line_valid = False
                
                # Check has_table logic
                if data['has_table'] and data['table_html'] in ('{}', '', None):
                    line_issues.append("has_table is true but table_html is empty")
                    line_valid = False
                if not data['has_table'] and data['table_html'] not in ('{}', '', None):
                    line_issues.append("has_table is false but table_html contains data")
                    line_valid = False
                    
                doc_names.add(data['DOC_NAME'])
                doc_ids.add(data['doc_id'])
                chapters.add(data['chapter'])
                titles.add(data['title'])
                
        except json.JSONDecodeError as e:
            line_issues.append(f"Invalid JSON format: {e}")
            line_valid = False
            
        if line_valid:
            valid_lines += 1
        else:
            issues.append(f"Line {total_lines}: " + ", ".join(line_issues))

validation_percentage = (valid_lines / total_lines) * 100 if total_lines > 0 else 0

print(f"Total Lines: {total_lines}")
print(f"Valid Lines: {valid_lines}")
print(f"Invalid Lines: {total_lines - valid_lines}")
print(f"Validation Percentage: {validation_percentage:.2f}%")
print(f"Unique DOC_NAMEs: {len(doc_names)} {list(doc_names)}")
print(f"Unique doc_ids: {len(doc_ids)} {list(doc_ids)}")
print(f"Unique chapters: {len(chapters)} {list(chapters)}")
print(f"Unique titles: {len(titles)} {list(titles)}")
print("\nIssues:")
for issue in issues:
    print(issue)
if not issues:
    print("None")
