from abc import ABC, abstractmethod

from app.backend.scraper.query_former import Query


class BaseScraper(ABC):
    @abstractmethod
    def load_headers(self, skip=False):
        pass
    
    @abstractmethod
    def load_proxies(self, skip=False):
        pass

    @abstractmethod
    def scrape_query(self, query:Query):
        pass
