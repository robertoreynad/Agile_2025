"""
Le Crexs Financial Dashboard - Interactive Version
- Monthly & Yearly trends
- Interactive tables (Pandas Styler)
- Interactive charts (Plotly)
- Top 15 customers by credit/debit with bar charts
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# -------------------------------
# Load and prepare data
# -------------------------------
def load_data(csv_path: str | Path = "../data/ROSA_financial_transactions.csv") -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["year_month"] = df["date"].dt.strftime("%Y-%m")
    df["year"] = df["date"].dt.year
    
    df["income"] = df.apply(lambda x: x["amount"] if x["type"] == "credit" else 0, axis=1)
    df["expense"] = df.apply(lambda x: x["amount"] if x["type"] in ["debit", "transfer"] else 0, axis=1)
    
    return df

# -------------------------------
# Monthly & Yearly Summary
# -------------------------------
def monthly_yearly_summary(df: pd.DataFrame):
    # Monthly
    monthly = df.groupby("year_month").agg(
        Income=("income", "sum"),
        Expense=("expense", "sum")
    ).round(2)
    monthly["Net"] = monthly["Income"] - monthly["Expense"]
    monthly = monthly.reset_index()

    # Yearly
    yearly = df.groupby("year").agg(
        Income=("income", "sum"),
        Expense=("expense", "sum")
    ).round(2)
    yearly["Net"] = yearly["Income"] - yearly["Expense"]
    yearly = yearly.reset_index()

    return monthly, yearly

# -------------------------------
# Customer Analysis
# -------------------------------
def customer_analysis(df: pd.DataFrame):
    summary = df.groupby("customer_id").agg(
        transactions=("transaction_id", "count"),
        total_credit=("income", "sum"),
        total_debit=("expense", "sum")
    ).round(2).reset_index()

    summary["net_balance"] = summary["total_credit"] - summary["total_debit"]

    top_credit = summary.nlargest(15, "total_credit").copy()
    top_debit = summary.nlargest(15, "total_debit").copy()

    return summary, top_credit, top_debit

# -------------------------------
# Interactive Visualizations
# -------------------------------
def plot_monthly_trend(monthly: pd.DataFrame):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly["year_month"], y=monthly["Income"], name="Income", marker_color="#32B1CD"))
    fig.add_trace(go.Bar(x=monthly["year_month"], y=-monthly["Expense"], name="Expense", marker_color="#ff6b6b"))
    fig.add_trace(go.Scatter(x=monthly["year_month"], y=monthly["Net"], mode="lines+markers", name="Net Balance", line=dict(color="#A1DBE8", width=4)))

    fig.update_layout(
        title="Monthly Income vs Expense (6 Years)",
        xaxis_title="Year-Month",
        yaxis_title="Amount ($)",
        barmode="relative",
        legend=dict(x=0, y=1.1, orientation="h"),
        height=600
    )
    fig.show()

def plot_yearly_trend(yearly: pd.DataFrame):
    fig = px.bar(yearly, x="year", y=["Income", "Expense"], title="Yearly Income vs Expense",
                 color_discrete_map={"Income": "#32B1CD", "Expense": "#ff6b6b"}, barmode="group")
    fig.add_scatter(x=yearly["year"], y=yearly["Net"], mode="lines+markers", name="Net", line=dict(color="white", width=4))
    fig.update_layout(height=500)
    fig.show()

def plot_top_customers(top_credit, top_debit):
    fig = go.Figure()
    fig.add_trace(go.Bar(y=top_credit["customer_id"].astype(str), x=top_credit["total_credit"],
                         name="Top Credit", orientation="h", marker_color="#32B1CD"))
    fig.add_trace(go.Bar(y=top_debit["customer_id"].astype(str), x=-top_debit["total_debit"],
                         name="Top Debit", orientation="h", marker_color="#ff6b6b"))
    
    fig.update_layout(
        title="Top 15 Customers: Credit vs Debit",
        xaxis_title="Amount ($)",
        yaxis_title="Customer ID",
        barmode="relative",
        height=600
    )
    fig.show()

# -------------------------------
# Main Execution
# -------------------------------
if __name__ == "__main__":
    print("Le Crexs Financial Dashboard - Loading data...\n")
    df = load_data()

    monthly, yearly = monthly_yearly_summary(df)
    full_summary, top_credit, top_debit = customer_analysis(df)

    # Interactive tables
    print("Monthly Summary (first 10 rows):")
    display(monthly.head(10).style.format({"Income": "${:,.2f}", "Expense": "${:,.2f}", "Net": "${:,.2f}"}))

    print(f"\nTotal Unique Customers: {len(full_summary)}")
    print(f"Total Income: ${monthly['Income'].sum():,.2f}")
    print(f"Total Expense: ${monthly['Expense'].sum():,.2f}")
    print(f"Net Profit: ${monthly['Net'].sum():,.2f}\n")

    # Interactive charts
    plot_monthly_trend(monthly)
    plot_yearly_trend(yearly)
    plot_top_customers(top_credit, top_debit)

    print("All interactive charts opened in your browser!")