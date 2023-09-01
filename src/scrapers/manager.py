try:
   import cPickle as pickle
except:
   import pickle
import os.path
import pandas as pd
import datetime
import requests
from pathos.multiprocessing import ProcessingPool as Pool
import scraper as sc
from task import Task
from article import Article


class ScrapingManager():
    save_file = "savestate"
    articles_file = "articles.csv"
    
    def __init__(self):
        self.scrapers=[]
        self.tasks = []
        self.df = pd.DataFrame()
        self.last_date = datetime.datetime.today()
        self.id_counter = 1
        self.session = requests.Session()

    def add_scraper(self, Scraper):
        self.scrapers.append(Scraper)

    def get_tasks(self):
        with Pool() as pool:
            for task_list in pool.map(lambda scraper: scraper.create_tasks(), self.scrapers):
                self.tasks.extend(task_list)
        self.set_task_ids()
        print("done fetching tasks")

    def set_task_ids(self):
        for task in self.tasks:
            if task.id:
                continue
            task.set_id(self.id_counter)
            self.id_counter += 1

    def process_tasks(self, hash = None):
        with Pool() as pool:
            self.tasks = pool.map(lambda task: task.process(), self.tasks)

    def split_articles(self):
        tasks_buffer = []
        articles_buffer = []
        for item in self.tasks:
            if type(item) == Article:
                articles_buffer.append(item.to_dict())
            else :
                tasks_buffer.append(item)
        self.tasks = tasks_buffer
        return articles_buffer

    def write_articles(self, articles_list):
        df = pd.DataFrame(articles_list)
        df.drop_duplicates(["url"])
        df.to_csv(self.articles_file, mode = "a", header = not os.path.exists(self.articles_file))

    def process_and_save(self):
        self.get_tasks()
        self.process_tasks()
        self.write_articles(self.split_articles())

    def resume():
        pass

    def save(self):
        f = open(self.save_file, 'wb')
        pickle.dump(self, f, 2)
        f.close()

    @classmethod
    def loader(self):
        with open(self.save_file, 'rb') as pickle_file:
            return pickle.load(pickle_file)



if __name__ == "__main__":

    #scrapingManager = ScrapingManager.loader()
    scrapingManager = ScrapingManager()
    scrapingManager.add_scraper(sc.KnackScraper())
    scrapingManager.add_scraper(sc.LesoirScraper())

    scrapingManager.process_and_save()
