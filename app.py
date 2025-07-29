import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import altair as alt

# ----------------------------
# App Styling
# ----------------------------
st.set_page_config(page_title="My Budget Tracker 💸", layout="centered")
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        font-family: monospace !important;
    }
    .main {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# Load or Initialize Data
# ----------------------------
data_file = "expenses.json"
if os.path.exists(data_file):
    with open(data_file, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

# ----------------------------
# Budget Setup
# ----------------------------
st.sidebar.title("📅 Monthly Setup")
income = st.sidebar.number_input("Monthly Income", value=3600000, step=10000)

st.sidebar.subheader("Fixed Expenses")
fixed_expenses = {}
for label, default in {
    "Rent": 1150000,
    "Debt Repayment": 380000,
    "Daycare": 300000,
    "Gym": 90000,
    "Internet": 100000,
    "Dog": 60000,
    "Transport": 100000,
    "Pills": 60000
}.items():
    fixed_expenses[label] = st.sidebar.number_input(f"{label}", value=default, step=10000)

flexible_categories = ["Groceries", "Eating Out", "Other"]
budget_flexible = {}
st.sidebar.subheader("Flexible Budgets")
for cat in flexible_categories:
    budget_flexible[cat] = st.sidebar.number_input(f"{cat}", value=200000, step=10000)

# ----------------------------
# Add Expense
# ----------------------------
st.title("💳 Daily Expense Tracker")
with st.form("expense_form"):
    date = st.date_input("Date", value=datetime.today())
    category = st.selectbox("Category", list(fixed_expenses.keys()) + flexible_categories)
    amount = st.number_input("Amount", step=1000)
    note = st.text_input("Note (optional)")
    submit = st.form_submit_button("Add Expense")

if submit:
    new_expense = pd.DataFrame([[date.strftime('%Y-%m-%d'), category, amount, note]], columns=["Date", "Category", "Amount", "Note"])
    df = pd.concat([df, new_expense], ignore_index=True)
    with open(data_file, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)
    st.success("Expense added!")

# ----------------------------
# Summary and Visuals
# ----------------------------
st.header("📊 Monthly Summary")

month = datetime.today().month
df["Date"] = pd.to_datetime(df["Date"])
df_month = df[df["Date"].dt.month == month]

summary = df_month.groupby("Category")["Amount"].sum().reset_index()
summary = summary.sort_values(by="Amount", ascending=False)

# Totals and Remaining
fixed_total = sum(fixed_expenses.values())
budget_total = fixed_total + sum(budget_flexible.values())
total_spent = summary["Amount"].sum()
remaining = income - total_spent

col1, col2, col3 = st.columns(3)
col1.metric("💸 Total Spent", f"${int(total_spent):,}")
col2.metric("🏠 Fixed Expenses", f"${int(fixed_total):,}")
col3.metric("💰 Remaining", f"${int(remaining):,}")

# Progress bar for overall budget usage
st.progress(min(total_spent / income, 1.0))

# Bar chart
bar_chart = alt.Chart(summary).mark_bar().encode(
    x=alt.X('Category', sort='-y'),
    y='Amount',
    color='Category'
).properties(width=600)

st.altair_chart(bar_chart, use_container_width=True)

st.write("### Detailed Log")
st.dataframe(df_month.sort_values(by="Date", ascending=False))
