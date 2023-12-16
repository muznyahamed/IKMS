#coding part
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfFileReader, PdfFileWriter,PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.llms import GooglePalm
from langchain_google_genai import GoogleGenerativeAIEmbeddings
google_api_key = "AIzaSyAGLqWWGWp5BcpHM9TDXTznVh2_ipOSxf4"
llm = GooglePalm(google_api_key=google_api_key)
llm.temperature = 0.1



import pickle
import os
from dotenv import load_dotenv
import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )




load_dotenv()

#Background images add function
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
#         background-size: cover;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
#add_bg_from_local('images.jpeg')  

#sidebar contents

with st.sidebar:
    st.title('IKMS - integrated knowledge management system')
    # st.markdown('''
    # ## About APP:

    # The app's primary resource is utilised to create::

    # - [streamlit](https://streamlit.io/)
    # - [Langchain](https://docs.langchain.com/docs/)
    # - [OpenAI](https://openai.com/)

    # ## About me:

    # - [Linkedin](https://www.linkedin.com/in/venkat-vk/)
    
    # ''')

    # add_vertical_space(4)
    # st.write('💡All about pdf based chatbot, created by VK🤗')

load_dotenv()

def main():
    st.header("Chat with your pdf file")

    #upload a your pdf file
    pdf = st.sidebar.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)

        text = ""
        for page in pdf_reader.pages:
            text+= page.extract_text()

        #langchain_textspliter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 100,
            chunk_overlap = 20,
            length_function = len
        )

        chunks = text_splitter.split_text(text=text)

        
        #store pdf name
        store_name = pdf.name[:-4]
        
        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl","rb") as f:
                vectorstore = pickle.load(f)
        else:
            embeddings = GoogleGenerativeAIEmbeddings(google_api_key=google_api_key,model="models/embedding-001")

            #Store the chunks part in db (vector)
            vectorstore = FAISS.from_texts(chunks,embedding=embeddings)

            with open(f"{store_name}.pkl","wb") as f:
                pickle.dump(vectorstore,f)
            
           
       
            
        def randon_string(user_input):
            docs = vectorstore.similarity_search(query=user_input,k=3)
            llm = GooglePalm(google_api_key=google_api_key)
            llm.temperature = 0.1
            chain = load_qa_chain(llm=llm, chain_type= "stuff")
            print(user_input)
            response = chain.run(input_documents = docs, question = user_input) 
            return(response)


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


        chat = st.chat_input("Enter your message", on_submit=chat_actions, key="chat_input")

        for i in st.session_state["chat_history"]:
            with st.chat_message(name=i["role"]):
                st.write(i["content"])
        




if __name__=="__main__":
    main()