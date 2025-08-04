import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
streamlit
pandas
plotly


# --- Page Config ---
st.set_page_config(page_title="Budget Nostalgia", layout="wide")
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Nunito', sans-serif;
            background-color: #fdf6e3;
            color: #4b3e2a;
        }

        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #3e3621;
        }

        .sidebar-section {
            background-color: #f4ecd8;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #d8c9aa;
        }

        .main-section {
            background-color: #f8f1e3;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #d8c9aa;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.title("📆 Monthly Budget Setup")
monthly_budget = st.sidebar.number_input("Enter Your Monthly Budget", min_value=0, step=50000, value=3000000)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- Initialize session state for expenses ---
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# --- Main Interface ---
st.markdown('<div class="main-section">', unsafe_allow_html=True)
st.title("💰 Budget Nostalgia")
st.markdown("### Add a New Expense")

category = st.text_input("Category")
amount = st.number_input("Amount Spent", min_value=0, step=1000)
add_expense = st.button("Add Expense")

if add_expense and category:
    st.session_state.expenses.append({"Category": category, "Amount": amount})

# --- Create DataFrame ---
df = pd.DataFrame(st.session_state.expenses)

# --- Budget Overview ---
st.markdown("<div class='section-title'>📊 Budget Overview</div>", unsafe_allow_html=True)
if df.empty:
    st.write("No expenses entered yet.")
else:
    total_spent = df["Amount"].sum()
    remaining = monthly_budget - total_spent

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Spent", f"${total_spent:,.0f}")
        st.metric("Remaining Budget", f"${remaining:,.0f}")

    with col2:
        pie_chart = px.pie(df, values="Amount", names="Category",
                           title="Spending by Category",
                           color_discrete_sequence=px.colors.sequential.Sunset)
        st.plotly_chart(pie_chart, use_container_width=True)

    st.markdown("### Detailed Expenses")
    st.dataframe(df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown(f"### 📈 Used Budget: {total_spent if not df.empty else 0:,.0f} / {monthly_budget:,.0f}")
st.sidebar.markdown('</div>', unsafe_allow_html=True)
