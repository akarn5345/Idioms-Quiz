import pandas as pd
import json
import random
import os
import openpyxl

# Check file extension and existence
file_path = 'idioms_list.xlsx'
if not os.path.isfile(file_path) or not file_path.lower().endswith('.xlsx'):
    raise FileNotFoundError(f"Error: '{file_path}' is not a valid .xlsx file or does not exist.")

# Validate file integrity
try:
    openpyxl.load_workbook(file_path)
except openpyxl.utils.exceptions.InvalidFileException as e:
    raise Exception(f"Error: '{file_path}' is not a valid Excel file: {str(e)}")
except Exception as e:
    raise Exception(f"Error: Cannot read '{file_path}' due to file corruption or format issue: {str(e)}")

# Read the .xlsx file with openpyxl engine
try:
    df = pd.read_excel(file_path, engine='openpyxl')
except FileNotFoundError:
    raise FileNotFoundError(f"Error: '{file_path}' not found in the current directory.")
except Exception as e:
    raise Exception(f"Error reading '{file_path}': {str(e)}")

# Define required and optional columns
required_columns = ['Idioms', 'Meaning', 'Hindi Meaning', 'Year']
all_columns = required_columns + ['Difficulty']  # Allow optional 'Difficulty' column

# Check for required columns
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

# Validate data
if df['Idioms'].duplicated().any():
    raise ValueError("Error: Duplicate 'Idioms' found in the Excel file. Each idiom must be unique.")
df = df.dropna(subset=['Meaning', 'Hindi Meaning'])  # Remove rows with missing meanings
if df.empty:
    raise ValueError("Error: No valid data after removing rows with missing 'Meaning' or 'Hindi Meaning'.")

# Prepare quiz data
quiz_data = []
all_meanings = df['Meaning'].tolist()

for index, row in df.iterrows():
    # Select 3 random incorrect meanings, ensuring no duplicates within options
    available_meanings = [m for m in all_meanings if m != row['Meaning']]
    if len(available_meanings) < 3:
        raise ValueError(f"Error: Not enough unique meanings to generate options for idiom '{row['Idioms']}'. Need at least 3 other meanings.")
    incorrect_meanings = random.sample(available_meanings, 3)
    # Combine correct and incorrect meanings, then shuffle
    options = [row['Meaning']] + incorrect_meanings
    random.shuffle(options)
    
    question = {
        'idiom': row['Idioms'],
        'meaning': row['Meaning'],
        'hindi_meaning': row['Hindi Meaning'],
        'year': str(row['Year']),  # Convert to string to match HTML radio values
        'options': options
    }
    # Add optional Difficulty if present
    if 'Difficulty' in df.columns and pd.notna(row['Difficulty']):
        question['difficulty'] = str(row['Difficulty'])
    quiz_data.append(question)

# Save to quiz_data.json
try:
    with open('quiz_data.json', 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    print("quiz_data.json generated successfully!")
except Exception as e:
    raise Exception(f"Error writing to 'quiz_data.json': {str(e)}")
