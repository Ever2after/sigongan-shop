import pandas as pd
import requests
import streamlit as st 
from streamlit_chat import message

st.set_page_config(
    page_title="Main",
    page_icon="🛒",
)

st.title('Sigongan-shop v0.0.1')
 
API_URL = "http://localhost:8000/chat"
 
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
 
if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'data' not in st.session_state:
    st.session_state['data'] = []
 
def query(input):
    msgs = []
    for i in range(len(st.session_state['generated']))[-3:]:
        msgs.append({'role':'user', 'content': st.session_state['past'][i]})
        msgs.append({'role':'assistant', 'content': st.session_state['generated'][i]})
    msgs.append({'role':'user', 'content': input})

    data = {
        'messages' : msgs,
        'data' : st.session_state['data']
    }

    response = requests.post(API_URL, json=data)
    return response.json()
 
 
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('Enter the message: ', '', key='input')
    submitted = st.form_submit_button('Send')
 
if submitted and user_input:
    body = query(user_input)
 
    st.session_state.data = body['data']
    st.session_state.past.append(user_input)
    st.session_state.generated.append(body['message'])
 
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=i)
        message(st.session_state['past'][i], is_user=True, key=f'{i}_user')
        
    body['data']

