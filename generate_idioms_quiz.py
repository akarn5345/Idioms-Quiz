import pandas as pd
import json
import random
from collections import deque
import os

# File paths
file_path = "idioms_list.xlsx"
json_output = "idioms_data.json"
used_ids_file = "used_ids.txt"

# Read the Excel file (even if misnamed, fallback to CSV reader)
try:
    df = pd.read_excel(file_path)
except Exception:
    df = pd.read_csv(file_path, sep='\t' if '\t' in open(file_path).readline() else ',')

# Shuffle once and cycle through
random.seed(42)  # For reproducibility
all_data = df.to_dict(orient="records")
random.shuffle(all_data)
queue = deque(all_data)

# Load used idioms if present
used = set()
if os.path.exists(used_ids_file):
    with open(used_ids_file, "r") as f:
        used = set(line.strip() for line in f)

quiz_data = []

while queue:
    item = queue.popleft()
    idiom = item["Idioms"].strip()
    if idiom in used:
        continue

    correct = item["Meaning"].strip()
    year = item.get("Year", "")

    # Collect 3 wrong meanings
    other_meanings = [i["Meaning"] for i in all_data if i["Idioms"] != idiom]
    wrong_options = random.sample(other_meanings, min(3, len(other_meanings)))
    options = wrong_options + [correct]
    random.shuffle(options)

    quiz_data.append({
        "idiom": idiom,
        "options": options,
        "answer": correct,
        "year": year
    })

    used.add(idiom)
    break  # Only add one question at a time

# Save used idioms
with open(used_ids_file, "w") as f:
    for idiom in used:
        f.write(idiom + "\n")

# Write JSON output
with open(json_output, "w", encoding="utf-8") as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print(f"Quiz generated: {json_output}")
