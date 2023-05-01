import requests
from bs4 import BeautifulSoup
import pandas as pd

class Daangn:
    #def __init__(self):
    def get_list(self, keyword):
        url = f"https://www.daangn.com/search/{keyword}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all("a", class_="flea-market-article-link")
        list = []
        for product in products:
            article_title = product.find("span", class_="article-title").get_text().replace("\n",'').strip()
            article_content = product.find("span", class_="article-content").get_text().replace("\n",'').strip()
            article_region = product.find("p", class_ = "article-region-name").get_text().replace("\n",'').strip()
            article_price = product.find("p", class_ = "article-price").get_text().replace("\n",'').strip()
            article_imgUrl = product.find("div", class_="card-photo").find("img")["src"]
            article_link = "https://www.daangn.com/" + product["href"]
            list.append({
                "name": article_title,
                "description": article_content,
                "region": article_region,
                "price": article_price,
                "imgUrl": article_imgUrl,
                "link": article_link
            })
        return list