"""Core functions for the ROSA Financial Transactions Summary Tool.

Este módulo contiene las funciones principales para:
- Cargar el dataset de transacciones desde un archivo CSV.
- Calcular los totales de ingresos, gastos, balance neto y transferencias.

Se asume que el CSV tiene, al menos, las columnas:
- 'amount' (monto numérico)
- 'type'   (por ejemplo: 'credit', 'debit', 'transfer')
"""

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
    # Leemos el archivo CSV completo en un DataFrame de pandas
    df = pd.read_csv(csv_path)

    # Si existe una columna 'date', intentamos convertirla a tipo datetime
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
    # Validamos que existan las columnas básicas
    if "amount" not in df.columns:
        raise ValueError("Expected an 'amount' column in the dataset.")
    if "type" not in df.columns:
        raise ValueError("Expected a 'type' column in the dataset.")

    # Ingresos: sumamos 'amount' donde type == 'credit'
    income = df.loc[df["type"] == "credit", "amount"].sum()

    # Gastos: sumamos 'amount' donde type == 'debit'
    expenses = df.loc[df["type"] == "debit", "amount"].sum()

    # Transferencias: sumamos 'amount' donde type == 'transfer'
    transfers = df.loc[df["type"] == "transfer", "amount"].sum()

    # Definimos el balance neto como ingresos - gastos
    net_balance = income - expenses

    # Devolvemos un diccionario con los resultados
    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": net_balance,
        "total_transfers": transfers,
    }
