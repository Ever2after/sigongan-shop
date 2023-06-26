from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# 아무런 경고가 없다면 이상없이 작동되는 것입니다

class SeleniumTest:
    def __init__(self):
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        #f_user_agent = UserAgent()
        #proxy = FreeProxy(country_id=['US'], rand=True, anonym=True).get()
        #ip = proxy.split("://")[1]
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--incognito")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("disable-infobars")
        options.add_argument('user-agent={0}'.format(user_agent))
        '''
        PROXY = ip
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":PROXY,
            "ftpProxy":PROXY,
            "sslProxy":PROXY,
            "noProxy":None,
            "proxyType":"MANUAL",
            "autodetect":False
        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        '''
        self.driver = webdriver.Chrome(options=options)
        '''
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })
        '''
    def initDriver(self, url):
        self.url = url
        self.driver.get(self.url)
        self.driver.implicitly_wait(1)
        # 페이지 이동
        #스크롤 전 높이(자바 스크립트 명령어 실행)
        before_h = self.driver.execute_script("return window.scrollY")

        #무한 스크롤
        while True:
            # 맨 아래로 스크롤을 내리기
            self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

            # 스크롤 사이 페이지 로딩 시간 추가
            time.sleep(1)

            # 스크롤 후 높이
            after_h = self.driver.execute_script("return window.scrollY")

            if after_h == before_h:
                break
            before_h = after_h
        
        return self.driver

    def get_coupang_img(self):
        list = []
        imgs = self.driver.find_elements(By.CLASS_NAME, "subType-IMAGE") # "subType-IMAGE")
        for img in imgs:
            list.append(img.find_element(By.TAG_NAME, "img").get_attribute("src"))
        return list
    
    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    sel = SeleniumTest()
    sel.initDriver('https://www.coupang.com/vp/products/172740098')
    imgs = sel.get_coupang_img()
    sel.quit()

