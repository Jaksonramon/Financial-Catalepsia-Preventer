import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

st.title("💰 Monthly Budget Tracker")
st.subheader("Edit your monthly budget categories")

# Sidebar input for each category
for category in st.session_state.categories:
    category['amount'] = st.number_input(
        category['name'], value=category['amount'], step=1000, format="%d"
    )

# Total calculation
budget = 3600000
total = sum(cat['amount'] for cat in st.session_state.categories)
remaining = budget - total

st.markdown(f"### 📈 Used Budget: {total:,.0f} / {budget:,.0f} COP")
st.markdown(f"### 💵 Remaining: {remaining:,.0f} COP")

# Pie chart
labels = [cat['name'] for cat in st.session_state.categories]
data = [cat['amount'] for cat in st.session_state.categories]

fig, ax = plt.subplots()
ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Export Data
if st.button("💾 Export Budget to CSV"):
    df = pd.DataFrame(st.session_state.categories)
    df.to_csv("monthly_budget.csv", index=False)
    st.success("File saved as monthly_budget.csv")
