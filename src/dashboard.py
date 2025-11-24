# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import re
from pathlib import Path

# -----------------------------
# Configuración básica de la app
# -----------------------------
st.set_page_config(
    page_title="ROSA Finance",
    layout="wide",
    page_icon="💸",
)
st.title("ROSA Financial Dashboard")
st.markdown("#### Your money, beautifully understood")

# -----------------------------
# Carga de datos
# -----------------------------

# Carpeta raíz del repo: .../Agile_2025
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta al CSV dentro del repo
csv_path = BASE_DIR / "data" / "ROSA_financial_transactions.csv"

if not csv_path.exists():
    st.error(f"CSV not found at:\n{csv_path}")
    st.stop()


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Normalizar columnas esperadas
    if "date" not in df.columns:
        raise ValueError("CSV must contain a 'date' column")
    if "amount" not in df.columns:
        raise ValueError("CSV must contain an 'amount' column")

    # Convertir tipos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])

    # Si no existe columna 'type', la inferimos:
    # valores positivos = credit, negativos = debit
    if "type" not in df.columns:
        df["type"] = df["amount"].apply(lambda x: "credit" if x > 0 else "debit")

    # Descripción limpia
    desc_col = "description"
    if desc_col not in df.columns:
        # Creamos una descripción mínima si no existe
        df[desc_col] = ""

    df["clean_desc"] = df[desc_col].astype(str).str.lower()
    df["clean_desc"] = df["clean_desc"].str.replace(r"[\W_]+", " ", regex=True)

    # Categorías por palabras clave
    categories = {
        "Groceries": [
            "tesco",
            "sainsbury",
            "aldi",
            "lidl",
            "asda",
            "morrisons",
            "waitrose",
            "food",
            "supermarket",
        ],
        "Transport": [
            "uber",
            "tfl",
            "train",
            "tube",
            "bus",
            "petrol",
            "fuel",
            "shell",
            "bp",
        ],
        "Salary": ["salary", "payroll", "income", "wage", "payment from"],
        "Utilities": [
            "thames water",
            "british gas",
            "ee",
            "vodafone",
            "sky",
            "virgin",
            "council tax",
            "rent",
        ],
        "Entertainment": [
            "netflix",
            "spotify",
            "cinema",
            "restaurant",
            "pub",
            "bar",
            "cafe",
        ],
        "Shopping": ["amazon", "ebay", "boots", "primark", "online purchase"],
        "Health": ["boots", "pharmacy", "doctor", "hospital", "superdrug"],
        "Travel": ["ryanair", "easyjet", "booking.com", "hotel", "eurostar"],
    }

    df["Category"] = "Other"
    for cat, keywords in categories.items():
        pattern = "|".join(re.escape(k) for k in keywords)
        mask = df["clean_desc"].str.contains(pattern, case=False, na=False)
        df.loc[mask, "Category"] = cat

    return df


# Cargar datos
try:
    df = load_data(csv_path)
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

st.success(f"Loaded {len(df):,} transactions")

# -----------------------------
# Sidebar – Filtros
# -----------------------------
st.sidebar.header("Filters")

# Filtro por tipo (debit / credit)
types_available = sorted(df["type"].dropna().unique().tolist())
default_types = [t for t in types_available if t in ["debit", "credit"]] or types_available
types = st.sidebar.multiselect(
    "Type", options=types_available, default=default_types
)

# Rango de fechas
min_date = df["date"].min().date()
max_date = df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Filtro por categoría
categories_available = sorted(df["Category"].dropna().unique().tolist())
category_sel = st.sidebar.multiselect(
    "Category", options=categories_available, default=categories_available
)

# Aplicar filtros
filtered = df.copy()
if types:
    filtered = filtered[filtered["type"].isin(types)]
if category_sel:
    filtered = filtered[filtered["Category"].isin(category_sel)]

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["date"].dt.date >= start_date)
        & (filtered["date"].dt.date <= end_date)
    ]

if filtered.empty:
    st.warning("No transactions match the current filters.")
    st.stop()

