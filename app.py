import streamlit as st
import pandas as pd
import plotly.express as px

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

        .alert-over {
            color: #a94442;
            font-weight: bold;
        }

        .alert-under {
            color: #3c763d;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- Fixed Categories ---
categories = ["Food", "Transportation", "Entertainment", "Utilities", "Miscellaneous"]

# --- Initialize session state ---
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "category_budgets" not in st.session_state:
    st.session_state.category_budgets = {cat: 0 for cat in categories}

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.title("📆 Monthly Budget by Category")
for cat in categories:
    st.session_state.category_budgets[cat] = st.sidebar.number_input(f"{cat} Budget", min_value=0, step=50000, value=st.session_state.category_budgets.get(cat, 0), key=f"budget_{cat}")
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# --- Main Section ---
st.markdown('<div class="main-section">', unsafe_allow_html=True)
st.title("💰 Budget Nostalgia")
st.markdown("### Add a New Expense")

category = st.selectbox("Category", categories)
amount = st.number_input("Amount Spent", min_value=0, step=1000)
add_expense = st.button("Add Expense")

if add_expense:
    st.session_state.expenses.append({"Category": category, "Amount": amount})

# --- Create DataFrame ---
df = pd.DataFrame(st.session_state.expenses)

# --- Budget Overview ---
st.markdown("<div class='section-title'>📊 Budget Overview</div>", unsafe_allow_html=True)
if df.empty:
    st.write("No expenses entered yet.")
    total_spent = 0
    total_budget = sum(st.session_state.category_budgets.values())
else:
    category_summary = df.groupby("Category")["Amount"].sum().reset_index()
    category_summary["Budget"] = category_summary["Category"].map(st.session_state.category_budgets)
    category_summary["Remaining"] = category_summary["Budget"] - category_summary["Amount"]
    category_summary["% Used"] = (category_summary["Amount"] / category_summary["Budget"] * 100).fillna(0).round(2)

    total_spent = df["Amount"].sum()
    total_budget = sum(st.session_state.category_budgets.values())
    remaining = total_budget - total_spent

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Spent", f"${total_spent:,.0f}")
        st.metric("Total Remaining", f"${remaining:,.0f}")

    with col2:
        pie_chart = px.pie(df, values="Amount", names="Category",
                           title="Spending by Category",
                           color_discrete_sequence=px.colors.sequential.Sunset)
        st.plotly_chart(pie_chart, use_container_width=True)

    st.markdown("### Category Breakdown")
    for _, row in category_summary.iterrows():
        status = "✅ Within Budget"
        css_class = "alert-under"
        if row["Amount"] > row["Budget"]:
            status = "🚨 Over Budget"
            css_class = "alert-over"

        st.markdown(f"**{row['Category']}**: ${row['Amount']:,.0f} / ${row['Budget']:,.0f} ", unsafe_allow_html=True)
        st.markdown(f"<span class='{css_class}'>{status}</span>", unsafe_allow_html=True)

    st.markdown("### All Expenses")
    st.dataframe(df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Sidebar Total ---
st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
st.sidebar.markdown(f"### 📈 Used Budget: {total_spent:,.0f} / {total_budget:,.0f}")
st.sidebar.markdown('</div>', unsafe_allow_html=True)
