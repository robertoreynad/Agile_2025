"""Core functions for the ROSA Financial Transactions Summary Tool."""

import pandas as pd


def load_transactions(csv_path: str) -> pd.DataFrame:
    """Load the financial transactions dataset from a CSV file.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the transactions.
    """
    return pd.read_csv(csv_path)


def summarize_totals(df: pd.DataFrame) -> dict:
    """Compute total income, total expenses, and net balance.

    Assumes the DataFrame has at least:
    - a numeric column named 'amount' where income is positive and expenses are negative.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with a column `amount`.

    Returns
    -------
    dict
        Dictionary with total_income, total_expenses, and net_balance.
    """
    if "amount" not in df.columns:
        raise ValueError("Expected an 'amount' column in the dataset.")

    total_income = df[df["amount"] > 0]["amount"].sum()
    total_expenses = df[df["amount"] < 0]["amount"].sum()
    net_balance = df["amount"].sum()

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
    }
