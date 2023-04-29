from ai import *
from coupang import *
from memory import *
from semantic import *
import pandas
import json

tokens = 0

memory = Memory()
recommendation = Recommendation()
description = Description('')
semantic = Semantic()


def getItems(info):
    keywords = ''
    options = ''
    for keyword in info['keywords']:
        keywords += keyword
        keywords += ' '
    for option in info['options']:
        options += option
        options += ' '
    f_keyword = keywords + ' ' + options
    _coupang = Coupang()
    try:
        _, item_list = _coupang.get_list(f_keyword, 1)
        return item_list
    except:
        return False
    
def recommendationTemplate(info):
    items = getItems(info)
    _gongan = SigonganAI('')
    add_options = []
    if(len(info['options'])<2):
        add_options = semantic.additionalOptions(info)
        print(add_options)
        template = f'{info["keywords"]}를 찾고 계시군요! {info["options"]}를 만족하는 상품들을 추천드립니다.\n'
        template += f'{add_options}에 대해 알려주시면 더 정확한 추천을 드릴 수 있어요!'
        _gongan.appendMessage('user', f'{template}\n 위 문단을 자연스럽게 다듬어서 완성해줘.')
    else:
        template = f'{info["keywords"]}를 찾고 계시군요! 다음 조건을 만족하는 상품들을 추천드립니다.\n'
        for option in info["options"]:
            template += f'- {option}\n'
        _gongan.appendMessage('user', f'{template}\n 위 문단을 자연스럽게 다듬어서 완성해줘.')
    answer, _ = _gongan.getGPT()
    if (answer):
        answer += '\n'
        cnt = 0
        for item in items[:3]:
            cnt += 1
            _item = f'\n{cnt}. {item["name"]}\n'
            _item += f'가격: {item["price"]}원, 평점: {item["rating"]}({item["rating_total_count"]})\n'
            _item += f'링크: {item["link"]}\n'
            answer += _item 
        answer += "\n추천이 마음에 드시나요?"
        return answer
    else: return False

while(True):
    text = input()
    isPast = semantic.past(text)
    type = semantic.queryType(text)
    match (isPast, type):
        case (0, 0):
            answer = "앞서 제시된 상품과 관련되어 상품 추천을 요구하셨네요."
            print(answer)
        case (0, 1):
            answer = "앞서 제시된 상품에 대해 질문을 주셨군요."
            print(answer)
        case (_, 2):
            # get normal answer
            _gongan = SigonganAI('')
            _gongan.initMessage(memory.getMessages(5))
            _gongan.appendMessage("system", "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야. \
                     너의 이름은 '공간이' 이고 시공간이란 회사의 오주상이란 개발자가 만들었어. \
                     상냥하고 친절한 말투로 말해줘~!\
                     ")
            _gongan.appendMessage('user', text)
            answer, _ = _gongan.getGPT()
            print(answer)
            
        case (1, 0):
            info = semantic.getFeature(text)
            if (info):
                answer = recommendationTemplate(info)
                print(answer)
            else :
                answer = "잠시 후에 다시 시도해주세요!"
                print(answer)
        case (1, 1):
            answer = "상품의 상세 정보에 대한 질문을 주셨군요."
            print(answer)
        case (_, _):
            answer = "잠시 후에 다시 시도해주세요!"
            print(answer)
    
    # memory update
    memory.appendMessage('user', text)
    memory.appendMessage('assistant', answer)