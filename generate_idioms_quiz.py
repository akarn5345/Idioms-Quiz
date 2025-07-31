import csv
import json
import random
from collections import Counter

USED_TRACK_FILE = 'used_idioms.txt'

# Format the idiom (capitalize first letter of each word)
def format_idiom(idiom):
    return ' '.join(word.capitalize() for word in idiom.strip().split())

# Generate 3 fresh distractors every time
def generate_distractor_meanings(correct_meaning, all_meanings):
    meanings_pool = [m for m in all_meanings if m.strip() and m.strip().lower() != correct_meaning.strip().lower()]
    return random.sample(meanings_pool, 3) if len(meanings_pool) >= 3 else meanings_pool[:3]

# Generate options
def generate_options(correct_idiom, all_idioms, all_meanings):
    correct_meaning = next(row['Meaning'] for row in all_idioms if row['Idioms'] == correct_idiom)
    distractors = generate_distractor_meanings(correct_meaning, all_meanings)
    options = distractors + [correct_meaning]
    random.shuffle(options)
    labeled = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled.items() if v == correct_meaning][0]
    return labeled, correct_letter

# Load used idioms
def load_used_idioms():
    try:
        with open(USED_TRACK_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

# Save used idioms
def save_used_idioms(used):
    with open(USED_TRACK_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(used))

# Input/output
input_csv = 'idioms_list.csv'
output_json = 'idioms_data.json'

quiz_data = []
year_counter = Counter()
unique_years = set()

used_idioms = load_used_idioms()

with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
    rows = list(reader)

    all_idioms = [{'Idioms': row['Idioms'], 'Meaning': row['Meaning']} for row in rows if row.get('Idioms')]
    all_meanings = [row['Meaning'] for row in rows if row.get('Meaning')]

    unused_rows = [row for row in rows if row.get('Idioms') and row['Idioms'].strip() not in used_idioms]
    if not unused_rows:
        print("🔄 All idioms used. Resetting...")
        unused_rows = rows
        used_idioms = set()

    for row in unused_rows:
        idiom = row.get('Idioms', '').strip()
        if not idiom:
            continue

        meaning = row.get('Meaning', '').strip()
        hindi_meaning = row.get('Hindi Meaning', '').strip()
        year = row.get('Year', '').strip() or '2024'
        unique_years.add(year)
        year_counter[year] += 1

        options, correct_letter = generate_options(idiom, all_idioms, all_meanings)

        quiz_data.append({
            'correct_idiom': format_idiom(idiom),
            'year': year,
            'meaning': meaning,
            'hindi_meaning': hindi_meaning,
            'options': options,
            'correct_letter': correct_letter
        })

        used_idioms.add(idiom)

        # 🔁 Removed the 25-question limit

# Save final output with both questions and list of years
final_output = {
    "questions": quiz_data,
    "years": sorted(unique_years)
}

with open(output_json, 'w', encoding='utf-8') as out:
    json.dump(final_output, out, indent=2, ensure_ascii=False)

save_used_idioms(used_idioms)

print(f"✅ Quiz saved to '{output_json}' with {len(quiz_data)} questions.")
print("\n📊 Year-wise breakdown:")
for y, c in sorted(year_counter.items()):
    print(f"  {y}: {c} questions")
