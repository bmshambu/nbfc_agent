import streamlit as st
import requests
import json
from constants import schema
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

# Streamlit UI
st.set_page_config(page_title="🧠 Banking Chat Agent", page_icon="📊")
st.title("📊 Banking Chat Agent")
st.markdown("Ask a question in natural language. The bot will query the Excel sheet:")

# Input field
question = st.text_input("Enter your question:", placeholder="How many customers have a principal outstanding greater than 1000?")

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
                if response:
                    st.success("✅ Extracted Answer:")
                    st.markdown(f"💬 Answer: {response}")
                    st.markdown("### SQL Query Executed:")
                    st.code(sql_query.strip(), language='sql')
                else:
                    st.error(f"❌ Something Went wrong")

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