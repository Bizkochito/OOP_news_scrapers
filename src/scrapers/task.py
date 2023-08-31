import logging
import typing


class Task():

    tasks_logger = logging.getLogger("Task")
    tasks_logger.setLevel(logging.WARNING)

    def __init__(self, id: int, scraper: Scraper, url: str) -> None:
        self.id = id        
        self.scraper = scraper
        self.url = url


    def process(self):
        try:
            return self.scraper.get_article(self)
        except:
            self.tasks_logger.warning(f"Issue processing Task at url: {self.url}")
            return self