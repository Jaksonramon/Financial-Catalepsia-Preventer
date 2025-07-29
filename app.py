import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Financial Catalepsia Preventer", layout="wide")

# --- Fixed Categories ---
FIXED_CATEGORIES = {
    "Rent": 1000000,
    "Utilities": 250000,
    "Groceries": 500000
}

# --- Sidebar: Monthly Selector & Income ---
st.sidebar.title("📅 Month & Income")
selected_month = st.sidebar.selectbox("Select month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=datetime.datetime.now().month - 1)
selected_year = st.sidebar.number_input("Year", value=datetime.datetime.now().year, min_value=2000, max_value=2100, step=1)
monthly_income = st.sidebar.number_input("Your Monthly Income", min_value=0, step=10000)

# --- Sidebar: Manual Variable Entry ---
st.sidebar.title("💸 Variable Expenses")
st.sidebar.write("Enter categories and how much they’ve drained from you.")

num_rows = st.sidebar.number_input("How many expenses do you want to enter?", min_value=1, max_value=50, value=5)

variable_data = {
    "Category": [],
    "Amount": [],
    "Budget": []
}

for i in range(num_rows):
    cat = st.sidebar.text_input(f"Category #{i+1}", key=f"cat_{i}")
    amt = st.sidebar.number_input(f"Amount #{i+1}", min_value=0, step=1000, key=f"amt_{i}")
    bud = st.sidebar.number_input(f"Budget for {cat if cat else f'Unnamed {i+1}'}", min_value=0, step=1000, key=f"bud_{i}")
    variable_data["Category"].append(cat if cat else f"Unnamed {i+1}")
    variable_data["Amount"].append(amt)
    variable_data["Budget"].append(bud)

# --- Create DataFrame from input ---
df = pd.DataFrame(variable_data)

# --- Main Page ---
st.title("💸 Financial Catalepsia Preventer")
st.caption(f"Tracking your doom for {selected_month}, {selected_year}")

st.subheader("📋 Your Entered Expenses")
st.dataframe(df)

# --- Compute Totals ---
variable_total = df["Amount"].sum()
fixed_total = sum(FIXED_CATEGORIES.values())
total_spent = variable_total + fixed_total
remaining = monthly_income - total_spent

st.subheader("📊 Summary")
st.write(f"**Total Variable Expenses:** ${variable_total:,.0f}")
st.write(f"**Total Fixed Costs:** ${fixed_total:,.0f}")
st.write(f"**Total Spent This Month:** ${total_spent:,.0f}")
st.write(f"**Remaining Balance:** ${remaining:,.0f}")

# --- Overspending Alert ---
if monthly_income > 0 and remaining < 0:
    st.error("🚨 You're spending more than you earn. Bravo.")
elif monthly_income > 0 and remaining < monthly_income * 0.1:
    st.warning("⚠️ You're hanging by a thread. Enjoy your instant coffee.")
else:
    st.success("✅ You might survive another month. Statistically unlikely, though.")

# --- Charts and Breakdown ---
category_summary = df.groupby("Category")["Amount"].sum()
category_summary = category_summary.append(pd.Series(FIXED_CATEGORIES))
st.write("**Spending by Category (including fixed):**")
st.bar_chart(category_summary.sort_values(ascending=False))

# --- Budget Evaluation ---
st.subheader("🎯 Budget Feedback")
for index, row in df.iterrows():
    if row["Budget"] > 0:
        if row["Amount"] > row["Budget"]:
            st.write(f"- **{row['Category']}**: Overspent by ${row['Amount'] - row['Budget']:.0f}. _What a surprise._")
        elif row["Amount"] == row["Budget"]:
            st.write(f"- **{row['Category']}**: Met your exact budget. _Congratulations on your mediocrity._")
        else:
            st.write(f"- **{row['Category']}**: Under budget by ${row['Budget'] - row['Amount']:.0f}. _Must’ve forgotten something._")

# --- Bleak Message ---
st.markdown("---")
st.write("💀 _You are probably still hemorrhaging money. But at least now you know where._")
