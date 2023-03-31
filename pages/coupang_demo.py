import streamlit as st
import seaborn as sns
from coupang import *
from ai import *
from PIL import Image
import requests
from io import BytesIO
import base64
import math
import io

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

    urls = json['imgUrl']
    ocr = ''
    cnt = 0
    for url in urls:
        if cnt > 10: # 10장으로 제한
            break
        content = requests.get(url).content
        img = Image.open(BytesIO(content))
        n = math.ceil(0.5* img.height / img.width)
        list = []
        for i in range(0, n):
            if (i==n-1):
                list.append(img.crop((0, i*2*img.width, img.width, img.height)))
            else:
                list.append(img.crop((0, i*2*img.width, img.width, (i+1)*2*img.width)))
            cnt += 1
        for el in list:
            buffer = io.BytesIO()
            el.save(buffer, format='PNG')
            el = buffer.getvalue()
            string = base64.b64encode(el)
            sigonganAI = SigonganAI(string)
            _ocr = sigonganAI.imgOCR("data")
            ocr += _ocr
            ocr += "\n"

    if len(ocr)>2000:
        ocr = ocr[:2000]
    sigonganAI = SigonganAI('')
    sigonganAI.appendMessage("system", "넌 제품을 판매하기 위한 판매자야. 제품에 대해 자세히 설명해줘.")
    sigonganAI.appendMessage("user", f"제품 정보: {str(json)}\n 제품 상세 정보: {ocr}")
    sigonganAI.appendMessage("user", "내가 이 제품을 사야 할 이유를 10가지로 정리해줘")
    answer = sigonganAI.getGPT()
    st.write("[이 제품을 사야 하는 10가지 이유]")
    st.write(answer)