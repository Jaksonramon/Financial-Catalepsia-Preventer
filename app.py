import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Financial Catalepsia Preventer", layout="wide")

# --- Sidebar: Monthly Settings ---
st.sidebar.title("📅 Monthly Setup")
st.sidebar.write("Set your monthly context.")

month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
year = st.sidebar.number_input("Enter Year", min_value=2000, max_value=2100, value=datetime.datetime.now().year)
income = st.sidebar.number_input("Monthly Income", min_value=0, step=1000)

# --- Fixed Categories (Annual costs divided by 12) ---
st.sidebar.subheader("📌 Fixed Costs (Annual, divided by 12)")
FIXED_CATEGORIES = {
    "Rent": 12000000 // 12,
    "Utilities": 3000000 // 12,
    "Groceries": 6000000 // 12
}

# --- Expense Entry ---
st.title("💸 Financial Catalepsia Preventer")
st.write("Helps you identify where you’re bleeding money before it kills your will to live.")

st.subheader("➕ Add Variable Expense")

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

with st.form("add_expense"):
    category = st.selectbox("Select a Category", ["Transport", "Eating Out", "Entertainment", "Health", "Other"])
    amount = st.number_input("Amount", min_value=0, step=1000)
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        st.session_state.expenses.append({"Category": category, "Amount": amount})

# --- Display Expenses ---
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.subheader("📋 Your Entered Expenses")
    st.dataframe(df)
else:
    st.info("No expenses added yet.")

# --- Compute Totals ---
variable_total = sum(e['Amount'] for e in st.session_state.expenses)
fixed_total = sum(FIXED_CATEGORIES.values())
total_spent = variable_total + fixed_total
remaining = income - total_spent

st.subheader("📊 Summary")
st.write(f"**Total Variable Expenses:** ${variable_total:,.0f}")
st.write(f"**Total Fixed Costs:** ${fixed_total:,.0f}")
st.write(f"**Total Spent This Month:** ${total_spent:,.0f}")
st.write(f"**Remaining After All Expenses:** ${remaining:,.0f}")

# --- Charts and Breakdown ---
if st.session_state.expenses:
    df_summary = pd.DataFrame(st.session_state.expenses).groupby("Category")["Amount"].sum()
    full_summary = df_summary.append(pd.Series(FIXED_CATEGORIES))
    st.write("**Spending by Category (including fixed):**")
    st.bar_chart(full_summary.sort_values(ascending=False))

# --- Bleak Message ---
st.markdown("---")
st.write("💀 _You are probably still hemorrhaging money. But at least now you know where._")
