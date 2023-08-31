import logging
import typing

class Task():

    tasks_logger = logging.getLogger("Task")
    tasks_logger.setLevel(logging.WARNING)

    def __init__(self, scraper, url: str) -> None:
        self.id = None 
        self.scraper = scraper
        self.url = url
        self.retry_counter = 0

    def set_id(self, _id):
        self.id = _id


    def process(self):
        try:
            return self.scraper.get_article(self)
        except:
            self.tasks_logger.warning(f"Issue processing Task at url: {self.url}")
            self.retry_counter += 1
            return self
        
    def describe(self, print_option = False):
        msg = (f' Task id (unknown), scraping {self.url}, using the {self.scraper.describe()}.')
        if print_option:
            print(msg)
        return (f' Task id (unknown), scraping {self.url}, using the {self.scraper.describe()}.')