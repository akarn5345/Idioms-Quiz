import pandas as pd
import json
import random
from collections import Counter
import os

# Format the word (capitalize only the first letter)
def format_word(word):
    return word.strip().capitalize()

# Generate typo variants
def generate_typo_variants(word):
    word = word.lower()
    variants = set()
    vowels = 'aeiou'

    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add(''.join(swapped))

    for i in range(len(word)):
        variants.add(word[:i] + word[i+1:])
        variants.add(word[:i] + word[i] + word[i:])

    for i in range(len(word)):
        if word[i] in vowels:
            for v in vowels:
                if v != word[i]:
                    variants.add(word[:i] + v + word[i+1:])

    variants.discard(word)
    variants = [format_word(v) for v in variants if len(v) > 2 and v.lower() != word.lower()]
    random.shuffle(variants)
    return variants[:3]

# Generate options
def generate_options(correct_word, all_words):
    typo_options = generate_typo_variants(correct_word)

    if len(typo_options) < 3:
        fallback = [format_word(w) for w in all_words if w.lower() != correct_word.lower()]
        random.shuffle(fallback)
        for w in fallback:
            if format_word(w) not in typo_options and len(typo_options) < 3:
                typo_options.append(format_word(w))

    options = typo_options + [format_word(correct_word)]
    random.shuffle(options)

    labeled_options = dict(zip(['A', 'B', 'C', 'D'], options))
    correct_letter = [k for k, v in labeled_options.items() if v == format_word(correct_word)][0]

    return labeled_options, correct_letter

# File paths
input_excel = 'word_list.xlsx'
used_words_file = 'used_words.txt'
output_json = 'quiz_data.json'

# Load data from Excel
df = pd.read_excel(input_excel)
df.columns = [c.strip() for c in df.columns]  # Normalize headers

rows = df.to_dict(orient='records')
all_words = [row['Word'].strip() for row in rows if 'Word' in row and row['Word'].strip()]

# Load used words
used = set()
if os.path.exists(used_words_file):
    with open(used_words_file, 'r', encoding='utf-8') as f:
        used = set(line.strip() for line in f)

quiz_data = []
year_counter = Counter()

# Generate up to N new questions
max_questions = 5
count = 0

for row in rows:
    if count >= max_questions:
        break
    if 'Word' not in row or not row['Word'].strip():
        continue

    correct_word = row['Word'].strip()
    if correct_word in used:
        continue

    year_raw = row.get('Year')
    year = year_raw.strip() if year_raw and year_raw.strip() else '2024'

    hindi_meaning = row.get('Hindi Meaning', 'No Hindi meaning available').strip()

    options, correct_letter = generate_options(correct_word, all_words)

    quiz_data.append({
        'correct_word': format_word(correct_word),
        'year': year,
        'hindi_meaning': hindi_meaning,
        'options': options,
        'correct_letter': correct_letter
    })

    year_counter[year] += 1
    used.add(correct_word)
    count += 1

# Save used words
with open(used_words_file, 'w', encoding='utf-8') as f:
    for word in used:
        f.write(word + '\n')

# Write to JSON
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, indent=2, ensure_ascii=False)

# Summary
print(f"✅ Quiz data written to '{output_json}' with {len(quiz_data)} new questions.")
print("\n📊 Question count by year:")
for yr, count in sorted(year_counter.items()):
    print(f"  {yr}: {count} questions")
