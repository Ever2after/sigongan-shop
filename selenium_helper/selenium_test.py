from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent={0}'.format(user_agent))
driver = webdriver.Chrome('chromedriver',options=options)
# 아무런 경고가 없다면 이상없이 작동되는 것입니다

class SeleniumTest:
    def __init__(self, url):
        self.url = url
        driver.get(self.url)
        driver.implicitly_wait(1)
        # 페이지 이동
        #스크롤 전 높이(자바 스크립트 명령어 실행)
        before_h = driver.execute_script("return window.scrollY")

        #무한 스크롤
        while True:
            # 맨 아래로 스크롤을 내리기
            driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

            # 스크롤 사이 페이지 로딩 시간 추가
            time.sleep(1)

            # 스크롤 후 높이
            after_h = driver.execute_script("return window.scrollY")

            if after_h == before_h:
                break
            before_h = after_h

    def get_img(self):
        list = []
        imgs = driver.find_elements(By.CLASS_NAME, "subType-IMAGE") # "subType-IMAGE")
        print(imgs)
        for img in imgs:
            list.append(img.find_element(By.TAG_NAME, "img").get_attribute("src"))
        return list
    
    def close(self):
        driver.close()


if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome('chromedriver',options=options)
    # 아무런 경고가 없다면 이상없이 작동되는 것입니다
    
    sel = SeleniumTest('https://www.coupang.com/vp/products/172740098')
    imgs = sel.get_img()
    print(imgs)

