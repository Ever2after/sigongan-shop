from ai import *

class Template:
    def itemReccommend(self, items, keyword, options):
        _gongan = SigonganAI('')
        prompt = "너는 온라인 쇼핑몰에서 상품 판매를 도와주는 AI 챗봇 '포미'야."
        prompt += f'고객이 {options}의 조건을 만족하는 {keyword}를 구매하려고 해'
        prompt += f'아래 상품들을 추천하는 이유를 간결하게 작성해줘\n'
        for idx, item in enumerate(items):
            prompt += f'{idx+1}번째 상품 정보 : {item}\n'
        prompt += '간단한 상품 추천 이유 3가지 : '
        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT()
        answer = f'{keyword} 추천 결과입니다. 조건: {" ".join(options)}\n' + answer       
        return answer
    
    def itemIntro(self, items, keyword, options):
        '''
        _gongan = SigonganAI('')
        prompt = "너는 온라인 쇼핑몰에서 상품 판매를 도와주는 AI 챗봇 '포미'야."
        prompt += f'고객이 {options}의 조건을 만족하는 {keyword}를 구매하려고 해'
        prompt += f'추천 상품들을 소개하는 문구를 다음 양식에 맞춰서 작성해줘\n'
        prompt += '소개 문구 예시 : 안녕하세요, ~ 이런 상품을 찾고 계시군요! 그러면 다음의 ~ 상품들은 어떠신가요?'
        prompt += '소개 문구 : '
        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT()
        '''
        answer = f'{keyword} 추천 결과입니다. 조건: {" / ".join(options)}\n' #+ answer       
        return answer
    
    def itemDisplay(self, items, keyword, options):
        display = ''
        for item in items:
            display += '\n'
            if(item['api']=='coupang'):
                display += f'상품명: {item["name"]}\n'
                display += f'가격: {item["price"]} (쿠팡)\n'
                display += f'리뷰: {item["reviews"]}, 평점: {item["ratings"]}\n'
                display += f'링크: https://www.coupang.com/vp/products/{item["group"]}\n'
            elif(item['api']=='naver'):
                display += f'상품명: {item["title"]}\n'
                display += f'가격: {item["lprice"]} ({item["mallName"]})\n'
                display += f'리뷰: {item["reviews"]}, 평점: {item["ratings"]}\n'
                display += f'링크: https://www.coupang.com/vp/products/{item["id"]}\n'
                
        return display