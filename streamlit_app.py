import streamlit as st
from langchain.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAIEmbeddings
google_api_key = "AIzaSyAGLqWWGWp5BcpHM9TDXTznVh2_ipOSxf4"
llm = GooglePalm(google_api_key=google_api_key)
llm.temperature = 0.1

value ="enter your name "

chats=[]

# Using object notation
value = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )
st.write(value)
chat = st.chat_input("Say something")
import string
import random


def randon_string(user_input):
    user_input =  user_input
    return llm(user_input)


def chat_actions():
    st.session_state["chat_history"].append(
        {"role": "user", "content": st.session_state["chat_input"]},
    )

    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": randon_string(st.session_state["chat_input"]),
        },
    )


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


st.chat_input("Enter your message", on_submit=chat_actions, key="chat_input")

for i in st.session_state["chat_history"]:
    with st.chat_message(name=i["role"]):
        st.write(i["content"])