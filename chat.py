from ai import *
from memory import *
from agent import *
from tools import parser, shop_item, template
import time

class Chat4me:
    def __init__(self):
        self.memory = Memory()
        self.recommendation = Recommendation()
        self.description = Description('')
        self.parser = parser.Parser()
        self.agent = Agent()    

    def getItems(self, info):
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
        
    def recommendationTemplate(self, info):
        items = self.getItems(info)
        if(len(info['options'])<1):
            template = f'"{info["keyword"]}" 추천 결과입니다. \n'
        else:
            template = f'"{info["keyword"]}" 추천 결과입니다. \n'
            template += "[조건]\n"
            for option in info["options"]:
                template += f'- {option}\n'
        answer = template
        if (answer):
            answer += '\n'
            answer += items
            answer += "\n추천이 마음에 드시나요?"
            return answer
        else: return False

    def getChat(self, text, messages=[]):
        latency = []
        self.memory.appendMessage('user', text, [])

        # select api latency
        start = time.time()
        apiType = self.agent.selectApi(text)
        end = time.time()
        latency.append(end-start)

        apiType = apiType.replace("'", "").strip()
        answer = ''

        data = []
        if('itemLists' in apiType):
            prompt = ''

            # get feature latency
            start = time.time()
            info = self.parser.getFeature(text)
            end = time.time()
            latency.append(end-start)

            if (info):
                #answer = self.recommendationTemplate(info)
                _item = shop_item.ShopItem()
                _template = template.Template()

                # search item latency
                start = time.time()
                data = _item.getItems(info['keyword'], info['options'], 3)
                end = time.time()
                latency.append(end-start)
                
                # promotion generation latency
                start = time.time()
                #answer = _template.itemReccommend(data, info['keyword'], info['options'])
                intro = _template.itemIntro(data, info['keyword'], info['options'])
                display = _template.itemDisplay(data, info['keyword'], info['options'])
                answer = intro + display
                end = time.time()
                latency.append(end-start)
            else :
                answer = "잠시 후에 다시 시도해주세요!"
        elif('details' in apiType):
            # get normal answer
            _gongan = SigonganAI('')
            prompt = "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야."
            prompt += "너의 이름은 '포미' 이고 시공간이란 회사가 만들었어."
            prompt += "귀여운 말투로 '짧게' '존댓말'로 대답해줘"
            _gongan.appendMessage("system", prompt)

            _, _messages = self.memory.getMessages(5)
            _gongan.appendMessages(_messages)
            
            start = time.time()
            answer, _ = _gongan.getGPT()
            end = time.time()
            latency.append(end-start)
        else:
            # get normal answer
            _gongan = SigonganAI('')
            prompt = "너는 지금부터 온라인 쇼핑몰의 상품을 추천해주는 도우미야."
            prompt += "너의 이름은 '포미' 이고 시공간이란 회사가 만들었어."
            prompt += "귀여운 말투로 '짧게' '존댓말'로 대답해줘"
            _gongan.appendMessage("system", prompt)

            _, _messages = self.memory.getMessages(5)
            _gongan.appendMessages(_messages)

            start = time.time()
            answer, _ = _gongan.getGPT()
            end = time.time()
            latency.append(end-start)
        
        # print total latency
        print(latency)

        # memory update
        self.memory.appendMessage('assistant', answer, data)

        return apiType, answer, data

if __name__ == '__main__':
    chat = Chat4me()
    text = input()
    apiType, answer, data = chat.getChat(text)
    print(answer)