import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Financial Catalepsia Preventer", layout="wide")

# --- Sidebar: Month and Year Selection ---
st.sidebar.title("Select Month")
today = datetime.date.today()
def_month = today.month

year = st.sidebar.selectbox("Year", list(range(2020, today.year + 1))[::-1], index=0)
month = st.sidebar.selectbox("Month", list(range(1, 13)), index=def_month - 1)

# --- Fixed Categories ---
FIXED_CATEGORIES = {
    "Rent": 1000000,
    "Utilities": 250000,
    "Groceries": 500000
}

# --- Manual Entry Table for Variable Expenses ---
st.title("💸 Financial Catalepsia Preventer")
st.write("Helps you identify where you’re bleeding money before it kills your will to live.")

st.subheader("📥 Enter Your Variable Expenses")
num_rows = st.number_input("How many expenses do you want to enter?", min_value=1, max_value=50, value=5)

variable_data = {
    "Category": [],
    "Amount": []
}

for i in range(num_rows):
    col1, col2 = st.columns([2, 1])
    with col1:
        cat = st.text_input(f"Category #{i+1}", key=f"cat_{i}")
    with col2:
        amt = st.number_input(f"Amount #{i+1}", min_value=0, step=1000, key=f"amt_{i}")
    variable_data["Category"].append(cat if cat else f"Unnamed {i+1}")
    variable_data["Amount"].append(amt)

# --- Create DataFrame from input ---
df = pd.DataFrame(variable_data)

# --- Show Entered Data ---
st.subheader(f"📋 Your Expenses for {year}-{month:02d}")
st.dataframe(df)

# --- Compute Total ---
variable_total = df["Amount"].sum()
fixed_total = sum(FIXED_CATEGORIES.values())
total_spent = variable_total + fixed_total

st.subheader("📊 Summary")
st.write(f"**Total Variable Expenses:** ${variable_total:,.0f}")
st.write(f"**Total Fixed Costs:** ${fixed_total:,.0f}")
st.write(f"**Total Spent in {year}-{month:02d}:** ${total_spent:,.0f}")

# --- Charts and Breakdown ---
category_summary = df.groupby("Category")["Amount"].sum()
category_summary = category_summary.append(pd.Series(FIXED_CATEGORIES))
st.write("**Spending by Category (including fixed):**")
st.bar_chart(category_summary.sort_values(ascending=False))

# --- Bleak Message ---
st.markdown("---")
st.write("💀 _You are probably still hemorrhaging money. But at least now you know where._")
