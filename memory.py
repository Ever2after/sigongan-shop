class Memory:
    def __init__(self, messages=[]):
        self.messages = messages

    def initMessage(self, messages):
        self.messages = messages
    
    def appendMessage(self, role, content):
        self.messages.append({
            'role': role, 'content': content
        })
    
    def getMessages(self, n):
        l = len(self.messages)
        n = n if n<=l else l
        return self.messages[l-n:]


class Recommendation:
    def __init__(self, keywords = [], options = []):
        self.keywords = keywords
        self.options = options
        
class Description:
    def __init__(self, link):
        self.link = link
        self.description = '상품 상세 정보입니다' 

class Product:
    def __init__(self, name, price, rating, count, link):
        self.name = name
        self.price = price
        self.rating = rating
        self.count = count
        self.link = link
        self.description = ''
