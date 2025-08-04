import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# Initialize session state before loading
if 'categories' not in st.session_state:
    st.session_state.categories = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Now safe to load data
load_data()

# If no data was loaded, set default categories
if not st.session_state.categories:
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
if 'categories' not in st.session_state or 'expenses' not in st.session_state:
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
    st.session_state.expenses = []
load_data()

st.set_page_config(page_title="Monthly Budget", layout="wide")

with st.sidebar:
    st.title("📝 Budget Sidebar")
    st.subheader("Adjust Your Categories")
    for category in st.session_state.categories:
        category['amount'] = st.number_input(
            category['name'], value=int(category.get('amount', 0)), step=1000, format="%d"
        )
    if st.button("💾 Save Changes"):
        save_data()
        st.success("Changes saved!")

st.title("💰 Monthly Budget Tracker")

# Total calculation
budget = 3600000
category_totals = {cat['name']: cat['amount'] for cat in st.session_state.categories}
category_spending = {cat['name']: 0 for cat in st.session_state.categories}

# Input new expense
st.subheader("➕ Add New Expense")
expense_category = st.selectbox("Select Category", [cat['name'] for cat in st.session_state.categories])
expense_amount = st.number_input("Amount", min_value=0, step=1000)
if st.button("Add Expense"):
    st.session_state.expenses.append({"category": expense_category, "amount": expense_amount})
    save_data()
    st.success(f"Added {expense_amount} to {expense_category}")

# Aggregate spending
for expense in st.session_state.expenses:
    category_spending[expense['category']] += expense['amount']

total = sum(cat['amount'] for cat in st.session_state.categories)
remaining = budget - total

st.markdown(f"### 📈 Used Budget: {total:,.0f} / {budget:,.0f} COP")
st.markdown(f"### 💵 Remaining: {remaining:,.0f} COP")

# Pie chart with Plotly
labels = [cat['name'] for cat in st.session_state.categories]
data = [cat['amount'] for cat in st.session_state.categories]

fig = px.pie(
    names=labels,
    values=data,
    title="📊 Monthly Budget Breakdown",
    hole=0.3
)
st.plotly_chart(fig, use_container_width=True)

# Show progress bars per category
st.subheader("📊 Budget Progress by Category")
for cat in st.session_state.categories:
    spent = category_spending[cat['name']]
    budgeted = cat['amount']
    percent = min(spent / budgeted, 1.0) if budgeted else 0
    st.markdown(f"**{cat['name']}**: {spent:,.0f} / {budgeted:,.0f} COP")
    st.progress(percent)

# Export Data
if st.button("📁 Export Budget to CSV"):
    df = pd.DataFrame(st.session_state.categories)
    df.to_csv("monthly_budget.csv", index=False)
    st.success("File saved as monthly_budget.csv")
