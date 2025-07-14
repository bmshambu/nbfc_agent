from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from groq_llm_handler import initialize_llm

llm = initialize_llm()

def analyze_excel_with_agent(file_path, query, llm, verbose=True):
    """
    Reads an Excel file, creates a pandas dataframe agent using the given LLM,
    and runs a natural language query on the data.

    Parameters:
        file_path (str): Path to the Excel file.
        query (str): Natural language query to ask about the data.
        llm: A language model instance (like OpenAI's LLM).
        verbose (bool): Whether to display verbose output.

    Returns:
        The result of the query from the agent.
    """
    df = pd.read_excel(file_path)
    agent = create_pandas_dataframe_agent(llm, df, verbose=verbose)
    response = agent.invoke(query)
    #response ='There are 891 rows in the dataframe.'
    return response