import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Data persistence
BUDGET_FILE = "budget_data.json"
EXPENSE_FILE = "expenses_data.json"

# Load from JSON if available
def load_data():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'r') as f:
            st.session_state.categories = json.load(f)
    if os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'r') as f:
            st.session_state.expenses = json.load(f)

# Save to JSON
def save_data():
    with open(BUDGET_FILE, 'w') as f:
        json.dump(st.session_state.categories, f)
    with open(EXPENSE_FILE, 'w') as f:
        json.dump(st.session_state.expenses, f)

# Initialize session state
if 'categories' not in st.session_state:
    st.session_state.categories = [
        { 'name': '🏠 Rent', 'amount': 1150000 },
        { 'name': '💳 Debt repayment', 'amount': 380000 },
        { 'name': '👶 Daycare (Mango)', 'amount': 300000 },
        { 'name': '🏋️ Gym', 'amount': 92000 },
        { 'name': '🌐 Internet', 'amount': 98000 },
        { 'name': '🐶 Dog (basic)', 'amount': 60000 },
        { 'name': '🚌 Transport', 'amount': 120000 },
        { 'name': '🧴 Personal care', 'amount': 80000 },
        { 'name': '🥦 Groceries', 'amount': 450000 },
        { 'name': '🍔 Eating out', 'amount': 250000 },
    ]

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

load_data()

st.set_page_config(page_title="Monthly Budget", layout="wide")

# Sidebar controls
with st.sidebar:
    st.title("📝 Budget Controls")
    st.subheader("Adjust Monthly Budget")
    for category in st.session_state.categories:
        category['amount'] = st.number_input(
            category['name'], value=int(category.get('amount', 0)), step=1000, format="%d"
        )
    if st.button("💾 Save Budget"):
        save_data()
        st.success("Budget changes saved!")

    st.markdown("---")
    st.subheader("➕ Add New Expense")
    expense_category = st.selectbox("Select Category", [cat['name'] for cat in st.session_state.categories])
    expense_amount = st.number_input("Amount", min_value=0, step=1000)
    if st.button("Add Expense"):
        st.session_state.expenses.append({"category": expense_category, "amount": expense_amount})
        save_data()
        st.success(f"Added {expense_amount} to {expense_category}")

st.title("💰 Monthly Budget Dashboard")

# Budget calculations
budget = 3600000
category_totals = {cat['name']: cat['amount'] for cat in st.session_state.categories}
category_spending = {cat['name']: 0 for cat in st.session_state.categories}

for expense in st.session_state.expenses:
    if expense['category'] in category_spending:
        category_spending[expense['category']] += expense['amount']

# Totals
total_allocated = sum(cat['amount'] for cat in st.session_state.categories)
total_spent = sum(category_spending.values())
remaining = budget - total_allocated

# KPIs
st.markdown(f"### 🧾 Allocated: {total_allocated:,.0f} / {budget:,.0f} COP")
st.markdown(f"### 💸 Spent: {total_spent:,.0f} COP")
st.markdown(f"### 💵 Remaining Allocation Room: {remaining:,.0f} COP")

# Pie chart
fig = px.pie(
    names=[cat['name'] for cat in st.session_state.categories],
    values=[cat['amount'] for cat in st.session_state.categories],
    title="📊 Monthly Budget Distribution",
    hole=0.3
)
st.plotly_chart(fig, use_container_width=True)

# Progress bars
st.subheader("📊 Spending Progress by Category")
for cat in st.session_state.categories:
    spent = category_spending.get(cat['name'], 0)
    budgeted = cat['amount']
    percent = min(spent / budgeted, 1.0) if budgeted else 0
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{cat['name']}**: {spent:,.0f} / {budgeted:,.0f} COP")
        st.progress(percent)
    with col2:
        st.markdown(f"{percent * 100:.1f}%")

# Download button
if st.button("📁 Export Budget & Expenses to CSV"):
    df_budget = pd.DataFrame(st.session_state.categories)
    df_expenses = pd.DataFrame(st.session_state.expenses)
    df_budget.to_csv("monthly_budget.csv", index=False)
    df_expenses.to_csv("monthly_expenses.csv", index=False)
    st.success("CSV files saved: monthly_budget.csv & monthly_expenses.csv")
 
