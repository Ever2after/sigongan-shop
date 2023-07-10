import sys
from pathlib import Path
wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))
from ai import *
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Parser:
    def __init__(self):
        self.headers = {
            "authority": "www.coupang.com",
            "method": "GET",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36",
            "sec-ch-ua-platform": "macOS",
            "cookie": "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;"
        }
    
    def getFeature(self, messages, data):
        text = messages[-1]['content']
        _gongan = SigonganAI()
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
        if _json['keyword'] == '':
            return False
        return _json
    

    def additionalOptions(self, info):
        example1 = {
            "options": ["가격", "브랜드", "성능"]
        }
        example2 = {
            "options": ["맛", "용량", "탄산여부"]
        }
        _gongan = SigonganAI()
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

    def getReportTitle(self, url = '', text = '', messages = []):
        response = requests.post('http://34.70.221.73:8000/bs4', json={
            'url' : url,
            'type' : 'meta'
        })
        urlData = response.json()
        
        gongan = SigonganAI()
        
        prompt = '아래 문의 내용을 아주 짧은 제목으로 요약해줘\n'
        prompt += '[예시1]\n'
        prompt += '문의 내용 : 8만원 이하의 들고 다닐 수 있는 녹음기를 추천해주세요. 5시간 이상 녹음이 가능했으면 좋겠어요.\n'
        prompt += '제목 : 휴대용 녹음기\n'
        prompt += '[예시2]\n'
        prompt += '문의 내용 : 어깨끈이 달린 오프숄더 블라우스를 사고싶은데 색은 상관없구 아무 무늬가 없고 프릴 달린거나 레이스가 있어도 상관없어요.\n'
        prompt += '제목 : 오프숄더 블라우스\n'
        if(text): prompt += f'문의 내용 : {text}\n'
        if(url): prompt += f'문의한 상품의 정보 : {urlData}]\n'
        if(messages != []): prompt += f'대화 내용 : {messages}\n'
        prompt += '제목 :' 
        
        gongan.appendMessage('user', prompt)
        answer, _ = gongan.getGPT()
        return answer
    
    def summaryDetails(self, text):
        example1 = [
            '7.1채널의 서라운드 기술로 더 우수한 입체 사운드 제공',
            '정확한 사운드 방향을 전달하여 게이머에게 최적화된 게이밍 헤드셋',
            'C-MEDIA사의 CM108B 칩셋을 장착하여 생생한 음질의 사운드 제공',
            '밀폐형 디자인 적용으로 편안하고 안락한 착용감 제공',
            '마이크 120도 방향 조절 가능, 고감도 플렉시블 마이크 탑재'
        ]
        example2 = [
            '대두식이섬유 2,000mg 함유 (1팩(190mL)기준)',
            '콩의 비린맛 없애고 풍부한 맛을 위한 특수 공법(EI) 적용',
            'HACCP 인증 및 엄격한 품질관리',
            '환경을 생각한 국제산림협의회 인증 종이팩'
        ]
        prompt = '아래는 어떤 상품에 대한 프로모션 문구들이야\n'
        prompt += '각 문단별로 중요한 내용들을 깔끔하게 정리해줘\n'
        prompt += '만약에 규칙이 없거나 어색한 글들은 무시하고 정리하지 마\n'
        prompt += f'[예시1] : {example1}\n'
        prompt += f'[예시2] : {example2}\n'
        prompt += f'프로모션 문구 : {text}\n'
        prompt += f'10가지 이하로 정리해줘'
        prompt += '정리 내용 : '
        _gongan = SigonganAI()
        _gongan.initMessage([{'role': 'system', 'content': '너는 이제 상품에 대해 설명하고 정리하는 도우미야'}])
        _gongan.appendMessage('user', prompt)
        answer, _ = _gongan.getGPT('gpt-3.5-turbo-16k-0613')
        return answer
    
    def urlParser(self, text):
        urls = re.findall("http[s]*:\/\/(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9][a-zA-Z0-9-_/.?=]*", text)
        return urls
                


if __name__ == '__main__':
    parser = Parser()
    answer = parser.urlParser("안녕하세요 ㅋㅋㅋhttps://naver.com 하위~~~")
    print(answer)