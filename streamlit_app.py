import streamlit as st
from groq_llm_handler import initialize_llm
from main import analyze_excel_with_agent

llm = initialize_llm()
# Mock function to convert text to SQL and return a mock result


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Banking Chat Agent")

st.markdown("Ask a question in natural language. The bot will convert it to SQL and query the database.")

# User input
user_input = st.text_input("You:", key="input")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "text": user_input})

    # Generate SQL and result
    response = analyze_excel_with_agent(
        file_path="ManagementReports-LoanDueList.xlsx",
        query=user_input,
        llm=llm,
        verbose=True
        )

    # Add bot response
    bot_reply = f"💬 Answer: {response}"
    st.session_state.messages.append({"role": "bot", "text": bot_reply})

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")