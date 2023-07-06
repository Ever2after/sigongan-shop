import sys
from pathlib import Path
from fastapi import FastAPI, Request
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))
sys.path.append('../selenium_helper')

from selenium_helper import selenium_test, selenium_mac

headers = {
    "authority": "www.coupang.com",
    "method": "GET",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36",
    "sec-ch-ua-platform": "macOS",
    "cookie": "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;"
}

#sel = selenium_mac.SeleniumTest()

app = FastAPI()

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post('/bs4')
async def get_bs4(request: Request):
    body = await request.json()
    url = body['url']
    try:
        response = requests.get(url, headers=headers)
        return response.text
    except Exception as e:
        return False
    
@app.post('/sel')
async def get_bs4(request: Request):
    body = await request.json()
    url = body['url']
    type = body['type']
    platform = body['platform']
    if type=='general':
        try:
            driver = selenium_test.SeleniumTest().initDriver(url)
            html = driver.page_source
            driver.quit()
            return html
        except Exception as e:
            return False
    elif type=='image':
        if platform=='coupang':
            try:
                driver = selenium_test.SeleniumTest().initDriver(url)
                imgs = driver.find_elements(By.CLASS_NAME, "subType-IMAGE")
                return [img.find_element(By.TAG_NAME, "img").get_attribute("src") for img in imgs]
            except:
                return False
        else:
            return False
    else:
        return False

    
    
    
