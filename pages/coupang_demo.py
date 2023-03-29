import streamlit as st
import seaborn as sns
from coupang import *

st.set_page_config(
    page_title="Coupang",
    page_icon="🛒",
)

st.sidebar.header("Coupang crawling demo")

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Coupang crawling demo")

keyword = st.text_input(label='쿠팡 키워드 검색', value="마우스")
btn1 = st.button("검색", key="btn1")
if btn1:
    coupang = Coupang()
    df = coupang.get_list(keyword, 3)
    st.dataframe(df)
    sns.histplot(data = df, x=df["price"])
    st.pyplot()

link = st.text_input(label='쿠팡 상품 링크 검색', value="https://www.coupang.com/vp/products/186205951")
btn2 = st.button('검색', key="btn2")
if btn2:
    coupang = Coupang()
    json = coupang.link_search(link)
    st.json(json)
