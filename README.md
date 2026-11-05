# 💰 SpendWise AI – Personal Finance Management System

SpendWise AI is an AI-powered personal finance management application developed using Python and Streamlit. It helps users track income and expenses, understand spending patterns, manage monthly budgets, and make better financial decisions.

## ✨ Features

- **Financial Dashboard:** View income, expenses, and available balance.
- **Transaction Management:** Add and track income and expenses.
- **AI Expense Categorization:** Automatically predict transaction categories using a Machine Learning model.
- **AI Insights:** Analyze spending patterns and receive saving suggestions.
- **Monthly Analysis:** View monthly income, expenses, and savings trends.
- **Budget Management:** Set and monitor monthly budgets.
- **Spending Alerts:** Receive alerts when spending reaches budget thresholds.
- **CSV Export:** Download transaction records as a CSV report.

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Scikit-learn

## 🤖 How AI Is Used

SpendWise AI uses a Naive Bayes Machine Learning classifier to predict transaction categories based on their descriptions.

It also provides spending insights and rule-based saving suggestions to help users understand their financial activity.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/alam-webnanditha/SpendWise-AI.git
```

### 2. Open the project folder

```bash
cd SpendWise-AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📁 Project Structure

```text
SpendWise-AI/
│
├── app.py
├── database.py
├── ai_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🎯 Project Objective

The objective of SpendWise AI is to demonstrate how Artificial Intelligence and Machine Learning can be used in personal finance management to support expense tracking, spending analysis, and budgeting.

## 👩‍💻 Developed As

A college academic project – AI for Finance CIA-2.

---

**Spend smarter. Save better. Live better!** 💚