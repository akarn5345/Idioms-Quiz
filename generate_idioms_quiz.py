import pandas as pd
import json
import random
from collections import Counter

# Input/Output
input_xlsx = 'idioms_list.xlsx'
output_json = 'idioms_data.json'

# Capitalize idioms properly
def format_idiom(idiom):
    return ' '.join(word.capitalize() for word in idiom.strip().split())

# Load Excel
df = pd.read_excel(input_xlsx, engine='openpyxl', dtype=str).fillna('')
rows = df.to_dict(orient='records')

# Prepare data
quiz_data = []
year_counter = Counter()

meanings_pool = [row['Meaning'].strip() for row in rows if row.get('Meaning')]

for row in rows:
    idiom = format_idiom(row.get('Idioms', ''))
    correct_meaning = row.get('Meaning', '').strip()
    hindi_meaning = row.get('Hindi Meaning', '').strip() or 'No Hindi meaning available'
    year = str(row.get('Year', '')).strip() or '2024'

    # Get 3 wrong options (exclude correct one)
    wrong_options = random.sample([m for m in meanings_pool if m != correct_meaning], 3)
    options = wrong_options + [correct_meaning]
    random.shuffle(options)

    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == correct_meaning][0]

    quiz_data.append({
        'idiom': idiom,
        'year': year,
        'hindi_meaning': hindi_meaning,
        'options': labeled_options,
        'correct_letter': correct_letter
    })

    year_counter[year] += 1

# Save JSON
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, indent=2, ensure_ascii=False)

# Summary
print(f"✅ Quiz data written to '{output_json}' with {len(quiz_data)} questions.")
print("\n📊 Question count by year:")
for yr, count in sorted(year_counter.items()):
    print(f"  {yr}: {count} questions")
