from abc import ABC, abstractmethod
from typing import List, Dict

from app.backend.scraper.query_former import Query


class BaseScraper(ABC):
    """
    Base class for abstract factory. Intended to be a parent of scrapers for different search engines
    """
    @abstractmethod
    def load_headers(self) -> List[Dict[str, str]]:
        pass
    
    @abstractmethod
    def load_proxie_list(self) -> List[str]:
        pass

    @abstractmethod
    def scrape_query(self, query:Query):
        pass
