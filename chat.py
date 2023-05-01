from ai import *
from coupang import *
from daangn import *
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
    fleamarket = '중고' in info['keyword'] or '중고' in info['options']
    keyword = info["keyword"]
    options = ''
    for option in info['options'][:2]:
        options += option
        options += ' '
    f_keyword = keyword + ' ' + options
    if fleamarket:
        _daangn = Daangn()
        try:
            item_list = _daangn.get_list(f_keyword.replace('중고',''))
        except:
            return False
        cnt = 0
        result = ''
        for item in item_list[:3]:
            cnt += 1
            _item = f'\n{cnt}. {item["name"]}\n'
            _item += f'가격: {item["price"]}, 지역: {item["region"]}\n'
            _item += f'링크: {item["link"]}\n'
            _item += f'상세: {item["description"][:30]}...\n'
            result += _item 
        return result
    else:
        _coupang = Coupang()
        try:
            _, item_list = _coupang.get_list(f_keyword, 1)
        except:
            return False
        # make result
        cnt = 0
        result = ''
        for item in item_list[:3]:
            cnt += 1
            _item = f'\n{cnt}. {item["name"]}\n'
            _item += f'가격: {item["price"]}원, 평점: {item["rating"]}({item["rating_total_count"]})\n'
            _item += f'링크: {item["link"]}\n'
            result += _item 
        return result
    
def recommendationTemplate(info):
    items = getItems(info)
    _gongan = SigonganAI('')
    add_options = []
    if(len(info['options'])<1):
        add_options = ', '.join(semantic.additionalOptions(info)['options'])
        template = f'"{info["keyword"]}" 추천 결과입니다. \n'
        template += f'"{add_options}"에 대해 알려주시면 더 정확한 추천을 드릴 수 있어요! \n'
        #_gongan.appendMessage('user', f'{template}\n 위 문단에서 적절히 빈칸을 채워줘.')
    else:
        template = f'"{info["keyword"]}" 추천 결과입니다. \n'
        template += "[조건]\n"
        for option in info["options"]:
            template += f'- {option}\n'
        #_gongan.appendMessage('user', f'{template}\n 위 문단에서 어색한부분을 수정해줘.')
    #answer, _ = _gongan.getGPT()
    answer = template
    if (answer):
        answer += '\n'
        answer += items
        answer += "\n추천이 마음에 드시나요?"
        return answer
    else: return False

while(True):
    text = input()
    if('!' in text):
        info = semantic.getFeature(text.split('!')[-1])
        print(info)
        break
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
            _gongan.initMessage(memory.getMessages(1))
            _gongan.appendMessage("system", "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야. \
                     너의 이름은 '공간이' 이고 시공간이란 회사가 만들었어. \
                     친절하게 대답해줘!\
                     ")
            _gongan.appendMessage('user', text)
            answer, _ = _gongan.getGPT()
            print(answer)
            
        case (1 | 2, 0):
            info = semantic.getFeature(text)
            if (info):
                answer = recommendationTemplate(info)
                print(answer)
            else :
                answer = "잠시 후에 다시 시도해주세요!"
                print(answer)
        case (1 | 2, 1):
            answer = "상품의 상세 정보에 대한 질문을 주셨군요."
            print(answer)
        case (_, _):
            answer = "잠시 후에 다시 시도해주세요!"
            print(answer)
    
    # memory update
    memory.appendMessage('user', text)
    memory.appendMessage('assistant', answer)