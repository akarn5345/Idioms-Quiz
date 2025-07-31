import csv
import json
import random
import pandas as pd

# File paths
input_csv = "idioms_list.csv"
output_json = "idioms_data.json"

# Load the CSV with tab delimiter
df = pd.read_csv(input_csv, delimiter="\t")

# Format idioms (capitalize each word)
def format_idiom(idiom):
    return ' '.join(word.capitalize() for word in idiom.strip().split())

# Generate quiz data
quiz_data = []
used_indices = set()

for idx, row in df.iterrows():
    idiom = format_idiom(row["Idioms"])
    correct = row["Meaning"]
    year = int(row["Year"])

    # Choose 3 wrong options (exclude the correct one)
    other_meanings = df[df["Meaning"] != correct]["Meaning"].tolist()
    wrong_options = random.sample(other_meanings, 3)

    # Combine and shuffle options
    options = wrong_options + [correct]
    random.shuffle(options)

    quiz_data.append({
        "idiom": idiom,
        "options": options,
        "answer": correct,
        "year": year
    })

# Write JSON output
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(quiz_data, f, indent=2, ensure_ascii=False)

print(f"Generated {len(quiz_data)} quiz questions.")
