import os
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

OUTPUT_DIR = "../output"
DATA_PATH = "data/ROSA_financial_transactions.csv"

# category keywords
category_keywords = {
    "Groceries": ["supermarket", "grocery", "food", "market", "sainsbury", "tesco", "aldi", "lidl", "whole foods", "eats", "meal", "fresh"],
    "Transport": ["bus", "train", "uber", "taxi", "fuel", "petrol", "gas", "transport", "metro", "car", "ride", "road", "way", "direction"],
    "Utilities": ["electricity", "water", "internet", "rent", "utility", "bill", "mobile", "payment", "service", "home", "house", "light", "electric", "phone", "cost", "charge"],
    "Entertainment": ["movie", "cinema", "concert", "theater", "game", "bar", "restaurant", "club", "leisure", "event", "dinner", "film", "play", "show", "fun", "happy", "music", "party", "star", "enjoy"],
    "Shopping": ["store", "shop", "retail", "clothes", "amazon", "online", "purchase", "boutique", "computer", "paper", "tv", "gift", "item", "product", "sale", "new", "old", "white", "green", "big", "bag", "box", "price", "list"],
    "Health": ["pharmacy", "hospital", "doctor", "clinic", "medical", "health", "medication", "care", "drug", "medicine", "sick", "well"],
    "Travel": ["hotel", "flight", "travel", "airline", "vacation", "trip", "booking", "conference", "tour", "journey", "airport", "foreign", "destination"],
    "Education": ["school", "course", "university", "college", "tuition", "study", "book", "education", "learn", "class", "student", "teacher", "knowledge", "ability"],
    "Salary": ["salary", "paycheck", "income", "wage", "payroll"]
}

# Merchants simulated by category
category_merchants = {
    "Groceries": ["Tesco", "WholeFoods", "Aldi", "Lidl"],
    "Transport": ["Uber", "Lyft", "Metro", "Greyhound"],
    "Utilities": ["HydroOne", "Bell", "Rogers", "Enbridge"],
    "Entertainment": ["Netflix", "Cineplex", "Spotify", "AMC"],
    "Shopping": ["Amazon", "Walmart", "Target", "BestBuy"],
    "Health": ["ShoppersDrugMart", "CVS", "Walgreens", "Hospital"],
    "Travel": ["AirCanada", "Delta", "Hilton", "Expedia"],
    "Education": ["Coursera", "Udemy", "Harvard", "ILAC"],
    "Salary": ["CompanyPayroll"],
    "Miscellaneous": ["OtherMerchant"]
}


def format_currency(x, pos=None):
    if x >= 1_000_000:
        return f"{x * 1e-6:.1f}M"
    elif x >= 1_000:
        return f"{x * 1e-3:.1f}K"
    return f"{x:.0f}"

# load data


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    print(f"[load] Reading data from: {path}")
    df = pd.read_csv(path)
    return df

# cleaning


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("[clean] Cleaning descriptions and assigning categories...")
    df["cleaned_description"] = df["description"].str.lower().apply(
        lambda x: re.sub(r"[\W_]+", " ", str(x))
    )
    df["Category"] = "Miscellaneous"
    for category, keywords in category_keywords.items():
        for keyword in keywords:
            mask = df["cleaned_description"].str.contains(keyword, na=False)
            df.loc[mask, "Category"] = category

    # simulate merchant by category
    df["merchant"] = df["Category"].apply(lambda cat: np.random.choice(
        category_merchants.get(cat, ["OtherMerchant"])
    ))

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df

# summary


def run_summaries(df: pd.DataFrame) -> dict:
    print("[summary] Generating summary tables...")
    by_category = df.groupby("Category")["amount"].sum(
    ).sort_values(ascending=False).reset_index()
    by_merchant = df.groupby("merchant")["amount"].sum(
    ).sort_values(ascending=False).reset_index()

    print("\nCategory summary:")
    print(by_category)

    print("\nTop 10 merchants by spending:")
    print(by_merchant.head(10))

    return {"by_category": by_category, "by_merchant": by_merchant}

# Charts


def generate_charts(summaries: dict) -> None:
    print("[charts] Generating and saving charts to output/ ...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Spending by Category
    cat = summaries["by_category"]
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="amount", y="Category", data=cat,
                     hue="Category", legend=False, palette="Set2")
    plt.title("Spending by Category")
    plt.xlabel("Total Spending")
    plt.ylabel("Category")
    plt.gca().xaxis.set_major_formatter(FuncFormatter(format_currency))
    for p in ax.patches:
        value = p.get_width()
        ax.annotate(
            format_currency(value),
            (value, p.get_y() + p.get_height() / 2),
            ha="left", va="center", fontsize=9, color="black",
            xytext=(5, 0), textcoords="offset points"
        )
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "summary_by_category.png"),
                bbox_inches="tight")
    plt.close()

    # Top 10 merchants
    mer = summaries["by_merchant"].head(10)
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x="amount", y="merchant", data=mer,
                     hue="merchant", legend=False, palette="Set2")
    plt.title("Top 10 Merchants by Total Spending")
    plt.xlabel("Total Spending")
    plt.ylabel("Merchant")
    plt.gca().xaxis.set_major_formatter(FuncFormatter(format_currency))
    for p in ax.patches:
        value = p.get_width()
        ax.annotate(
            format_currency(value),
            (value, p.get_y() + p.get_height() / 2),
            ha="left", va="center", fontsize=9, color="black",
            xytext=(5, 0), textcoords="offset points"
        )
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_merchants.png"),
                bbox_inches="tight")
    plt.close()

# Pipeline


def run_pipeline():
    df = load_data()
    df = clean_data(df)
    summaries = run_summaries(df)
    generate_charts(summaries)
    print("[done] Pipeline completed without errors.")
