import csv
import json
import random
from collections import Counter

# Format the idiom (capitalize first letter of each word)
def format_idiom(idiom):
    return ' '.join(word.capitalize() for word in idiom.strip().split())

# Generate distractor meanings with similarity
def generate_distractor_meanings(correct_meaning, all_meanings):
    # Split correct meaning into keywords (simple approach: non-stop words)
    keywords = [word.lower() for word in correct_meaning.split() if word.lower() not in ['a', 'an', 'the', 'of', 'and']]
    if not keywords:
        keywords = [correct_meaning.split()[0].lower()]  # Fallback to first word

    # Find meanings with at least one similar keyword
    similar_meanings = []
    for meaning in all_meanings:
        if meaning.lower() != correct_meaning.lower():
            if any(keyword in meaning.lower() for keyword in keywords):
                similar_meanings.append(meaning)

    # If not enough similar meanings, fall back to random non-matching meanings
    distractors = similar_meanings[:3]
    if len(distractors) < 3:
        available_meanings = [m for m in all_meanings if m.lower() != correct_meaning.lower() and m not in similar_meanings]
        random.shuffle(available_meanings)
        distractors.extend(available_meanings[:3 - len(distractors)])

    return distractors[:3]  # Ensure exactly three distractors

# Generate options with meanings
def generate_options(correct_idiom, all_idioms, all_meanings):
    correct_meaning = next(row['Meaning'] for row in all_idioms if row['Idioms'] == correct_idiom)
    distractor_options = generate_distractor_meanings(correct_meaning, all_meanings)
    options = distractor_options + [correct_meaning]
    random.shuffle(options)  # Shuffle the final options list
    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == correct_meaning][0]
    return labeled_options, correct_letter

# Input/Output files
input_csv = 'idioms_list.csv'
output_json = 'idioms_data.json'

quiz_data = []
year_counter = Counter()

# Read CSV and normalize headers
with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    reader.fieldnames = [fn.strip() for fn in reader.fieldnames]
    rows = list(reader)
    
    all_idioms = [{'Idioms': row['Idioms'], 'Meaning': row['Meaning']} for row in rows if 'Idioms' in row and row['Idioms'].strip()]
    all_meanings = [row['Meaning'] for row in rows if 'Idioms' in row and row['Idioms'].strip()]
    
    for row in rows:
        if 'Idioms' not in row or not row['Idioms'].strip():
            continue
        
        correct_idiom = row['Idioms'].strip()
        
        # Handle Year with cleanup
        year_raw = row.get('Year')
        year = year_raw.strip() if year_raw and year_raw.strip() else '2024'
        
        # Handle Meaning and Hindi Meaning
        meaning = row.get('Meaning', 'No meaning available').strip()
        hindi_meaning = row.get('Hindi Meaning', 'कोई अर्थ उपलब्ध नहीं').strip()
        
        year_counter[year] += 1
        
        options, correct_letter = generate_options(correct_idiom, all_idioms, all_meanings)
        
        quiz_data.append({
            'correct_idiom': format_idiom(correct_idiom),
            'year': year,
            'meaning': meaning,
            'hindi_meaning': hindi_meaning,
            'options': options,
            'correct_letter': correct_letter
        })

# Write to JSON
with open(output_json, 'w', encoding='utf-8') as jsonfile:
    json.dump(quiz_data, jsonfile, indent=2, ensure_ascii=False)

# Summary
print(f"✅ Quiz data written to '{output_json}' with {len(quiz_data)} questions.")
print("\n📊 Question count by year:")
for yr, count in sorted(year_counter.items()):
    print(f"  {yr}: {count} questions")
