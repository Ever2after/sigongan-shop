from . import coupang, naver, daangn, coupang_ict

class ShopItem:
    def getItems(self, keyword, options, num):
        items = []
        _coupang = coupang_ict.CoupangICT()
        c_items = _coupang.get_items_by_keyword(keyword)['products']
        if len(c_items) < 3:
            items = list(map(lambda x: self.updateDict(x, 'api', 'coupang'), c_items))
            _naver = naver.Naver()
            n_items = _naver.get_list(keyword, 3 - len(c_items))
            items += list(map(lambda x: self.updateDict(x, 'api', 'naver'), n_items))
        else:
            items = list(map(lambda x: self.updateDict(x, 'api', 'coupang'), c_items[:3]))
        return items
        
    def updateDict(self, dict, key, value):
        dict.update({key: value})
        return dict
        