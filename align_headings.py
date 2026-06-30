import json
import re

def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def norm_no_numbers(t):
    t = re.sub(r'^\d+(\.\d+)*\s*', '', t)
    return re.sub(r'[^a-z0-9]', '', t.lower())

with open('new_toc_mapping.json', 'r', encoding='utf-8') as f:
    toc = json.load(f)

toc_headings = list(toc.values())
N = len(toc_headings)

chunks = []
with open(r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        chunks.append(json.loads(line))
M = len(chunks)

# Create a cost matrix for matching chunk i with TOC j
# We want to find a monotonic path mapping i to j.
# Every chunk MUST be mapped to exactly one TOC entry.
# Multiple chunks can map to the same TOC entry (continuation).
# TOC entries might be skipped if we can't find them, but ideally all are covered.

# Precompute match scores
match_scores = [[0 for _ in range(N)] for _ in range(M)]

for i, c in enumerate(chunks):
    title = c.get('original_title', '')
    text = c.get('text', '')
    raw_head = c.get('heading', '')
    n_title = norm_no_numbers(title)
    
    # Strip non-alphanumeric for text
    n_text = re.sub(r'[^a-z0-9]', '', text.lower())
    
    for j, toc_h in enumerate(toc_headings):
        n_toc = norm_no_numbers(toc_h)
        score = 0
        
        # Exact title match
        if n_toc == n_title and len(n_toc) > 0: score += 20
        # Title substring match
        elif n_title and len(n_title) > 5 and n_title in n_toc: score += 10
        elif n_title and len(n_title) > 5 and n_toc in n_title: score += 10
        
        # Text match
        if len(n_toc) > 5 and n_toc in n_text:
            score += 15
            
        match_scores[i][j] = score

# DP state: dp[i][j] = max score for aligning chunks 0..i such that chunk i is mapped to j.
# Since j must be >= previous j, dp[i][j] = match_scores[i][j] + max(dp[i-1][k]) for k <= j.
# We also want to penalize skipping TOC entries. Let's add a small penalty for j - previous_j > 1.
# Or better: penalize if we don't cover all TOC entries.
# Actually, just finding the best match with DP:

dp = [[-float('inf')] * N for _ in range(M)]
parent = [[-1] * N for _ in range(M)]

for j in range(N):
    # Penalty for starting at j > 0: we skip j headings
    dp[0][j] = match_scores[0][j] - 1000 * j

for i in range(1, M):
    best_k_less_than_j_val = -float('inf')
    best_k_less_than_j_idx = -1
    
    for j in range(N):
        # Update running max for k < j
        if j > 0:
            best_k_less_than_j_val -= 1000  # Penalty for skipping increases by 1000 for every step j moves away from k
            
            val_j_minus_1 = dp[i-1][j-1]
            if val_j_minus_1 > best_k_less_than_j_val:
                best_k_less_than_j_val = val_j_minus_1
                best_k_less_than_j_idx = j - 1
                
        val_skip = best_k_less_than_j_val
        val_stay = dp[i-1][j] - 0.5 # tiny penalty for staying
        
        if val_skip > val_stay:
            best_prev = val_skip
            best_idx = best_k_less_than_j_idx
        else:
            best_prev = val_stay
            best_idx = j
            
        dp[i][j] = best_prev + match_scores[i][j]
        parent[i][j] = best_idx

# Backtrack
best_final_j = -1
best_final_val = -float('inf')
for j in range(N):
    # Penalty for ending at j < N-1: we skip (N - 1 - j) headings
    final_val = dp[M-1][j] - 1000 * (N - 1 - j)
    if final_val > best_final_val:
        best_final_val = final_val
        best_final_j = j

# Backtrack
assignment = []
curr_j = best_final_j
for i in range(M-1, -1, -1):
    assignment.append(curr_j)
    curr_j = parent[i][curr_j]

assignment.reverse()

# Apply assignments
for i, c in enumerate(chunks):
    c['heading'] = toc_headings[assignment[i]]

# Output
out_path = r'c:\Users\Akshith Srinivas\chunk-validator-one\chunks after validation\RAM_2022_Sixth_Edition_fixed.jsonl'
with open(out_path, 'w', encoding='utf-8') as f:
    for c in chunks:
        f.write(json.dumps(c) + '\n')

unique = len(set(assignment))
print(f"Assigned {unique} unique headings out of {N}.")
