import datetime
import logging



class Article():

    articles_logger = logging.getLogger("Article")
    articles_logger.setLevel(logging.WARNING)

    def __init__(self, _id: str, date, url: str = "", text: str = "", source: str = "", language: str = "fr" ) -> None:
        self._id = _id
        self.url = url
        self.text = text
        self.set_date(date)
        self.source = source
        self.language = language

    def set_date(self, date) -> None:
        try:
            if type(date) == datetime.date:
                self.date = date
            elif type(date) == datetime.datetime:
                self.date = date.todate()
        except:
            self.date = ""
            self.articles_logger.warning(f"Issue with the date at article {self._id}, url: {self.url}")

    


