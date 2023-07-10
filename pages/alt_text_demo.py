import streamlit as st
import pandas as pd
import requests

CRAWLING_API_URL = 'http://34.70.221.73:8000/sel'

st.set_page_config(
    page_title="Alt_Text",
    page_icon="😯",
)

if 'data' not in st.session_state:
    st.session_state['data'] = []

def query(url):
    data = {
        'url' : url,
        'type' : 'image',
        'platform': 'general'
    }
    response = requests.post(CRAWLING_API_URL, json = data)
    return response.json()

url =  st.text_input(
    "Enter the url",
    value="https://si-gongan.imweb.me"
)

if st.button("Start!"):
    data = query(url)
    if data:
        df = pd.DataFrame(data)
        st.data_editor(
            df, 
            column_config = {
                "url": st.column_config.ImageColumn(
                    "Preview Image", help="Streamlit app preview screenshots",
                    width="large"
                ),
                "alt": st.column_config.Column(
                    "Alt Text"
                )
            }
        )
        st.write('총 이미지 개수 : ', df.shape[0])
        st.write('Alt가 삽입된 이미지 개수 : ', (df['alt'] != '').sum())
    else :
        st.write("wrong url!!!")

