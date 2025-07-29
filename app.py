import streamlit as st
import json
import os

DATA_FILE = "budget_data.json"

# --- Load & Save Functions ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"categories": {}, "total_budget": 0}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- UI ---
st.title("📊 Budget Tracker")

data = load_data()

# Budget Setup
st.header("1. Set Monthly Budget")
data["total_budget"] = st.number_input("Total Monthly Budget", min_value=0, value=data.get("total_budget", 0))

# Expense Entry
st.header("2. Add Expense")
category = st.text_input("Category (e.g. groceries, rent, transport)")
amount = st.number_input("Amount", min_value=0, value=0)

if st.button("➕ Add Expense"):
    if category:
        data["categories"][category] = data["categories"].get(category, 0) + amount
        save_data(data)
        st.success(f"Added {amount} to {category}.")

# Progress Visualization
st.header("3. Budget Overview")

total_spent = sum(data["categories"].values())
remaining = data["total_budget"] - total_spent

st.metric("Total Spent", f"${total_spent}")
st.metric("Remaining", f"${remaining}")

progress = total_spent / data["total_budget"] if data["total_budget"] else 0
st.progress(min(progress, 1.0))

# Category Breakdown
st.subheader("Category Breakdown")
for cat, amt in data["categories"].items():
    st.write(f"**{cat}**: ${amt}")

# Reset
if st.button("🔁 Reset All Data"):
    save_data({"categories": {}, "total_budget": 0})
    st.success("Data has been reset.")
