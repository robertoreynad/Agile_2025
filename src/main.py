"""Entry point for the ROSA Financial Transactions Summary Tool.

Este módulo actúa como punto de entrada de la herramienta:
- Define la ruta del CSV.
- Llama a las funciones para cargar los datos y generar el resumen.
- Imprime los resultados en consola.
"""

from .summary_tool import load_transactions, summarize_totals


def main():
    # Ruta del archivo CSV dentro de la carpeta 'data'.
    # Asegúrate de que el archivo exista con este nombre:
    # data/ROSA_financial_transactions.csv
    csv_path = "data/ROSA_financial_transactions.csv"

    print("ROSA – Financial Transactions Summary Tool")
    print("Loading transactions from:", csv_path)

    try:
        # Cargamos el DataFrame con todas las transacciones
        df = load_transactions(csv_path)
    except FileNotFoundError:
        # Mensaje de error claro si el archivo no se encuentra
        print("ERROR: Dataset not found. Please place the CSV file in the 'data/' folder.")
        return

    # Obtenemos el resumen de totales (ingresos, gastos, etc.)
    summary = summarize_totals(df)

    # Mostramos los resultados de manera formateada
    print("\n=== Summary of Totals ===")
    print(f"Total income:   {summary['total_income']:.2f}")
    print(f"Total expenses: {summary['total_expenses']:.2f}")
    print(f"Net balance:    {summary['net_balance']:.2f}")
    print(f"Transfers:      {summary['total_transfers']:.2f}")


# Permite ejecutar este archivo directamente con:
# python -m src.main
if __name__ == "__main__":
    main()
