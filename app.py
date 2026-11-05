
import streamlit as st
import pandas as pd
import io
import plotly.express as px
from datetime import date
from ai_model import predict_category
from database import (
    create_table,
    add_transaction,
    get_transactions,
    create_budget_table,
    save_budget,
    get_budget
)
st.set_page_config(
    page_title="SpendWise AI",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f8f4;
}
h1, h2, h3 {
    color: #245c43;
}
</style>
""", unsafe_allow_html=True)

# Create database table
create_table()
create_budget_table()
st.title("💰 SpendWise AI")
st.subheader("Export Financial Report")

transactions = get_transactions()

if not transactions.empty:
    csv_data = transactions.to_csv(index=False)

    st.download_button(
        label="📥 Download Transactions as CSV",
        data=csv_data,
        file_name="SpendWise_Financial_Report.csv",
        mime="text/csv"
    )
else:
    st.info("No transactions available to export.")
st.subheader("Your Personal AI-Powered Finance Manager")
st.write("Track your income, manage expenses and make smarter financial decisions.")

st.divider()

# Navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Add Transaction", "AI Insights", "Monthly Analysis", "Monthly Budget"]
)

# Get saved transactions
transactions = get_transactions()

# Dashboard
if page == "Dashboard":

    st.header("Financial Dashboard")

    income = transactions.loc[
        transactions["type"] == "Income", "amount"
    ].sum()

    expenses = transactions.loc[
        transactions["type"] == "Expense", "amount"
    ].sum()

    balance = income - expenses

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Income", f"₹{income:,.2f}")
    col2.metric("Total Expenses", f"₹{expenses:,.2f}")
    col3.metric("Remaining Balance", f"₹{balance:,.2f}")

    st.divider()
    st.subheader("Expense Breakdown")

    expense_data = transactions[
        transactions["type"] == "Expense"
    ]

    if not expense_data.empty:
        fig = px.pie(
            expense_data,
            names="category",
            values="amount",
            title="Where Does Your Money Go?"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add an expense to see your expense breakdown.")

    st.subheader("Recent Transactions")

    if not transactions.empty:
        st.dataframe(transactions, use_container_width=True)
    else:
        st.info("No transactions yet. Add your first transaction!")

# Add Transaction

elif page == "Add Transaction":

    st.header("Add a Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    description = st.text_input("Description")

    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        step=100.0
    )

    categories = [
        "Food",
        "Shopping",
        "Transport",
        "Education",
        "Bills",
        "Entertainment",
        "Health",
        "Salary",
        "Other"
    ]

    if description.strip():
        predicted_category = predict_category(description)
    else:
        predicted_category = "Other"

    st.info(f"🤖 AI Predicted Category: {predicted_category}")

    category = st.selectbox(
        "Confirm or change the category",
        categories,
        index=categories.index(predicted_category)
    )

    transaction_date = st.date_input(
        "Date",
        value=date.today()
    )

    if st.button("Save Transaction"):

        if description.strip() and amount > 0:

            add_transaction(
                transaction_type,
                description,
                amount,
                category,
                str(transaction_date)
            )

            st.success("Transaction saved successfully!")
            st.rerun()

        else:
            st.warning("Please enter a description and an amount greater than zero.")

elif page == "AI Insights":

    st.header("🤖 AI Financial Insights")

    expense_data = transactions[
        transactions["type"] == "Expense"
    ]

    if not expense_data.empty:

        category_spending = expense_data.groupby(
            "category"
        )["amount"].sum().sort_values(ascending=False)

        total_expenses = expense_data["amount"].sum()

        highest_category = category_spending.index[0]
        highest_amount = category_spending.iloc[0]

        st.metric("Total Spending", f"₹{total_expenses:,.2f}")

        st.subheader("Your Spending Analysis")

        st.write(
            f"Your highest spending category is **{highest_category}** "
            f"with ₹{highest_amount:,.2f}."
        )

        fig = px.bar(
            category_spending.reset_index(),
            x="category",
            y="amount",
            title="Spending by Category"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💡 Smart Saving Suggestions")

        if highest_category == "Food":
            suggestion = "Review your food expenses and plan your meals to manage spending."
        elif highest_category == "Shopping":
            suggestion = "Consider comparing prices and planning purchases before shopping."
        elif highest_category == "Entertainment":
            suggestion = "Review entertainment subscriptions and optional purchases."
        elif highest_category == "Transport":
            suggestion = "Compare travel options and plan trips to manage transport costs."
        else:
            suggestion = f"Review your {highest_category.lower()} expenses to identify possible savings."

        st.success(suggestion)

    else:
        st.info("Add some expense transactions to generate financial insights.")

# Monthly Analysis
elif page == "Monthly Analysis":

    st.header("📊 Monthly Spending Analysis")
    st.write("Understand your monthly income, expenses and savings.")

    if not transactions.empty:

        transactions["date"] = pd.to_datetime(
            transactions["date"]
        )

        transactions["month"] = transactions["date"].dt.strftime(
            "%B %Y"
        )

        monthly_data = transactions.groupby(
            ["month", "type"]
        )["amount"].sum().unstack(fill_value=0)

        if "Income" not in monthly_data.columns:
            monthly_data["Income"] = 0

        if "Expense" not in monthly_data.columns:
            monthly_data["Expense"] = 0

        monthly_data["Savings"] = (
            monthly_data["Income"] - monthly_data["Expense"]
        )

        st.subheader("Monthly Financial Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Income",
            f"₹{monthly_data['Income'].sum():,.2f}"
        )

        col2.metric(
            "Total Expenses",
            f"₹{monthly_data['Expense'].sum():,.2f}"
        )

        col3.metric(
            "Total Savings",
            f"₹{monthly_data['Savings'].sum():,.2f}"
        )

        st.divider()

        st.subheader("Income vs Expenses")

        chart_data = monthly_data[
            ["Income", "Expense"]
        ].reset_index()

        fig = px.bar(
            chart_data,
            x="month",
            y=["Income", "Expense"],
            barmode="group",
            title="Monthly Income and Expenses"
        )

        st.plotly_chart(fig, width="stretch")

        st.subheader("Monthly Savings Trend")

        savings_data = monthly_data[
            ["Savings"]
        ].reset_index()

        fig2 = px.line(
            savings_data,
            x="month",
            y="Savings",
            markers=True,
            title="Monthly Savings"
        )

        st.plotly_chart(fig2, width="stretch")

        st.subheader("Detailed Monthly Report")

        st.dataframe(
            monthly_data,
            width="stretch"
        )

    else:
        st.info("Add some transactions to generate your monthly analysis.")
elif page == "Monthly Budget":

    st.title("💰 Monthly Budget Management")

    current_month = date.today().strftime("%Y-%m")

    st.subheader("Set Your Monthly Budget")

    budget = st.number_input(
        "Enter your monthly budget (₹)",
        min_value=0.0,
        value=float(get_budget(current_month)),
        step=500.0
    )

    if st.button("Save Budget"):
        save_budget(current_month, budget)
        st.success("Monthly budget saved successfully!")

    st.divider()

    st.subheader("Budget Overview")

    transactions = get_transactions()

    monthly_expenses = transactions[
        (transactions["type"] == "Expense") &
        (transactions["date"].str.startswith(current_month))
    ]["amount"].sum()

    remaining = budget - monthly_expenses

    col1, col2, col3 = st.columns(3)

    col1.metric("Monthly Budget", f"₹{budget:,.2f}")
    col2.metric("Total Expenses", f"₹{monthly_expenses:,.2f}")
    col3.metric("Remaining Budget", f"₹{remaining:,.2f}")

    if budget > 0:
        progress = min(monthly_expenses / budget, 1.0)
        st.progress(progress)
        if monthly_expenses >= budget:
            st.error("🚨 Budget exceeded! You have crossed your monthly limit.")

        elif monthly_expenses >= budget * 0.8:
            st.warning("⚠️ Alert! You have used 80% of your monthly budget.")

        elif monthly_expenses >= budget * 0.5:
            st.info("💡 You have used 50% of your monthly budget. Keep track of spending!")

        else:
            st.success("✅ Your spending is under control!")
        if monthly_expenses > budget:
            st.warning("You have exceeded your monthly budget!")
        else:
            st.success("You are within your monthly budget!")
           