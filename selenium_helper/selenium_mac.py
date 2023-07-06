from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SeleniumTest:
    def __init__(self):
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')

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
        imgs = self.driver.find_elements(By.CLASS_NAME, "subType-IMAGE") 
        for img in imgs:
            list.append(img.find_element(By.TAG_NAME, "img").get_attribute("src"))
        return list
    
    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()
        
if __name__ == '__main__':
    sel = SeleniumTest()
    sel.initDriver('https://coupang.com/vp/products/7225403435')
    list = sel.get_coupang_img()
    print(list)
    