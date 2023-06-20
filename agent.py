from ai import *

class Agent():
    def __init__(self):
        self.toolList = {
            'itemLists': {
                'description' : 'search item lists from given keyword. you can use it for product recommendation',
                'output': '[item1, item2, item3, ...]'
            },
            'details': {
                'description' : 'get detailed information of specific item such as price, delivery, spec, review',
                'output' : '{name, price, delivery date, shipping price, spec, brand, review, ...}'
            },
        }
        
    def selectApi(self, messages, data):
        text = messages[-1]['content']
        _gongan = SigonganAI('')

        prompt = 'You are the online shopping mall AI guidence.'
        prompt += 'You should determine the appropriate tool to use at answering the following question. If dont need any tools, say "none".'
        prompt += 'You can only say the name of the tool. \n'
        prompt += f'Convesation : {text}\n'
        prompt += f'Tool list = {self.toolList}'

        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT()
        return answer
    
    
if __name__=="__main__":
    agent = Agent()
    while True:
        text = input()
        api = agent.selectApi(text)
        print(api)