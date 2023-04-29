from ai import *
from coupang import *
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
    if (answer):
        answer = answer.replace('\'', '\"')
        try:
            _json = json.loads(answer)
        except:
            print(answer)
            return False
        return _json
    else: return False

def getItems(info):
    keywords = ''
    options = ''
    for keyword in info['keyword']:
        keywords += keyword
        keywords += ' '
    for option in info['options']:
        options += option
        options += ' '
    f_keyword = keywords + ' ' + options
    _coupang = Coupang()
    try:
        item_list = _coupang.get_list(f_keyword, 1)
        return item_list
    except:
        return False
        
def semanticParsing(text):
    _gongan = SigonganAI('')
    _gongan.appendMessage('user', f'다음 질문이 어떤 의도인지 분류해줘. 중복 선택도 가능해 \
         카테고리 = ["상품 검색, 추천 요구", "상품에 대한 상세 설명, 판매 정보 요구", "그 외 단순 질문"].     \
         질문 : {text}.   \
        ')
    answer, _ = _gongan.getGPT()
    list = []
    if('추천' in answer): list.append(0)
    elif('설명' in answer): list.append(1)
    else: list.append(2)
    return list

while(True):
    type = input('select type')
    if ('0' in type):
        text = input('give a question')
        answer = semanticParsing(text)
        print(answer)
    elif('1' in type):
        text = input('give a question')
        if("q" in text): break
        info = extractFeature(text)
        print(info)
        if (not info): continue
        moreOptions = getMoreFeature(info)
        print(moreOptions)
        item_list = getItems(info)
        print(item_list[:4])
    else: continue



