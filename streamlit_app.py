import streamlit as st
import requests
import json
from constants import schema
from main_groq import text_to_sql
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from constants import response_synthesizer
from groq_llm_handler import initialize_llm
from tools.get_dynamic_questions import get_dynamic_questions
import os
import sqlparse
import pandas as pd
import sqlite3
from constants.schema import schema

# Streamlit UI
st.set_page_config(page_title="🧠 Banking Chat Agent", page_icon="📊")
st.title("📊 Banking Chat Agent")
st.markdown("Ask a question in natural language. The bot will query the Excel sheet:")

suggested_questions = [
    "How many customers have a principal outstanding greater than 1000?",
    "What is the average loan amount per region?",
    "How many loans are currently overdue?"
]


if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'last_llm_response' not in st.session_state:
    st.session_state['last_llm_response'] = ""


# # Input field (load suggestion if present)
question = st.text_input(
    "Enter your question:",
    value=st.session_state.get("input", ""),
    placeholder="How many customers have a principal outstanding greater than 1000?"
)

# print("Current Question:", question)

# Submit button
if st.button("Submit") and question.strip():
    with st.spinner("Analyzing..."):
        try:
            try:
                # response = requests.post(API_URL, json={"question": question, "thread_id": "streamlit-user"})
                text_to_sql_chain=text_to_sql()
                sql_query = text_to_sql_chain.run(schema=schema, question=question)
                print("Generated SQL Query:\n", sql_query.strip())
                conn = sqlite3.connect("loan_data.db")
                result_df = pd.read_sql_query(sql_query, conn)
                json_output = result_df.to_json(orient="records", indent=2)
                response_chain = LLMChain(
                    llm=initialize_llm(),
                    prompt=PromptTemplate.from_template(response_synthesizer.prompt)
                )
                response = response_chain.run(
                    question=question,
                    answer=json_output
                )
                #st.session_state['response'] = response
                st.session_state['history'].append((question, response))
                st.session_state['last_llm_response'] =response
                if response:
                    st.success("✅ Extracted Answer:")
                    st.markdown(f"💬 Answer: {response}")
                    # st.markdown("### SQL Query Executed:")
                    # st.code(sql_query.strip(), language='sql')
                else:
                    st.error(f"❌ Something Went wrong")
                #st.rerun()
            except Exception as e:
                response_chain = LLMChain(
                    llm=initialize_llm(),
                    prompt=PromptTemplate.from_template(response_synthesizer.prompt)
                )
                response = response_chain.run(
                    question=question,
                    answer=e
                )

                if response:
                    st.success("✅ Extracted Answer:")
                    st.markdown(f"💬 Answer: {response}")
                else:
                    st.error(f"❌ Something Went wrong")
        except Exception as e:
            st.error(f"⚠️ Exception occurred: {str(e)}")

# Suggest dynamic follow-up questions if conversation exists
if st.session_state['history']:
    last_q, last_a = st.session_state['history'][-1]
    suggested = get_dynamic_questions(last_q, last_a)
    st.markdown("### 💡 Suggested Follow-up Questions:")
    for i, sug in enumerate(suggested):
        if st.button(sug, key=f"followup_{i}"):
            st.session_state["input"] = sug
            st.rerun()
else:
    st.markdown("### 💡 Suggested Questions:")
    for i, sug in enumerate(suggested_questions):
        if st.button(sug, key=f"suggested_{i}"):
            st.session_state["input"] = sug
            st.rerun()