import streamlit as st
import pandas as pd
import plotly.express as px

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

st.set_page_config(page_title="Monthly Budget", layout="wide")

with st.sidebar:
    st.title("📝 Budget Sidebar")
    st.subheader("Adjust Your Categories")
    for category in st.session_state.categories:
        category['amount'] = st.number_input(
            category['name'], value=category['amount'], step=1000, format="%d"
        )

st.title("💰 Monthly Budget Tracker")

# Total calculation
budget = 3600000
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

# Export Data
if st.button("💾 Export Budget to CSV"):
    df = pd.DataFrame(st.session_state.categories)
    df.to_csv("monthly_budget.csv", index=False)
    st.success("File saved as monthly_budget.csv")
