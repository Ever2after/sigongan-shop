from ai import *
from memory import *
from agent import *
from tools import parser, shop, coupang
import time
import re
import asyncio

class Chat4me:
    def __init__(self):
        self.memory = Memory()
        self.parser = parser.Parser()
        self.agent = Agent()    

    async def getChat(self, messages, data = []):
        latency = []
        self.memory.initMemory(messages, data)
        answer = ''
        newData = data

        if('coupang.com/vp/products' in messages[-1]['content']):
            result = re.findall("(https:\/\/)|(coupang.com\/vp\/products\/[0-9]*)", messages[-1]['content'])
            list = []
            for el in result[:2]:
                list.append(''.join(el))
            url = ''.join(list)

            _coupang = coupang.Coupang()
            start = time.time()
            text = await _coupang.image_read(url)
            mid = time.time()
            summary = self.parser.summaryDetails(text)
            end = time.time()
            latency += [mid-start, end-mid]

            product_info = {}
            product_info['detail'] = summary
            
            newData = product_info
            answer = summary

            end = time.time()
            latency.append(end-start)
        
        else:
            # select api latency
            start = time.time()
            apiType = self.agent.selectApi(messages, data)
            apiType = apiType.replace("'", "").strip()
            end = time.time()
            latency.append(end-start)
            
            if('productLists' in apiType):
                prompt = ''

                # get feature latency
                start = time.time()
                info = self.parser.getFeature(messages, data)
                end = time.time()
                latency.append(end-start)

                if (info):
                    _shop = shop.Shop(info['keyword'], info['options'])

                    # search item latency
                    start = time.time()
                    newData = _shop.getItems(3)
                    end = time.time()
                    latency.append(end-start)
                    
                    # promotion generation latency
                    start = time.time()
                    intro = _shop.itemIntro()
                    display = _shop.itemDisplay()
                    answer = intro + display
                    end =   time.time()
                    latency.append(end-start)
                else :
                    answer = "잠시 후에 다시 시도해주세요!"
            elif('details' in apiType):
                # get normal answer
                _gongan = SigonganAI()
                prompt = "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야."
                prompt += "너의 이름은 '포미' 이고 시공간이란 회사가 만들었어."
                prompt += "귀엽게 '짧게' '존댓말'로 대답해줘"
                _gongan.appendMessage("system", prompt)

                _messages = self.memory.getMessages()[-5:]
                _data = self.memory.getData()
                _gongan.appendMessages(_messages)
                if _data:
                    _gongan.appendMessage('user', f'\n [답변에 참고할 정보] : {_data}')

                start = time.time()
                answer, _ = _gongan.getGPT('gpt-3.5-turbo-16k-0613')
                end = time.time()
                latency.append(end-start)
            else:
                # get normal answer
                _gongan = SigonganAI()
                prompt = "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야."
                prompt += "너의 이름은 '포미' 이고 시공간이란 회사가 만들었어."
                prompt += "귀여운 말투로 '짧게' '존댓말'로 대답해줘"
                _gongan.appendMessage("system", prompt)

                _messages = self.memory.getMessages()[-5:]
                _data = self.memory.getData()
                _gongan.appendMessages(_messages)
                if data: 
                    _gongan.appendMessage('user', f'\n [답변에 참고할 정보] : {_data}')

                start = time.time()
                answer, _ = _gongan.getGPT()
                end = time.time()
                latency.append(end-start)
        
        # print total latency
        print(latency)
        return answer, newData

if __name__ == '__main__':
    chat = Chat4me()
    text = input()
    answer, newData = asyncio.run(chat.getChat([{'role': 'user', 'content': text}]))
    print(answer, newData)
    