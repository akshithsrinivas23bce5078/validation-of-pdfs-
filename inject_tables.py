import json
import re

def extract_text_from_html(html):
    # Simple regex to extract text between > and <
    text = re.sub(r'<[^>]+>', ' ', html)
    # Replace html entities
    text = text.replace('&nbsp;', ' ')
    # remove extra spaces
    return re.sub(r'\s+', ' ', text).strip()

def main():
    print("Loading tables...")
    with open('extracted_tables.json', 'r', encoding='utf-8') as f:
        tables = json.load(f)

    print("Loading chunks...")
    chunks = []
    with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
        for line in f:
            chunks.append(json.loads(line))

    # For each table, find the best matching chunk
    matched_count = 0
    for t in tables:
        table_text = extract_text_from_html(t['html'])
        words = set(w.lower() for w in table_text.split() if len(w) > 3)
        
        if not words:
            continue
            
        best_chunk = None
        best_score = 0
        
        for c in chunks:
            chunk_words = set(w.lower() for w in c['text'].split() if len(w) > 3)
            # Find intersection
            intersection = words.intersection(chunk_words)
            score = len(intersection) / len(words)
            
            if score > best_score:
                best_score = score
                best_chunk = c

        # If score is decently high, assign it
        if best_chunk and best_score > 0.3:
            best_chunk['has_table'] = True
            # if multiple tables in one chunk, we can append them or wrap them in a div
            if not best_chunk.get('table_html') or not best_chunk['table_html']:
                best_chunk['table_html'] = {"html": t['html']}
            else:
                existing_html = best_chunk['table_html'].get("html", "")
                best_chunk['table_html'] = {"html": existing_html + "<br>" + t['html']}
            matched_count += 1
            try:
                print(f"Matched table on page {t['page']} to chunk: {best_chunk['heading']} (Score: {best_score:.2f})")
            except UnicodeEncodeError:
                print(f"Matched table on page {t['page']} to chunk with score {best_score:.2f}")
        else:
            print(f"Could not match table on page {t['page']}. Best score: {best_score:.2f}")

    print(f"Successfully matched {matched_count} out of {len(tables)} tables.")

    print("Writing updated chunks...")
    with open(r'chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'w', encoding='utf-8') as f:
        for c in chunks:
            fixed_c = {
                "chapter": c.get("chapter"),
                "title": c.get("title"),
                "heading": c.get("heading"),
                "text": c.get("text"),
                "page.no": c.get("page.no", "()"),
                "has_table": c.get("has_table", False),
                "table_html": c.get("table_html", {})
            }
            f.write(json.dumps(fixed_c, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
