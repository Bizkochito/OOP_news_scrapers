try:
   import cPickle as pickle
except:
   import pickle
import os.path
import pandas as pd
import datetime
import requests


class ScrapingManager():
    save_file = "savestate"
    articles_db = "articles"
    
    def __init__(self):
        self.scrapers=[]
        self.tasks = []
        self.df = pd.DataFrame()
        self.last_date = datetime.datetime.today()
        self.session = requests.Session()


    def save(self):
        f = open(self.save_file, 'wb')
        pickle.dump(self, f, 2)
        f.close()

    def add_scraper(self, Scraper):
        self.scrapers.append(Scraper)

    @classmethod
    def loader(self):
        with open(self.save_file, 'rb') as pickle_file:
            return pickle.load(pickle_file)

    def resume():
        pass

if __name__ == "__main__":

    scrapingManager = ScrapingManager.loader()
