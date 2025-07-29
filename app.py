
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Budget Tracker", layout="centered")

st.markdown("""
    <style>
        * {
            font-family: monospace;
        }
        .stButton > button {
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
            border: none;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "expenses.json"
FIXED_CATEGORIES = {
    "Rent": 800000,
    "Transport": 130000,
    "Internet": 70000,
    "Pharmaceutical": 60000,
}

# Initialize or load data
if Path(DATA_FILE).exists():
    df = pd.read_json(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])

# Header
st.title("💰 Monthly Budget Tracker")

# Input fields
with st.form("expense_form"):
    st.subheader("➕ Add New Expense")
    category = st.selectbox("Select a category", list(FIXED_CATEGORIES.keys()) + ["Groceries", "Eating Out", "Other"])
    amount = st.number_input("Amount", min_value=0)
    note = st.text_input("Note (optional)")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    new_expense = {
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Amount": amount,
        "Note": note,
    }
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_json(DATA_FILE, orient="records", indent=4)
    st.success("Expense added!")

# Clear entries section
st.subheader("🧹 Manage Entries")
col1, col2 = st.columns(2)
with col1:
    if st.button("Undo Last Entry"):
        if not df.empty:
            df = df[:-1]
            df.to_json(DATA_FILE, orient="records", indent=4)
            st.warning("Last entry removed.")
        else:
            st.info("No entries to remove.")

with col2:
    if st.button("Clear All Expenses"):
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
        df.to_json(DATA_FILE, orient="records", indent=4)
        st.error("All data cleared.")

# Budget Summary
st.subheader("📊 Budget Overview")
total_budget = 1200000  # Set your total monthly budget here
total_spent = df["Amount"].sum() + sum(FIXED_CATEGORIES.values())
remaining_budget = total_budget - total_spent
progress = total_spent / total_budget

st.metric("Total Budget", f"${total_budget:,.0f}")
st.metric("Total Spent", f"${total_spent:,.0f}")
st.metric("Remaining", f"${remaining_budget:,.0f}")

st.progress(min(progress, 1.0))

# Display Data Table
st.subheader("🧾 Expense Log")
st.dataframe(df)
