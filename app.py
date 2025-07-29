import streamlit as st
import pandas as pd
import datetime
import json
import os

st.set_page_config(page_title="Financial Catalepsia Preventer", layout="wide")

# Sidebar controls
st.sidebar.title("Controls")
uploaded_file = st.sidebar.file_uploader("Upload your .csv bank statement", type="csv")
date_range = st.sidebar.date_input("Select date range", [datetime.date.today().replace(day=1), datetime.date.today()])

# Load fixed categories from JSON or default
fixed_json_path = "fixed_costs.json"
if os.path.exists(fixed_json_path):
    with open(fixed_json_path, 'r') as f:
        FIXED_CATEGORIES = json.load(f)
else:
    FIXED_CATEGORIES = {
        "Rent": 1000000,
        "Utilities": 250000,
        "Groceries": 500000
    }

# Allow user to modify fixed costs
st.sidebar.subheader("Fixed Monthly Costs")
for category in list(FIXED_CATEGORIES.keys()):
    FIXED_CATEGORIES[category] = st.sidebar.number_input(f"{category}", value=FIXED_CATEGORIES[category], step=10000)

# Save updated fixed categories to JSON
with open(fixed_json_path, 'w') as f:
    json.dump(FIXED_CATEGORIES, f)

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

            # Save summary JSON
            summary_json = {
                "total_spent": total_spent,
                "fixed_costs": FIXED_CATEGORIES,
                "date_range": [str(date_range[0]), str(date_range[1])]
            }
            with open("summary.json", "w") as f:
                json.dump(summary_json, f)

            st.success("Spend wisely, or perish slowly.")
    except Exception as e:
        st.error(f"There was an error processing the file: {e}")
else:
    st.warning("Please upload a CSV file to begin analysis.")
