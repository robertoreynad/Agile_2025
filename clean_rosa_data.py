# clean_rosa_data.py   ← Put this in C:\Users\sacbe\OneDrive\Desktop\Agile_2025\
import pandas as pd
from pathlib import Path

# THIS IS THE ONLY CORRECT LINE FOR YOUR PROJECT
PROJECT_ROOT = Path(__file__).parent                  # ← script is in the root folder
CSV_IN       = PROJECT_ROOT / "data" / "ROSA_financial_transactions.csv"
CSV_OUT      = PROJECT_ROOT / "data" / "ROSA_cleaned.csv"

print(f"Looking for file: {CSV_IN}")

if not CSV_IN.exists():
    raise FileNotFoundError(f"ERROR: File not found!\n   → {CSV_IN}\n   Make sure the file is in the 'data' folder!")

print("Loading data...")
df = pd.read_csv(CSV_IN)

print(f"Original rows: {len(df)}")

# --- CLEANING ---
df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['customer_id'] = pd.to_numeric(df['customer_id'], errors='coerce', downcast='integer')

df.dropna(subset=['date', 'amount'], inplace=True)
df['description'].fillna('Unknown', inplace=True)
df['type'].fillna(df['type'].mode()[0], inplace=True)

print(f"Cleaned rows: {len(df)}")
df.to_csv(CSV_OUT, index=False)
print(f"Cleaned file saved → {CSV_OUT}")