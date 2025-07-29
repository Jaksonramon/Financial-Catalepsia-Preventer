import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Financial Catalepsia Preventer", layout="wide")

# --- Fixed Categories (Annual) ---
FIXED_CATEGORIES = {
    "Rent": 12000000,        # Annual
    "Utilities": 3000000,    # Annual
    "Groceries": 6000000     # Annual
}

# --- Sidebar: Monthly Budget Entry ---
st.sidebar.title("📆 Monthly Setup")
monthly_income = st.sidebar.number_input("Monthly Income", min_value=0, step=50000, value=3000000)

st.sidebar.markdown("---")

# --- Add Expense Entry ---
st.sidebar.title("➕ Add an Expense")
category = st.sidebar.selectbox("Select Category", ["Food", "Transport", "Entertainment", "Health", "Other"])
amount = st.sidebar.number_input("Amount", min_value=0, step=1000)
add_expense = st.sidebar.button("Add Expense")

# --- Session State to Store Expenses ---
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if add_expense:
    st.session_state.expenses.append({"Category": category, "Amount": amount})

# --- Create DataFrame ---
df = pd.DataFrame(st.session_state.expenses)

# --- Main Page ---
st.title("💸 Financial Catalepsia Preventer")
st.write("Helps you identify where you’re bleeding money before it kills your will to live.")

st.subheader("📋 Your Entered Expenses")
if df.empty:
    st.write("No expenses entered yet.")
else:
    st.dataframe(df)

    # --- Summary Calculations ---
    variable_total = df["Amount"].sum()
    fixed_monthly_total = sum(FIXED_CATEGORIES.values()) / 12
    total_spent = variable_total + fixed_monthly_total
    remaining = monthly_income - total_spent

    st.subheader("📊 Summary")
    st.write(f"**Total Variable Expenses:** ${variable_total:,.0f}")
    st.write(f"**Monthly Share of Fixed Costs:** ${fixed_monthly_total:,.0f}")
    st.write(f"**Total Spent This Month:** ${total_spent:,.0f}")
    st.write(f"**Remaining Budget:** ${remaining:,.0f}")

    # --- Charts and Breakdown ---
    category_summary = df.groupby("Category")["Amount"].sum()
    st.write("**Spending by Category:**")
    st.bar_chart(category_summary.sort_values(ascending=False))

st.markdown("---")
st.write("💀 _You are probably still hemorrhaging money. But at least now you know where._")
