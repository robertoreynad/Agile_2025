from .summary_tool import load_transactions, summarize_totals


def main():
    # data/ROSA_financial_transactions.csv
    csv_path = "data/ROSA_financial_transactions.csv"

    print("ROSA – Financial Transactions Summary Tool")
    print("Loading transactions from:", csv_path)

    try:
        df = load_transactions(csv_path)
    except FileNotFoundError:
        print("ERROR: Dataset not found. Please place the CSV file in the 'data/' folder.")
        return

    
    summary = summarize_totals(df)

    
    print("\n=== Summary of Totals ===")
    print(f"Total income:   {summary['total_income']:.2f}")
    print(f"Total expenses: {summary['total_expenses']:.2f}")
    print(f"Net balance:    {summary['net_balance']:.2f}")
    print(f"Transfers:      {summary['total_transfers']:.2f}")



if __name__ == "__main__":
    main()
