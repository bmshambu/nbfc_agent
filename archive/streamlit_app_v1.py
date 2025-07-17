import streamlit as st
from main import text_to_sql
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from constants import response_synthesizer
from groq_llm_handler import initialize_llm
import os
import sqlparse
import pandas as pd
import sqlite3

schema = """
   Table: LoanDueDetails
   Columns: Branch Name', 'Br. Code', 'Loan Type', 'Origin Type',
    'Inventory Number', 'Account Number', 'Issue Date', 'Customer Num',
    'Customer Name', 'Address', 'Cell Num', 'Phone Num',
    'Issue Amount', 'Weight', 'Deductions', 'Net Weight', 'Purity',
    'Principal Received', 'Interest Received', 'PL Interest Rcvd.',
    'Principal Outstanding', 'Interest Due', 'Penal Interest Due',
    'Base Interest Rate', 'Total Interest Rate', 'Interest Period',
    'Paid Rate Per Gram', 'Account Number-PL', 'PL loan Type-PL',
    'Principal Outstanding-PL', 'Interest Due-PL',
    'Interest Received-PL', 'Total Outstanding', 'Total Interest Due',
    'Current Rate Per Gram', 'Notice Letter Status', 'Loan Period',
    'Loan Period Type', 'Market Rate(Prty)', 'Asset Value', 'DAR',
    'Ref. Doc.#', 'Marketing Executive', 'Relationship Executive',
    'Collection Executive', 'Is Locked', 'Locked On', 'Locked By',
    'Last Receipt Tran Date', 'Locker No.
    """

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Banking Chat Agent")
st.markdown("Ask a question in natural language. The bot will query the Excel sheet.")

# Input with Enter button
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", key="input")
    submitted = st.form_submit_button("Enter")

if submitted and user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Show loading spinner
    with st.spinner("Thinking..."):
        # response = run_dataframe_agent(
        #     query=user_input
        # )
        try:
            text_to_sql_chain=text_to_sql()
            sql_query = text_to_sql_chain.run(schema=schema, question=user_input)
            print("Generated SQL Query:\n", sql_query.strip())
            conn = sqlite3.connect("loan_data.db")
            result_df = pd.read_sql_query(sql_query, conn)
            json_output = result_df.to_json(orient="records", indent=2)

            response_chain = LLMChain(
                llm=initialize_llm(),
                prompt=PromptTemplate.from_template(response_synthesizer.prompt)
            )
            response = response_chain.run(
                question=user_input,
                answer=json_output
            )
        except Exception as e:
            response_chain = LLMChain(
                llm=initialize_llm(),
                prompt=PromptTemplate.from_template(response_synthesizer.prompt)
            )
            response = response_chain.run(
                question=user_input,
                answer=e
            )

    # Add bot response to history
    print("Generated Response:\n", response)
    bot_reply = f"💬 Answer: {response}"
    st.session_state.messages.append({"role": "bot", "text": bot_reply})

# Display the chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")