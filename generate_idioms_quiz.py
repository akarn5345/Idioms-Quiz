import csv
import json
import random
from collections import Counter

# Format the idiom (capitalize first letter of each word)
def format_idiom(idiom):
    return ' '.join(word.capitalize() for word in idiom.strip().split())

# Generate relatable distractor idioms with shuffling
def generate_distractor_idioms(correct_idiom, all_idioms):
    available_idioms = [i for i in all_idioms if i.lower() != correct_idiom.lower()]
    random.shuffle(available_idioms)  # Shuffle the pool each time
    return [format_idiom(i) for i in available_idioms[:3]]  # Pick three random distractors

# Generate options with shuffling
def generate_options(correct_idiom, all_idioms):
    distractor_options = generate_distractor_idioms(correct_idiom, all_idioms)
    options = distractor_options + [format_idiom(correct_idiom)]
    random.shuffle(options)  # Shuffle the final options list
    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == format_idiom(correct_idiom)][0]
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
    
    all_idioms = [row['Idioms'] for row in rows if 'Idioms' in row and row['Idioms'].strip()]
    
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
        
        options, correct_letter = generate_options(correct_idiom, all_idioms)
        
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