# -----------------------------
# Métricas principales
# -----------------------------
income = filtered.loc[filtered["type"] == "credit", "amount"].sum()
expense = filtered.loc[filtered["type"] == "debit", "amount"].sum()
net = income + expense  # expense suele ser negativo

col1, col2, col3, col4 = st.columns(4)
col1.metric("Income", f"${income:,.0f}")
col2.metric("Expenses", f"${expense:,.0f}")
col3.metric("Net Flow", f"${net:,.0f}", delta=f"{net:+,.0f}")
col4.metric("Transactions", f"{len(filtered):,}")

st.markdown("---")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Overview", "Categories", "All Transactions"])

# -----------------------------
# Tab 1 – Overview
# -----------------------------
with tab1:
    c1, c2 = st.columns(2)

    # Serie temporal de flujo acumulado
    ts = (
        filtered.sort_values("date")
        .set_index("date")["amount"]
        .resample("D")
        .sum()
        .cumsum()
        .to_frame(name="cumulative_net")
    )

    with c1:
        st.subheader("Net worth over time")
        fig_net = px.line(
            ts,
            x=ts.index,
            y="cumulative_net",
            labels={"x": "Date", "cumulative_net": "Cumulative Net"},
        )
        fig_net.update_layout(height=400)
        st.plotly_chart(fig_net, use_container_width=True)

    # Ingresos y gastos por mes
    with c2:
        st.subheader("Monthly cash flow")
        monthly = filtered.copy()
        monthly["month"] = monthly["date"].dt.to_period("M").dt.to_timestamp()
        monthly_summary = (
            monthly.groupby(["month", "type"])["amount"]
            .sum()
            .reset_index()
        )
        fig_month = px.bar(
            monthly_summary,
            x="month",
            y="amount",
            color="type",
            barmode="group",
            labels={"month": "Month", "amount": "Amount", "type": "Type"},
        )
        fig_month.update_layout(height=400)
        st.plotly_chart(fig_month, use_container_width=True)

    st.subheader("Transactions over time")
    scatter_df = filtered.copy()
    fig_scatter = px.scatter(
        scatter_df.sort_values("date"),
        x="date",
        y="amount",
        color="type",
        hover_data=["Category", "description"],
        labels={"date": "Date", "amount": "Amount"},
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Tab 2 – Categories
# -----------------------------
with tab2:
    st.subheader("Spending by category (Debits)")

    expenses_only = filtered[filtered["type"] == "debit"].copy()
    if not expenses_only.empty:
        cat_expense = (
            expenses_only.groupby("Category")["amount"]
            .sum()
            .sort_values()
            .to_frame(name="total")
        )
        # Para el gráfico usamos valores absolutos
        cat_expense["total_abs"] = cat_expense["total"].abs()

        fig_expense = px.bar(
            cat_expense,
            x="total_abs",
            y=cat_expense.index,
            orientation="h",
            labels={
                "total_abs": "Total spent",
                "Category": "Category",
            },
            title="Where your money goes",
        )
        fig_expense.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_expense, use_container_width=True)
    else:
        st.info("No debit transactions in the selected filters.")

    st.subheader("Income sources (Credits)")
    income_only = filtered[filtered["type"] == "credit"].copy()
    if not income_only.empty:
        income_cat = (
            income_only.groupby("Category")["amount"]
            .sum()
            .sort_values(ascending=True)
            .to_frame(name="amount")
        )
        fig_income = px.bar(
            income_cat,
            x="amount",
            y=income_cat.index,
            orientation="h",
            labels={"amount": "Total income", "Category": "Category"},
        )
        fig_income.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_income, use_container_width=True)
    else:
        st.info("No credit transactions in the selected filters.")

# -----------------------------
# Tab 3 – All Transactions
# -----------------------------
with tab3:
    st.subheader("All filtered transactions")
    show_cols = ["date", "amount", "type", "Category", "description"]
    show_cols = [c for c in show_cols if c in filtered.columns]

    st.dataframe(
        filtered[show_cols].sort_values("date", ascending=False),
        use_container_width=True,
        height=700,
    )

st.balloons()

if __name__ == "__main__":
    # Streamlit lo ejecuta igual, pero esto permite correrlo como script
    pass
