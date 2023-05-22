from ai import *

class Agent():
    def __init__(self):
        self.apiList = {
            'itemLists': {
                'description' : 'get item lists from given keyword',
                'url' : '/itemlists/[keyword]'
            },
            'details': {
                'description' : 'get detailed information of certain item such as price, shipping, spec, etc.',
                'url' : '/details/[itemName]'
            },
            'pastPrice': {
                'description' : 'returns past price history of the item. list of date-price',
                'url' : '/pastprice/[itemName]'
            },
        }
        
    def selectApi(self, text):
        _gongan = SigonganAI('')
        prompt = '너는 온라인 쇼핑몰 고객을 응대하는 AI 챗봇이야.'
        prompt += '너가 질문에 더 잘 대답할 수 있도록 사용할 수 있는 API 리스트를 줄게.'
        prompt += '아래 질문에 대해 너가 사용할 api를 선택해서 api 이름만 대답해. 다른말 하지마. 적절한 api가 없으면 "none" 이라고 대답해. \n'
        prompt += f'질문 : {text}\n'
        prompt += f'API list = {self.apiList}'
        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT()
        return answer
    
    
if __name__=="__main__":
    agent = Agent()
    while True:
        text = input()
        api = agent.selectApi(text)
        print(api)