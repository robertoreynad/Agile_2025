# dashboard.py ← Replace your entire file with this
import streamlit as st
import pandas as pd
import plotly.express as px
import re
from pathlib import Path

st.set_page_config(page_title="ROSA Finance", layout="wide", page_icon="money_with_wings")
st.title("ROSA Financial Dashboard")
st.markdown("#### Your money, beautifully understood")

# Load data
csv_path = Path("../data/ROSA_financial_transactions.csv").resolve()
if not csv_path.exists():
    st.error(f"CSV not found at:\n{csv_path}")
    st.stop()

@st.cache_data
def load_data():
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df = df.dropna(subset=['date', 'amount'])

    df['clean_desc'] = df['description'].astype(str).str.lower()
    df['clean_desc'] = df['clean_desc'].str.replace(r'[\W_]+', ' ', regex=True)

    categories = {
        'Groceries': ['tesco','sainsbury','aldi','lidl','asda','morrisons','waitrose','food','supermarket'],
        'Transport': ['uber','tfl','train','tube','bus','petrol','fuel','shell','bp'],
        'Salary': ['salary','payroll','income','wage','payment from'],
        'Utilities': ['thames water','british gas','ee','vodafone','sky','virgin','council tax','rent'],
        'Entertainment': ['netflix','spotify','cinema','restaurant','pub','bar','cafe'],
        'Shopping': ['amazon','ebay','boots','primark','online purchase'],
        'Health': ['boots','pharmacy','doctor','hospital','superdrug'],
        'Travel': ['ryanair','easyjet','booking.com','hotel','eurostar'],
    }

    df['Category'] = 'Other'
    for cat, keywords in categories.items():
        pattern = '|'.join(keywords)
        df.loc[df['clean_desc'].str.contains(pattern, case=False, na=False), 'Category'] = cat

    return df

df = load_data()
st.success(f"Loaded {len(df):,} transactions")

# Filters
with st.sidebar:
    st.header("Filters")
    types = st.multiselect("Type", options=df['type'].unique(), default=['debit','credit'])
    date_range = st.date_input("Date Range",
        value=(df['date'].min().date(), df['date'].max().date()),
        min_value=df['date'].min().date(),
        max_value=df['date'].max().date()
    )

filtered = df[
    df['type'].isin(types) &
    (df['date'].dt.date >= date_range[0]) &
    (df['date'].dt.date <= date_range[1])
].copy()

# Metrics
income = filtered[filtered['type']=='credit']['amount'].sum()
expense = filtered[filtered['type']=='debit']['amount'].sum()
net = income - expense

col1, col2, col3, col4 = st.columns(4)
col1.metric("Income", f"${income:,.0f}")
col2.metric("Expenses", f"${expense:,.0f}")
col3.metric("Net Flow", f"${net:,.0f}", delta=f"{net:+,.0f}")
col4.metric("Transactions", f"{len(filtered):,}")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Categories", "All Transactions"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig_pie = px.pie(filtered['type'].value_counts(), names=filtered['type'].value_counts().index,
                         title="By Transaction Type", color_discrete_sequence=["#ff6b6b","#4ecdc4","#45b7d1"])
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        daily = filtered.groupby('date')['amount'].sum().reset_index()
        fig_area = px.area(daily, x='date', y='amount', title="Daily Cash Flow")
        st.plotly_chart(fig_area, use_container_width=True)

with tab2:
    st.subheader("Spending Breakdown (Debits)")
    spending = filtered[filtered['type']=='debit'].groupby('Category')['amount'].sum().sort_values(ascending=True)
    fig_expense = px.bar(spending, x='amount', y=spending.index, orientation='h',  # ← Fixed line
                         title="Where your money goes", color='amount', color_continuous_scale="Reds")
    fig_expense.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_expense, use_container_width=True)

    st.subheader("Income Sources (Credits)")
    income_cat = filtered[filtered['type']=='credit'].groupby('Category')['amount'].sum().sort_values(ascending=True)
    fig_income = px.bar(income_cat, x='amount', y=income_cat.index, orientation='h',  # ← Fixed line
                        color='amount', color_continuous_scale="Greens")
    st.plotly_chart(fig_income, use_container_width=True)

with tab3:
    st.dataframe(filtered[['date','amount','type','Category','description']].sort_values('date', ascending=False),
                 use_container_width=True, height=700)

st.balloons()