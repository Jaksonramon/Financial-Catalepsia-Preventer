import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define initial categories and budgets
if 'categories' not in st.session_state:
    st.session_state.categories = {
        '🏠 Rent': 1150000,
        '💳 Debt repayment': 380000,
        '👶 Daycare (Mango)': 300000,
        '🏋️ Gym': 92000,
        '🌐 Internet': 98000,
        '🐶 Dog (basic)': 60000,
        '🚌 Transport': 120000,
        '🧴 Personal care': 80000,
        '🥦 Groceries': 450000,
        '🍔 Eating out': 250000,
    }

# Sidebar budget input
st.sidebar.title("💰 Monthly Budget Settings")
total_budget = 3600000
for category in st.session_state.categories:
    st.session_state.categories[category] = st.sidebar.number_input(
        f"{category} Budget (COP)", 
        value=st.session_state.categories[category], 
        step=1000
    )

# Expense entry
st.title("📘 Financial Catalepsia Preventer")
st.subheader("Add a New Expense")

with st.form("expense_form", clear_on_submit=True):
    category = st.selectbox("Category", list(st.session_state.categories.keys()))
    amount = st.number_input("Amount Spent (COP)", min_value=0, step=1000)
    submitted = st.form_submit_button("➕ Add Expense")

    if submitted:
        if "expenses" not in st.session_state:
            st.session_state.expenses = []
        st.session_state.expenses.append({"Category": category, "Amount": amount})

# Expenses table
st.subheader("📜 Expense Log")
if "expenses" in st.session_state and st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(df)

    # Pie chart per category
    st.subheader("📊 Spending Breakdown")
    category_sums = df.groupby("Category")["Amount"].sum()
    fig, ax = plt.subplots()
    ax.pie(category_sums, labels=category_sums.index, autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # Remaining per category
    st.subheader("📈 Category Progress")
    for category in st.session_state.categories:
        spent = category_sums.get(category, 0)
        budget = st.session_state.categories[category]
        percent = spent / budget * 100 if budget else 0
        st.write(f"**{category}**: {spent:,.0f} / {budget:,.0f} COP ({percent:.1f}%)")
        st.progress(min(int(percent), 100))
else:
    st.info("No expenses recorded yet. Add some above!")
