"""Entry point for the ROSA Financial Transactions Summary Tool."""

from .summary_tool import load_transactions, summarize_totals


def main():
    # Example placeholder path; update as needed
    csv_path = "data/financial_transactions.csv"

    print("ROSA – Financial Transactions Summary Tool")
    print("Loading transactions from:", csv_path)

    try:
        df = load_transactions(csv_path)
    except FileNotFoundError:
        print("ERROR: Dataset not found. Please place 'financial_transactions.csv' in the 'data/' folder.")
        return

    summary = summarize_totals(df)

    print("\n=== Summary of Totals ===")
    print(f"Total income: {summary['total_income']}")
    print(f"Total expenses: {summary['total_expenses']}")
    print(f"Net balance: {summary['net_balance']}")


if __name__ == "__main__":
    main()
