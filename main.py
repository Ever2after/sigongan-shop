import pandas as pd
import streamlit as st 

st.set_page_config(
    page_title="Main",
    page_icon="🛒",
)

st.title('Sigongan-shop v0.0.1')

st.write('템플릿 예시')
option = st.selectbox('서비스를 선택하세요', ('제품 추천', '제품 상세 설명', '구매 대행'))
name = st.text_input('제품명')
description = st.text_area('제품 추천 이유')
btn1 = st.button('완료')
if btn1:
    st.markdown(f'안녕하세요, 시공간 쇼핑입니다. 저희의 {option} 서비스를 이용해주셔서 감사드립니다.')
    st.markdown(f'아래는 요청하신 서비스에 대한 결과물입니다.')
    st.markdown(f'제품명: {name}')
    st.markdown(f'제품 추천 이유')
    st.markdown(f'>{description}')
    st.markdown('감사합니다.')
    

