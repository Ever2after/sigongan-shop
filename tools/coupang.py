import requests
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import hmac
import hashlib
from time import gmtime, strftime

wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))
sys.path.append('../selenium_helper')
from selenium_helper import selenium_test, selenium_mac
from ai import *

load_dotenv()

# Crawling server url
crawling_server_url = 'http://34.70.221.73:8000' #os.getenv('CRAWLING_SERVER_URL')

# Coupang partners api url
coupang_partners_api_domain = "https://api-gateway.coupang.com"
coupang_partners_api_url = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"
coupang_partners_access_key = "9e20cccc-8d69-4a9b-bce6-64adb6729692" # os.getenv('COUPANG_PARTNERS_ACCESS_KEY')
coupang_partners_secret_key = "b1fbf2021aa5f39b747a49efc10169be0b0c43eb" # os.getenv('COUPANG_PARTNERS_SECRET_KEY')

class Coupang:
    def item_list_url(self, keyword, page):
        return f"https://www.coupang.com/np/search?component=&q={keyword}&channel=user&page={page}"
    
    def get_list(self, keyword, page):
        list = []
        for i in range(1, page+1):
            response = requests.get(self.item_list_url(keyword, i), headers = self.headers, verify=True)
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
                    "rating_total_count": int(rating_total_count.get_text().replace('(','').replace(')', '')) if rating_total_count else rating_total_count,
                    "link": link
                })
        df = pd.DataFrame(list)
        return df, list

    def link_search(self, url):
        response = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h2', attrs={"class":"prod-buy-header__title"}).get_text()
        price = soup.find('span', attrs={"class":"total-price"}).strong.get_text()
        shipping = soup.find('div', attrs={"class":"prod-shipping-fee-message"}).span.em.get_text()
        description = soup.find('ul', class_="prod-description-attribute").find_all('li')
        description = list(map(lambda x: x.get_text(), description))
        return {
            'name': name,
            'price': price,
            'shipping': shipping,
            'description': description,
        }
        
    def get_imageUrl(self, url):
        response = requests.post(f'{crawling_server_url}/sel', json={
            'url' : url,
            'type' : 'image',
            'platform' : 'coupang'
        })
        print(response.json())
        return response.json()['imgUrls']
        
    
    async def image_read(self, url):
        imgUrl = self.get_imageUrl(url)
        gongan = SigonganAI()
        _context, _chunks = await gongan.imageProcessor(imgUrl)
        context = ''
        for _chunk in _chunks:
            if len(_chunk)>40:
                context += _chunk
                context += '\n'
        return context
    
    def getDeeplink(self, urls):
        REQUEST = { "coupangUrls": urls }
        authorization = self.generateHmac('POST', coupang_partners_api_url, coupang_partners_secret_key, coupang_partners_access_key)
        url = "{}{}".format(coupang_partners_api_domain, coupang_partners_api_url)
        try:
            response = requests.request(method='POST', url=url,
                                        headers={
                                            "Authorization": authorization,
                                            "Content-Type": "application/json"
                                        },
                                        data=json.dumps(REQUEST)
                                        )
            return response.json()
        except:
            return False


    def generateHmac(self, method, url, secretKey, accessKey):
        path, *query = url.split("?")
        datetimeGMT = strftime('%y%m%d', gmtime()) + 'T' + strftime('%H%M%S', gmtime()) + 'Z'
        message = datetimeGMT + method + path + (query[0] if query else "")

        signature = hmac.new(bytes(secretKey, "utf-8"),
                            message.encode("utf-8"),
                            hashlib.sha256).hexdigest()

        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetimeGMT, signature)