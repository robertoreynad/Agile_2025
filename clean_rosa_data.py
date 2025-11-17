# clean_rosa_data.py  (save this in the ROOT folder)
import pandas as pd
from pathlib import Path

# --------------------- CONFIG ---------------------
PROJECT_ROOT = Path(__file__).parent  # This script is in the root
CSV_IN       = PROJECT_ROOT / "data" / "ROSA_financial_transactions.csv"
CSV_OUT      = PROJECT_ROOT / "data" / "ROSA_cleaned.csv"

# --------------------- LOAD ---------------------
if not CSV_IN.exists():
    raise FileNotFoundError(f"Input file not found: {CSV_IN}")

df = pd.read_csv(CSV_IN)
print(f"Loaded {len(df)} rows")

# --------------------- CLEANING ---------------------
# Strip whitespace
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Replace empty strings
df.replace("", pd.NA, inplace=True)

# Drop duplicates
dupes = df.duplicated().sum()
df.drop_duplicates(inplace=True)
print(f"Removed {dupes} duplicates")

# Convert types
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce", downcast="integer")

# Drop critical nulls
df.dropna(subset=["date", "amount"], inplace=True)

# Fill description and type
df["description"].fillna("Unknown", inplace=True)
df["type"].fillna(df["type"].mode()[0], inplace=True)

# --------------------- SAVE ---------------------
CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(CSV_OUT, index=False)
print(f"Cleaned data saved: {CSV_OUT}")
print(f"Final rows: {len(df)}")