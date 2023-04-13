import streamlit as st
import pandas as pd
from coupang import *
from ai import *

keyword = st.text_input(label="키워드 입력", value="키보드")
btn1 = st.button("검색", key="btn1")

if btn1:
    coupang = Coupang()
    df = coupang.get_list(keyword, 1)
    item = df.iloc[1]
    item2 = df.iloc[4]
    link = item['link']
    json = coupang.link_search(link)
    st.json(json)
    sigonganAI = SigonganAI('')
    sigonganAI.appendMessage("system", "넌 제품을 판매하기 위한 판매원이야.")
    sigonganAI.appendMessage("user", "예시 : 이 제품은 ~~이런 성능이 우수한게 장점이에요. 당신에게 안성맞춤인 제품입니다. 지금 바로 구매해보세요!")
    sigonganAI.appendMessage("user", f"제품 정보: {str(json)}\n")
    sigonganAI.appendMessage("user", "이 제품을 홍보하기 위한 강력하고 짧은 프로모션 문구를 만들어줘")
    promo1 = sigonganAI.getGPT()
    st.write(promo1)
    sigonganAI.appendMessage("user", "이 제품의 구매자에게 감사하다고 하고 기분 좋아지는 정성스런 안부인사를 건네줘")
    promo2 = sigonganAI.getGPT()
    st.write(promo2)
    sigonganAI.appendMessage("user", f"구매자에게 비슷한 다른 제품도 간단히 추천하는 문구를 작성해줘. 제품 정보: {str(json)}")
    promo3 = sigonganAI.getGPT()
    st.write(promo3)
    
