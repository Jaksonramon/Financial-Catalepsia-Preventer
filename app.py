import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Financial Catalepsia Preventer", layout="wide")

# Sidebar controls
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("Upload your .csv bank statement", type="csv")
date_range = st.sidebar.date_input("Select date range", [datetime.date.today().replace(day=1), datetime.date.today()])

# Fixed categories to simulate unavoidable costs
FIXED_CATEGORIES = {
    "Rent": 1000000,
    "Utilities": 250000,
    "Groceries": 500000
}

st.title("💸 Financial Catalepsia Preventer")
st.write("Helps you identify where you’re bleeding money before it kills your will to live.")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = [col.strip() for col in df.columns]  # Clean up column names

        # Show raw data
        st.subheader("Raw Statement Data")
        st.dataframe(df.head())

        # Ensure proper column names exist
        if "Amount" not in df.columns or "Category" not in df.columns or "Date" not in df.columns:
            st.error("CSV must contain 'Amount', 'Category', and 'Date' columns.")
        else:
            # Preprocessing
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
            df = df.dropna(subset=["Date"])
            df = df[(df["Date"] >= pd.to_datetime(date_range[0])) & (df["Date"] <= pd.to_datetime(date_range[1]))]

            # Show filtered data
            st.subheader("Filtered Transactions")
            st.dataframe(df)

            # Summaries
            total_spent = df["Amount"].sum() + sum(FIXED_CATEGORIES.values())
            st.subheader("📊 Summary")
            st.write(f"**Total Spent (including fixed costs):** ${total_spent:,.0f}")

            category_summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            st.write("**Spending by Category:**")
            st.bar_chart(category_summary)

            st.write("**Fixed Costs:**")
            for category, amount in FIXED_CATEGORIES.items():
                st.write(f"- {category}: ${amount:,.0f}")

            st.success("Spend wisely, or perish slowly.")
    except Exception as e:
        st.error(f"There was an error processing the file: {e}")
else:
    st.warning("Please upload a CSV file to begin analysis.")

