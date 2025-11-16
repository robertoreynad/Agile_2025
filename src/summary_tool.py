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
    
    df = pd.read_csv(csv_path)

    
    if "date" in df.columns:
        # errors="coerce" convierte valores inválidos en NaT (missing datetime)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


def summarize_totals(df: pd.DataFrame) -> dict:
    """Compute total income, total expenses, net balance, and transfers.

    Assumes the DataFrame has:
    - a numeric column named 'amount'
    - a column named 'type' with values such as 'credit', 'debit', 'transfer'.

    Returns
    -------
    dict
        Dictionary with:
        - total_income
        - total_expenses
        - net_balance
        - total_transfers
    """
    
    if "amount" not in df.columns:
        raise ValueError("Expected an 'amount' column in the dataset.")
    if "type" not in df.columns:
        raise ValueError("Expected a 'type' column in the dataset.")

    
    income = df.loc[df["type"] == "credit", "amount"].sum()

    
    expenses = df.loc[df["type"] == "debit", "amount"].sum()

    
    transfers = df.loc[df["type"] == "transfer", "amount"].sum()

    
    net_balance = income - expenses

    
    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": net_balance,
        "total_transfers": transfers,
    }
