import requests

class CoupangICT:
    def __init__(self):
        self.url = 'https://api.kimgosu.vsolution.app/products'
        self.headers = {'Authorization' : 'Bearer 389|wxFe3R2xVdE2eFXII3pPH7lF5tFqaUp5o9RVkOQl'}
        
    def get_items_by_keyword(self, keyword):
        response = requests.get(self.url + '?keyword=' + keyword, headers = self.headers)
        return response.json()
    
    def get_item_by_id(self, product_id):
        response = requests.get(self.url + '/' + product_id, headers = self.headers)
        return response.json()
    
    def get_history(self, product_id):
        response = requests.get(self.url + '/' + product_id + '/histories', headers = self.headers)
        return response.json()

if __name__ == '__main__':
    coupang = CoupangICT()
    items = coupang.get_items_by_keyword('게이밍 키보드')
    print(items)
    