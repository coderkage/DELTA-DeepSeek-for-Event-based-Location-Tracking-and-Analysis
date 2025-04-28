import streamlit as st
import ollama
import re

def remove_before_think(text):
    return re.sub(r'^.*?</think>', '', text)

model = "deepseek-r1:1.5b"

def chat_with_deep(prompt):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    content = response.message.content
    return re.sub(r'^.*?</think>\s*', '', content, flags=re.DOTALL) 

# Streamlit UI Setup
st.set_page_config(page_title="Assistant AI", page_icon="🤖", layout="centered")
st.markdown(
    f"""
    <style>
    .stApp {{
        
        background-size: cover;
    }}
    .title-text {{
        font-size: 40px;
        font-weight: bold;
        color: #ff66b2;
        text-align: center;
    }}
    .chat-bubble {{
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        display: inline-block;
    }}
    .user-msg {{
        background-color: #ffccff;
        align-self: flex-end;
    }}
    .osaka-msg {{
        background-color: #ccffff;
        align-self: flex-start;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="title-text">🦙 Disaster Assistant (Ollama)</div>', unsafe_allow_html=True)


st.write("---")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How may I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = chat_with_deep(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})