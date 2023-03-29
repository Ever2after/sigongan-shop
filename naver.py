import requests

class Naver:
    def __init__(self):
        self.headers = {
            "X-Naver-Client-Id" : "YvgavDiyG_9BVoblkBd0",
            "X-Naver-Client-Secret" : "MqZ1LrZ_E2",
        }
        self.url = "https://openapi.naver.com/v1/search/shop.json"
    
    def get_list(self, keyword, num):
        _num = 100 if num>100 else num
        payload = {
            "query": keyword,
            "display": _num,
            "start": 1,
            "sort": "sim", # sim, date, asc, dsc
            "exclude": "used:rental:cbshop",
        }
        response = requests.get(self.url, headers=self.headers, params=payload)
        return response.json()