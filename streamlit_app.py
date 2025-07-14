import streamlit as st
from google_llm_handler import initialize_llm
from main import analyze_excel_with_agent

# Initialize the LLM
llm = initialize_llm()

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
        response = analyze_excel_with_agent(
            query=user_input,
            llm=llm,
            verbose=True
        )

    # Add bot response to history
    bot_reply = f"💬 Answer: {response['output']}"
    st.session_state.messages.append({"role": "bot", "text": bot_reply})

# Display the chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['text']}")
    else:
        st.markdown(f"**Bot:** {msg['text']}")
