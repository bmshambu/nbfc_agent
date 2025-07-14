# 🧠 Banking Chat Agent

A Streamlit-powered natural language interface that lets users query banking data using plain English. This application translates user questions into SQL queries and fetches results from a local SQLite database. The results are then synthesized into human-readable responses using a large language model.

---

## 🚀 Features

* **Natural Language Interface** – Ask questions like "What is the total interest due for gold loans?"
* **Automated SQL Generation** – Converts questions into SQL using a language model chain.
* **Smart Responses** – Translates raw data into clear, readable answers using a response synthesizer.
* **Streamlit Interface** – Clean, simple, and interactive web UI.

---

## 🏗️ Architecture Overview

* `Streamlit` for the frontend UI
* `LangChain` and `Groq` for LLM-backed SQL generation and response synthesis
* `SQLite` as the backend database
* `Pandas` for query result processing
* `sqlparse` for formatting and debugging SQL queries

---

## 📂 Project Structure

```
📁 project-root/
├── streamlit_app.py                      # Main Streamlit application
├── main.py                     # Contains `text_to_sql` function for SQL generation
├── constants
    --response_synthesizer.py
    --sys_prompt.py          # Holds the `response_synthesizer` prompt
├── groq_llm_handler.py         # Initializes the Groq LLM
├── loan_data.db                # SQLite database with banking data
├── requirements.txt            # Python dependencies
└── README.md                   # You are here!
```

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/banking-chat-agent.git
cd banking-chat-agent
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your database

Ensure you have a SQLite database named `loan_data.db` with a table named `LoanDueDetails` structured as defined in the schema.

---

## 📊 Schema Used

The agent uses the following table schema for generating SQL queries:

```sql
Table: LoanDueDetails
Columns: 
- Branch Name
- Br. Code
- Loan Type
- Origin Type
- Inventory Number
- Account Number
- Issue Date
- Customer Num
- Customer Name
...
- Last Receipt Tran Date
- Locker No.
```

*Note: See full schema in `app.py`*

---

## 🧠 How It Works

1. **User inputs** a natural language query.
2. **LangChain** + Groq LLM converts the question into a SQL query.
3. The **SQLite database** is queried using `pandas.read_sql_query`.
4. The raw results are passed to the **response synthesizer** for a human-readable reply.
5. The **chat interface** updates with the result.

---

## ▶️ Run the App

```bash
streamlit run streamlit_app.py
```

---

## 📌 Example Questions

* “How much interest is due for all loans in June?”
* “List all customers with outstanding principal greater than 50,000.”
* “What is the average paid rate per gram for gold loans?”

---

## 🛠 Dependencies

Add these to `requirements.txt`:

```txt
streamlit
pandas
langchain
langchain-groq
sqlparse
sqlite3
```

---

## 📬 Contact

For issues or contributions 
- bmshambu134@gmail.com
- anandchangoth@gmail.com

