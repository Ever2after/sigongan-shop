import streamlit as st
import pandas as pd
from naver import *

st.set_page_config(
    page_title="Naver",
    page_icon="🛒",
)

st.sidebar.header("Naver search api demo")

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Naver search api demo")

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

if 'df_exist' not in st.session_state:
    st.session_state['df_exist'] = False

keyword = st.text_input(label="네이버 쇼핑 검색", value="프로틴")
btn1 = st.button("검색", key="btn1")

if btn1:
    naver = Naver()
    df = pd.DataFrame(naver.get_list(keyword, 100)['items'])
    st.session_state['df'] = df
    st.session_state['df_exist'] = True

number = st.slider("제품 선택", 1, st.session_state.df.shape[0])

if st.session_state.df_exist:
    data = st.session_state.df.iloc[number-1]
    st.image(data.image, width=300, caption=f"{data.title}, {data.lprice}원")
    st.write(data.link)
    st.dataframe(st.session_state.df)

url = st.text_input("링크 입력")
btn2 = st.button("검색", key="btn2")
if btn2:
    naver = Naver()
    naver.get_original_url(url)