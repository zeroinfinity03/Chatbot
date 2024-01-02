from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



## function to load Gemini Pro model and get repsonses

model=genai.GenerativeModel("gemini-pro") 
# creates an instance of GenerativeModel with the specified model name.
chat = model.start_chat(history=[])
def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response



##initialize our streamlit app

st.set_page_config(page_title="ChatBot")
st.header("AI ChatBot")


# Initialize streamlit session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []



input=st.text_input("Input: ",key="input")

col1, col2 = st.columns(2,gap="large")
with col1:
    submit = st.button("Ask the question", key='ask_question')
with col2:
    clear_history = st.button("Clear Chat History", key='clear_history')
    

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("Me", input))
    # st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

if clear_history:
    st.session_state['chat_history'] = []


st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
    



    





