from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import sqlparse
import pandas as pd
import sqlite3
from constants.sys_prompt import prompt
from groq_llm_handler import initialize_llm

df=pd.read_excel("ManagementReports-LoanDueList.xlsx",header=1)

def text_to_sql():
    """
    Converts a natural language query to an SQL query using a language model.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data schema.

    Returns:
        str: The generated SQL query.
    """

    conn = sqlite3.connect("loan_data.db")
    df.to_sql("LoanDueDetails", conn, index=False, if_exists='replace')
    prompt_template=PromptTemplate.from_template(prompt)
    #Initialize the Groq LLM
    llm=initialize_llm()
    text_to_sql_chain=LLMChain(llm=llm,prompt=prompt_template)
    return text_to_sql_chain