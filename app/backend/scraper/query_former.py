from abc import ABC, abstractmethod

from app.backend.utility.constants import SearchEngines


class LinkFormer(ABC):
    @abstractmethod
    def get_link(algorithm_name, website):
        pass

class GoogelLinkFormer(LinkFormer):
    def get_link(algorithm_name, website):
        query = f"site:{website}" if website else ""
        query += f'{algorithm_name}'
        query.replace(" ", "+")
        return f"https://www.google.com/search?q={query}"


class Query:
    def __init__(self, algorithm_name, website=None, search_engine="google") -> None:
        self.algorithm_name = algorithm_name
        self.website = website
        self.search_engine = search_engine
        self.link = None
        self.form_link()
        self.is_completed = False

    def form_link(self):
        builder = None
        if self.search_engine == SearchEngines.google.value:
            builder = GoogelLinkFormer
        self.link = builder.get_link(self.algorithm_name, self.website)

    