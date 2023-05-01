from ai import *

class Semantic:
    def past(self, text):
        _gongan = SigonganAI('')
        _gongan.appendMessage('user', '너는 온라인쇼핑몰의 상품을 판매하는 도우미야.')
        _gongan.appendMessage('user', f'질문 : "{text}". 이 질문의 카테고리를 분류해줘. \
                            카테고리 = ["과거에 제시한 상품에 대한 질문", "새로운 상품에 대한 질문", "그 외 질문"] \
                            ')
        answer, _ = _gongan.getGPT()
        if (not answer): return False
        elif ('과거' in answer): return 0
        elif('새로운' in answer): return 1
        else: return 2

    def queryType(self, text):
        _gongan = SigonganAI('')
        _gongan.appendMessage('user', f'다음 질문이 어떤 의도인지 분류해줘. 중복 선택도 가능해 \
            카테고리 = ["상품 검색, 추천 요구", "상품 상세 설명, 판매 정보 요구", "그 외 단순 질문"].     \
            질문 : {text}.   \
            ')
        answer, _ = _gongan.getGPT()
        if (not answer): return False
        elif('추천' in answer): return 0
        elif('정보' in answer): return 1
        else: return 2

    def getFeature(self, text):
        _gongan = SigonganAI("")
        example1 = {
            "keyword": "키보드",
            "options": ["게이밍", "10만원대", "저렴한", "평점 좋은"]
        }
        example2 = {
            "keyword": "오프숄더 블라우스",
            "options": ["가을에 입을만한", "베이지 계열", "에이블리"]
        }
        example3 = {
            "keyword": "모니터 led 등",
            "options": []
        }
        message = [
            {"role": "user", "content": f"설명: {text} \n 상품 이름 -> keyword, 상품 조건 -> options. output -> json. json 외에 다른 답은 하지마."},
            {"role": "user", "content": "평점좋고 저렴한 10만원대 게이밍 키보드 추천해줘"},
            {"role": "assistant", "content": f"{example1}"},
            {"role": "user", "content": "가을에 입을 만한 베이지 계열 오프숄더 블라우스 찾아줘. 에이블리에서 파는거면 좋겠어"},
            {"role": "assistant", "content": f"{example2}"},
            {"role": "user", "content": "모니터에 다는 led 등 사고싶어"},
            {"role": "assistant", "content": f"{example3}"},
            {"role": "user", "content": text}
        ]
        _gongan.initMessage(message)
        answer, _ = _gongan.getGPT()
        if (not answer): return False

        answer = answer.replace('\'', '\"')
        answer = '{' + answer.split('{')[-1]
        answer = answer.split('}')[0] + '}'
        try:
            _json = json.loads(answer)
        except:
            return False
        return _json
    

    def additionalOptions(self, info):
        example1 = {
            "options": ["가격", "브랜드", "성능"]
        }
        example2 = {
            "options": ["맛", "용량", "탄산여부"]
        }
        _gongan = SigonganAI('')
        _gongan.appendMessage('system', '너는 온라인 쇼핑몰의 상품을 소개하는 도우미야.')
        _gongan.appendMessage('user', f'나는 {info["keyword"]}를 구매하려고 해. {info["options"]}의 조건 외에 더 고려해보면 좋을 만한 조건, 선택지를 json으로 제시해줘. json 외 다른 답은 하지마. \
                            예시1: {example1}, 예시2: {example2}')
        answer, _ = _gongan.getGPT()
        if (not answer): return False
        answer = answer.replace('\'', '\"')
        answer = '{' + answer.split('{')[-1]
        answer = answer.split('}')[0] + '}'
        try:
            _json = json.loads(answer)
        except:
            print(answer)
            return False
        return _json