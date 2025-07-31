import pandas as pd
import json
import random

# Read the .xlsx file
df = pd.read_excel('idioms_data.xlsx')

# Ensure required columns exist
required_columns = ['Idioms', 'Meaning', 'Hindi Meaning']
if not all(col in df.columns for col in required_columns):
    raise ValueError("Excel file must contain 'Idioms', 'Meaning', and 'Hindi Meaning' columns")

# Prepare quiz data
quiz_data = []
all_meanings = df['Meaning'].tolist()

for index, row in df.iterrows():
    # Select 3 random incorrect meanings
    incorrect_meanings = random.sample([m for m in all_meanings if m != row['Meaning']], 3)
    # Combine correct and incorrect meanings, then shuffle
    options = [row['Meaning']] + incorrect_meanings
    random.shuffle(options)
    
    question = {
        'idiom': row['Idioms'],
        'meaning': row['Meaning'],
        'hindi_meaning': row['Hindi Meaning'],
        'options': options
    }
    quiz_data.append(question)

# Save to quiz_data.json
with open('quiz_data.json', 'w', encoding='utf-8') as f:
    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

print("quiz_data.json generated successfully!")
