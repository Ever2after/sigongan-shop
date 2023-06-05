from . import coupang, naver, daangn

class ShopItem:
    def getItems(self, keyword, options, num):
        _naver = naver.Naver()
        output = _naver.get_list(keyword, num)
        return output

        