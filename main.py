from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
# from groq_llm_handler import initialize_llm
from google_llm_handler import initialize_llm

llm = initialize_llm()
file_path = "ManagementReports-LoanDueList.xlsx"
df = pd.read_excel(file_path)

def analyze_excel_with_agent(query, llm, verbose=True):
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

    agent = create_pandas_dataframe_agent(llm, df,
                                        agent_type="tool-calling",
                                        include_df_in_prompt=True,
                                        number_of_head_rows=2,
                                        verbose=verbose,allow_dangerous_code=True)
    response = agent.invoke(query)
    print (f"Response: {response}")
    # For demonstration purposes, we return a mock response
    #response ='There are 891 rows in the dataframe.'
    return response