import csv
import json
import random
import pandas as pd

# File paths
input_csv = "idioms_list.csv"
output_json = "idioms_data.json"

# Attempt to read CSV with tab delimiter first, fallback to comma
try:
    df = pd.read_csv(input_csv, delimiter="\t")
except Exception:
    df = pd.read_csv(input_csv)

# Format idioms (capitalize each word)
def format_idiom(idiom):
    return ' '.join(word.capitalize() for word in idiom.strip().split())

# Generate quiz data
quiz_data = []

for idx, row in df.iterrows():
    idiom = format_idiom(row["Idioms"])
    correct = row["Meaning"]
    year = int(row["Year"])

    # Choose 3 wrong options (excluding the correct one)
    other_meanings = df[df["Meaning"] != correct]["Meaning"].tolist()
    wrong_options = random.sample(other_meanings, 3) if len(other_meanings) >= 3 else other_meanings

    # Combine and shuffle options
    options = wrong_options + [correct]
    random.shuffle(options)

    quiz_data.append({
        "idiom": idiom,
        "options": options,
        "answer": correct,
        "year": year,
        "hindiMeaning": row["Hindi Meaning"]  # ✅ Added line
    })

# Write JSON output
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(quiz_data, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(quiz_data)} quiz questions.")
