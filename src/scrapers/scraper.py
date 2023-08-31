import datetime
import pickle
import requests
from bs4 import BeautifulSoup as bs
from dateutil import parser
import os
import json
import unicodedata
import ssl
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
        # Output: list or generator object
        return []

    def create_tasks(self):
        return [Task(self, url) for url in self.get_links()]

    def get_article(self, task):
        # Output: Article object expected. Task is acceptable.
        return task

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

    def get_article(self, task):

        def find_article_title(soup) -> str:
            article_title = soup.find("h1").text
            return article_title
        
        # selector for geeko.lesoir.be urls
        def geeko_selector(soup) -> tuple:
            div = soup.find("div", attrs={"class": "post-content-area"})
            paragraphs = div.find_all("p")
            if "Suivez Geeko sur Facebook" in paragraphs[-1].text:
                paragraphs = paragraphs[:-1]
            text = ""
            return paragraphs, text
        
        # selector for sosoir.lesoir.be urls
        def sosoir_selector(soup) -> tuple:
            h2 = soup.find("h2", attrs={"class": "chapeau"}).text.strip()
            div = soup.find("div", attrs={"id": "artBody"})
            paragraphs = div.find_all("p")
            if "sosoir.lesoir.be" in paragraphs[-1].text:
                paragraphs = paragraphs[:-1]
            text = h2
            return paragraphs, text


        # selector for www.lesoir.be and soirmag.lesoir.be urls
        def lesoirmag_selector(soup) -> tuple:
            article = soup.find("article", attrs={"class": "r-article"})
            paragraphs = article.find_all("p")
            if "www.soirmag.be" in paragraphs[-1].text:
                paragraphs = paragraphs[:-1]
            text = ""
            return paragraphs, text


        def find_article_text(soup, url: str) -> str:
            if "sosoir" in url:
                paragraphs, text = sosoir_selector(soup)
            elif "geeko" in url:
                paragraphs, text = geeko_selector(soup)
            else:
                paragraphs, text = lesoirmag_selector(soup)
            for p in paragraphs:
                p_text = unicodedata.normalize("NFKD", p.text.strip())
                text += p_text
            return text


        def find_published_date(soup) -> str:
            script = soup.find("script", {"type": "application/ld+json"})
            data = json.loads(script.text, strict=False)
            try:
                published_date = data["@graph"][0]["datePublished"]
            except:
                published_date = data["datePublished"]
            date = parser.parse(published_date)
            return date
               
        dict = {"url": task.url}
        link_response = requests.get(dict["url"])
        link_soup = bs(link_response.content, "html.parser")
        print(" Adding article text ...")
        dict["text"] = find_article_text(link_soup, dict["url"])
        print(" Adding date ...")
        dict["date"] = find_published_date(link_soup)
        print(" Adding title ...")
        dict["title"] = find_article_title(link_soup)
        print(" Adding language ...")
        dict["language"] = "fr"
        return Article()


    def describe(self):
        return "lesoir.be scraper"
    


