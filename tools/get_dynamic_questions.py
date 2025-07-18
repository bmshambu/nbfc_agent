from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from constants.get_dynamic_question_prompt import prompt
from groq_llm_handler import initialize_llm
from tools.parse_output import safe_parse_llm_suggestions

def get_dynamic_questions(question: str,last_answer: str = ""):
    """
    Generates dynamic questions based on the schema using a language model. """

    prompt_template=PromptTemplate.from_template(prompt)
    #Initialize the Groq LLM
    llm=initialize_llm()
    get_dynamic_question_chain=LLMChain(llm=llm,prompt=prompt_template)
    dynamic_quesions=get_dynamic_question_chain.run(last_question=question,last_answer=last_answer)
    list_of_dynamic_questions = list(dynamic_quesions.strip().split('\n'))
    list_of_dynamic_questions = safe_parse_llm_suggestions(list_of_dynamic_questions)
    #print("Generated Dynamic Questions:\n", dynamic_quesions)
    #print("Type of dynamic_quesions:", list_of_dynamic_questions[0],len(list_of_dynamic_questions))
    return list_of_dynamic_questions
