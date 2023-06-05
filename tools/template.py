from ai import *

class Template:
    def itemReccommend(self, items, keyword, options):
        _gongan = SigonganAI('')
        prompt = "너는 온라인 쇼핑몰에서 상품 판매를 도와주는 AI 챗봇 '포미'야."
        prompt += f'고객이 {options}의 조건을 만족하는 {keyword}를 구매하려고 해'
        prompt += f'아래 상품들을 추천하는 이유를 간결하게 작성해줘\n'
        for idx, item in enumerate(items):
            prompt += f'{idx+1}번째 상품 정보 : {item}\n'
        prompt += '간단한 상품 추천 이유 2가지 : '
        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT()
        answer = f'{keyword} 추천 결과입니다. 조건: {" ".join(options)}\n' + answer       
        return answer