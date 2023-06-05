import pandas as pd
import requests
import streamlit as st 
from streamlit_chat import message

st.set_page_config(
    page_title="Main",
    page_icon="🛒",
)

st.title('Sigongan-shop v0.0.1')
 
API_URL = "http://18.116.15.180:8000/chat/"
 
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
 
if 'past' not in st.session_state:
    st.session_state['past'] = []
 
def query(input):
	response = requests.get(API_URL+input)
	return response.json()
 
 
with st.form('form', clear_on_submit=True):
    user_input = st.text_input('You: ', '', key='input')
    submitted = st.form_submit_button('Send')
 
if submitted and user_input:
    output = query(user_input)
    output
 
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["message"])
 
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
    

