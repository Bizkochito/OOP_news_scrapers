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
import task

class ScrapingManager():
    save_file = "savestate"
    articles_db = "articles.json"
    
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
        print("done fetching tasks")

    def set_task_ids(self):
        for task in self.tasks_list:
            if task.id:
                continue
            task.set_id(self.id_counter)
            self.id_counter += 1

    def process_tasks(self):
        with Pool() as pool:
            self.tasks_list = pool.map(lambda task: task.process(), self.tasks_list)
        


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
    response = requests.get("https://www.lesoir.be/18/sections/le-direct")

    scrapingManager.get_tasks()
    scrapingManager.set_task_ids()
    scrapingManager.process_tasks()
    for task in scrapingManager.tasks:
        print(len(task))