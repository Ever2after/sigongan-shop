import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium_test import *

class Coupang:
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

    def item_list_url(self, keyword, page):
        return f"https://www.coupang.com/np/search?component=&q={keyword}&channel=user&page={page}"
    
    def get_list(self, keyword, page):
        list = []
        for i in range(1, page+1):
            response = requests.get(self.item_list_url(keyword, i), headers = self.headers, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            productlist = soup.find_all('li', attrs={"class":"search-product"})
            for product in productlist:
                name = product.find('div', attrs={"class":"name"})
                price = product.find('strong', attrs={"class":"price-value"})
                rating = product.find('em', attrs={"class":"rating"})
                rating_total_count = product.find('span', attrs={"class":"rating-total-count"})
                link = 'https://www.coupang.com' + product.find('a')['href'].split('?')[0]
                list.append({
                    "name": name.get_text() if name else name,
                    "price": int(price.get_text().replace(',', '')) if price else price,
                    "rating": float(rating.get_text()) if rating else rating,
                    "rating_total_count": rating_total_count.get_text() if rating_total_count else rating_total_count,
                    "link": link
                })
        df = pd.DataFrame(list)
        return df

    def link_search(self, url):
        response = requests.get(url, headers = self.headers, verify=False, timeout=(3.05, 27))
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h2', attrs={"class":"prod-buy-header__title"}).get_text()
        price = soup.find('span', attrs={"class":"total-price"}).strong.get_text()
        shipping = soup.find('div', attrs={"class":"prod-shipping-fee-message"}).span.em.get_text()
        description = soup.find('ul', class_="prod-description-attribute").find_all('li')
        description = list(map(lambda x: x.get_text(), description))

        seleniumTest = SeleniumTest(url)
        imgUrl = seleniumTest.get_img()
        #seleniumTest.close()
        return {
            'name': name,
            'price': price,
            'shipping': shipping,
            'description': description,
            'imgUrl': imgUrl,
        }
        
    def get_promotion(self):
        url = "https://partners.coupang.com/#affiliate/ws/events?page=1"
        response = requests.get(url, headers = self.headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all("div", class_ = "ant-card card--3Bacuk ant-card-hoverable")
        list = []
        for item in items:
            img = item.find("img")['src']
            desc = item.find("div", class_ = "ant-card-meta-title")
            list.append({
                'imgUrl': img,
                'description': desc,
            })
        return pd.DataFrame(list)
        