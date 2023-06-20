from ai import *

class Parser:
    def getFeature(self, messages, data):
        text = messages[-1]['content']
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
        messages = [
            {"role": "user", "content": f"설명: {text} \n 상품 이름 -> keyword, 상품 조건 -> options. output -> json. json 외에 다른 답은 하지마."},
            {"role": "user", "content": "평점좋고 저렴한 10만원대 게이밍 키보드 추천해줘"},
            {"role": "assistant", "content": f"{example1}"},
            {"role": "user", "content": "가을에 입을 만한 베이지 계열 오프숄더 블라우스 찾아줘. 에이블리에서 파는거면 좋겠어"},
            {"role": "assistant", "content": f"{example2}"},
            {"role": "user", "content": "모니터에 다는 led 등 사고싶어"},
            {"role": "assistant", "content": f"{example3}"},
            {"role": "user", "content": text}
        ]
        _gongan.initMessage(messages)
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

    def getReportTitle(self, text):
        prompt = '아래 문의 내용을 아주 짧은 제목으로 요약해줘\n'
        prompt += '[예시1]\n'
        prompt += '문의 내용 : 8만원 이하의 들고 다닐 수 있는 녹음기를 추천해주세요. 5시간 이상 녹음이 가능했으면 좋겠어요.\n'
        prompt += '제목 : 휴대용 녹음기\n'
        prompt += '[예시2]\n'
        prompt += '문의 내용 : 어깨끈이 달린 오프숄더 블라우스를 사고싶은데 색은 상관없구 아무 무늬가 없고 프릴 달린거나 레이스가 있어도 상관없어요.\n'
        prompt += '제목 : 오프숄더 블라우스\n'
        prompt += f'문의 내용 : {text}\n'
        prompt += '제목 : '
        _gongan = SigonganAI('')
        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT()
        return answer