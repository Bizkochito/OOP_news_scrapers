import datetime
import pickle
import requests
from bs4 import BeautifulSoup as bs
import os
import json
from functools import partial
from article import Article
from task import Task

class Scraper():
    def __init__(self):
        self.feeds_url = ""
        self.load_file = ""
        self.save_file = ""
        self.urls_list = []
        self.retry_list = []
        self.process_date = datetime.datetime.today
        self.session = requests.Session()

    def get_links(self):
        pass

    def create_tasks(self):
        return [Task(self, url) for url in self.get_links()]

    def get_article(self):
        pass

    def write_article(self):
        pass

    def describe(self):
        return "Generic scraper"

class KnackScraper(Scraper):
    feeds_url = "https://www.knack.be/news-sitemap.xml"

    def get_links(self):
        print("Fetching knack.be urls")
        page = self.session.get("https://www.knack.be/news-sitemap.xml").text
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

    def describe(self):
        return "knack.be scraper"

class LesoirScraper(Scraper):

    def get_links(self):
        print("Fetching Lesoir urls")
        response = requests.get("https://www.lesoir.be/18/sections/le-direct")
        soup = bs(response.content, "html.parser")
        links = soup.select("h3 > a")
        base_url = "https://www.lesoir.be"
        urls = [link.get("href") for link in links]
        urls = [url if "//" in url else base_url + url for url in urls]
        return urls

    def get_article(self):
        pass

    def write_article(self):
        pass

    def describe(self):
        return "lesoir.be scraper"
    


