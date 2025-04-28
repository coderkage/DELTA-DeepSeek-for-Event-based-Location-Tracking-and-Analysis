import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
import requests
 

API_KEY = "#################################################################"
# Replace with your OpenRouter API key

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

OSAKA_PROMPT = """
You need to assist user.
"""
def osaka_respond(user_input):

    # Generate Osaka-style response using OpenRouter (Mistral 7B)
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-v3-base:free",
            "messages": [
                {"role": "system", "content": OSAKA_PROMPT},
                {"role": "user", "content": f"{user_input}"},
            ]
        })
    )

    response_json = response.json()
    return response_json["choices"][0]["message"]["content"] if "choices" in response_json else "Huh? I got lost again..."


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


st.markdown('<div class="title-text">Disaster Assistant</div>', unsafe_allow_html=True)


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

    response = osaka_respond(prompt)
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})