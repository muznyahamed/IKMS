import streamlit as st

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
if chat:
    chats.append(chat)
    st.write(f"User has sent the following prompt: {chat}")
    print(chats)
