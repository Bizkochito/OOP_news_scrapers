import datetime
import pickle
import requests
from bs4 import BeautifulSoup as bs
import os
import json
from functools import partial
from src.scrapers.article import Article


class Scraper():
    def __init__(self):
        self.feeds_url = ""
        self.load_file = ""
        self.save_file = ""
        self.urls_list = []
        self.retry_list = []
        self.process_date = datetime.datetime.today
        self.session = 

    def get_links(self):
        pass

    def get_article(self):
        pass

    def write_article(self):
        pass

class KnackScraper(Scraper):
    feeds_url = "https://www.knack.be/news-sitemap.xml"
    def __init__(self):
        super().__init__()

    def get_links(self):
        page = self.session.get(self.feeds_url).text
        soup = bs(page, "html.parser")
        for link in soup.find_all("loc"):
            yield link.text
            
    def get_article(self, task):
        container = {}
        response = self.session.get(url)
        if response.status_code!= 200:
            print(response.status_code)
            return 
        soup = bs(response.content, "html.parser")
        container["source"] = self.feeds_url.split(".")[1]
        container["url"] = url
        title = soup.find_all("h1")
        if title :
            article_title = title[0].text.strip()
            container["title"] = article_title
        else :
            print("no title")

        elements = soup.find_all("p", attrs={"class": None})
        if elements :
            text_list = [element.get_text() for element in elements]
            container["text"] = "\n".join(text_list)
        else :
            print("no articles")

        published_time = soup.find('script', {"type": "application/ld+json"})
        container["date"] = ""
        if published_time:
            data = json.loads(published_time.text, strict=False)
            published_date = data["@graph"][0]["datePublished"]
            container["date"] = published_date

        return Article(task.id, 
                       container["url"], 
                       container["text"], 
                       container["date"], 
                       container["source"], 
                       "nl")   

    def write_article(self):
        pass

class LesoirScraper(Scraper):

    def __init__(self):
        pass
    def get_links(self):
        pass

    def get_article(self):
        pass

    def write_article(self):
        pass
    


