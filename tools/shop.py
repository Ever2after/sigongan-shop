from . import coupang, naver, daangn, coupang_ict

class Shop:
    def __init__(self, keyword, options = [], items = []):
        self.keyword = keyword
        self.options = options
        self.items = items

    def getItems(self, num):
        items = []
        
        #### Coupang ####
        '''        
        _coupang = coupang.Coupang()
        c_keyword = keyword
        for option in options[:2]:
            c_keyword += f' {option}'
        c_items = _coupang.get_list(c_keyword, 1)
        '''
        
        #### Coupang ICT #### 
        _coupang = coupang_ict.CoupangICT()
        c_items = _coupang.get_items_by_keyword(self.keyword)['products']
        if len(c_items) < num:
            items = list(map(lambda x: self.updateDict(x, 'api', 'coupang'), c_items))
            _naver = naver.Naver()
            n_items = _naver.get_list(self.keyword, num - len(c_items))
            items += list(map(lambda x: self.updateDict(x, 'api', 'naver'), n_items))
        else:
            items = list(map(lambda x: self.updateDict(x, 'api', 'coupang'), c_items[:num]))

        _items = []
        for item in items:
            if item['api']=='coupang':
                _items.append({
                    'name': item['name'],
                    'option': item['option'],
                    'discount_rate': item['discount_rate'],
                    'price': item['price'],
                    'brand': item['brand'],
                    'reviews': item['reviews'],
                    'ratings': item['ratings'],
                    'url': f'https://coupang.com/vp/products/{item["group"]}',
                    'express_shipping': item['express_shipping'],
                    'highest_price': item['highest_price'],
                    'lowest_price': item['lowest_price'],
                    'membership_price': item['membership_price'],
                    'api': item['api']
                })
            else :
                _items.append(item)
        self.items = _items
        return _items
    
    def itemIntro(self):
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
        answer = f'{self.keyword} 추천 결과입니다. 조건: {" / ".join(self.options)}\n' #+ answer       
        return answer
    
    def itemDisplay(self):
        display = ''
        for item in self.items:
            display += '\n'
            if(item['api']=='coupang'):
                display += f'상품명: {item["name"]}\n'
                display += f'가격: {item["price"]} (쿠팡)\n'
                display += f'리뷰: {item["reviews"]}, 평점: {item["ratings"]}\n'
                display += f'링크: {item["url"]}\n'
            elif(item['api']=='naver'):
                display += f'상품명: {item["title"].replace("<b>", "")}\n'
                display += f'가격: {item["lprice"]} ({item["mallName"]})\n'
                display += f'브랜드: {item["brand"]}\n'
                display += f'링크: {item["link"]}\n'
        return display
        
    def updateDict(self, dict, key, value):
        dict.update({key: value})
        return dict
        