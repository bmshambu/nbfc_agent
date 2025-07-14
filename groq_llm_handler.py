# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config import AppConfig
import os

cfg=AppConfig()

def initialize_llm():
    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = cfg.api_key_groq
    llm = ChatGroq(
        model=cfg.groq_model_name,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    return llm