from ai import *
import json

gongan = SigonganAI("")
tokens = 0
gongan.appendMessage("system", "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야")

def extractFeature(text):
    _gongan = SigonganAI("")
    example1 = {
        "keyword": ["키보드"],
        "options": ["게이밍", "10만원대", "저렴한", "평점 좋은"]
    }
    example2 = {
        "keyword": ["원피스", "블라우스"],
        "options": ["가을에 입을만한", "베이지 계열", "오프숄더"]
    }
    message = [
        {"role": "user", "content": f"설명: {text} \n 위 글은 고객이 원하는 상품에 대한 설명이야. 이 상품에 대한 keyword와 option을 나누어서 json 형태로 정리해줘. json 외에 다른 답은 하지마. \
         예시1: {example1}, 예시2: {example2}."}
    ]
    _gongan.initMessage(message)
    answer, _ = _gongan.getGPT()
    answer = answer.replace('\'', '\"')
    try:
        _json = json.loads(answer)
    except:
        return False
    return _json

def getMoreFeature(info):
    example1 = {
        "options": ["가격", "브랜드", "성능"]
    }
    example2 = {
        "options": ["맛", "용량", "탄산여부"]
    }
    _gongan = SigonganAI('')
    _gongan.appendMessage('system', '너는 온라인 쇼핑몰의 상품을 소개하는 도우미야.')
    _gongan.appendMessage('user', f'나는 {info["keyword"]}를 구매하려고 해. {info["options"]}의 조건 외에 더 고려해보면 좋을 만한 조건, 선택지를 json으로 제시해줘. json 외 다른 답은 하지마.\
                            예시1: {example1}, 예시2: {example2}')
    answer, _ = _gongan.getGPT()
    answer = answer.replace('\'', '\"')
    try:
        _json = json.loads(answer)
    except:
        return False
    return _json


while(True):
    text = input()
    if("q" in text): break
    info = extractFeature(text)
    print(info)
    if (not info): continue
    moreOptions = getMoreFeature(info)
    print(moreOptions)



