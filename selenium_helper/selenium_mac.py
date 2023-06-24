from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome('/usr/local/bin/chromedriver')

driver.get('https://www.coupang.com/vp/products/172740098')

imgs = driver.find_elements(By.CLASS_NAME, "subType-IMAGE")
list = []
for img in imgs:
    list.append(img.find_element(By.TAG_NAME, "img").get_attribute("src"))
print(list)