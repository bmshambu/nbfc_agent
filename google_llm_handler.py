from langchain_google_genai import ChatGoogleGenerativeAI
from config import AppConfig
import os

cfg=AppConfig()

def initialize_llm():
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = cfg.api_key
    llm = ChatGoogleGenerativeAI(
        model=cfg.model_name,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
    )
    return llm