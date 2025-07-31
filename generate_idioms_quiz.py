import pandas as pd
import json
import random
from collections import Counter
import os

# Format the idiom
def format_text(text):
    return text.strip().capitalize()

# Generate typo distractors
def generate_typo_variants(phrase):
    phrase = phrase.lower().replace(" ", "")
    variants = set()
    vowels = 'aeiou'

    for i in range(len(phrase) - 1):
        swapped = list(phrase)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add(''.join(swapped))

    for i in range(len(phrase)):
        variants.add(phrase[:i] + phrase[i+1:])
        variants.add(phrase[:i] + phrase[i] + phrase[i:])

    for i in range(len(phrase)):
        if phrase[i] in vowels:
            for v in vowels:
                if v != phrase[i]:
                    variants.add(phrase[:i] + v + phrase[i+1:])

    variants.discard(phrase)
    cleaned = [format_text(v) for v in variants if len(v) > 4]
    random.shuffle(cleaned)
    return cleaned[:3]

# Generate options with typo distractors
def generate_options(correct, all_meanings):
    typo_options = generate_typo_variants(correct)

    if len(typo_options) < 3:
        fallback = [format_text(m) for m in all_meanings if m.lower() != correct.lower()]
        random.shuffle(fallback)
        for m in fallback:
            if m not in typo_options and len(typo_options) < 3:
                typo_options.append(m)

    options = typo_options + [format_text(correct)]
    random.shuffle(options)

    labeled = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled.items() if v == format_text(correct)][0]
    return labeled, correct_letter

# File paths
input_excel = 'idioms_list.xlsx'
used_file = 'used_idioms.txt'
output_json = 'idioms_data.json'

# Read Excel file with specified engine
df = pd.read_excel(input_excel, engine='openpyxl')
df.columns = [c.strip() for c in df.columns]
records = df.to_dict(orient='records')
all_meanings = [r['Meaning'] for r in records if r.get('Meaning')]

# Load used idioms
used = set()
if os.path.exists(used_file):
    with open(used_file, 'r', encoding='utf-8') as f:
        used = set(line.strip() for line in f)

quiz_data = []
year_stats = Counter()
max_questions = 5
count = 0

for row in records:
    idiom = row.get('Idioms', '').strip()
    if not idiom or idiom in used:
        continue

    meaning = row.get('Meaning', '').strip()
    hindi = row.get('Hindi Meaning', '—').strip()
    year = row.get('Year', '2024').strip()

    options, correct_letter = generate_options(meaning, all_meanings)

    quiz_data.append({
        'idiom': format_text(idiom),
        'meaning': format_text(meaning),
        'hindi_meaning': hindi,
        'year': year,
        'options': options,
        'correct_letter': correct_letter
    })

    year_stats[year] += 1
    used.add(idiom)
    count += 1
    if count >= max_questions:
        break

# Save used idioms
with open(used_file, 'w', encoding='utf-8') as f:
    for idiom in used:
        f.write(idiom + '\n')

# Save JSON output
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, indent=2, ensure_ascii=False)

# Summary
print(f"✅ Saved {len(quiz_data)} quiz questions to '{output_json}'")
print("📊 Year breakdown:")
for y, c in sorted(year_stats.items()):
    print(f"  {y}: {c} questions")
