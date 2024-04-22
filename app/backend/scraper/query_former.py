from abc import ABC, abstractmethod

from app.backend.utility.constants import SearchEngines, Status


class LinkFormer(ABC):
    @abstractmethod
    def get_url(algorithm_name, website):
        pass

class GoogelLinkFormer(LinkFormer):
    def get_url(algorithm_name, website):
        query = f"site:{website} " if website else ""
        query += f'{algorithm_name}'
        query = query.replace(" ", "+")
        return f"https://www.google.com/search?q={query}"


class Query:
    def __init__(self, algorithm_name, website=None, search_engine="google") -> None:
        self.algorithm_name = algorithm_name
        self.website = website
        self.search_engine = search_engine
        self.url = None
        self.form_url()
        self.status = Status.queued

    def form_url(self):
        builder = None
        if self.search_engine == SearchEngines.google:
            builder = GoogelLinkFormer
        self.url = builder.get_url(self.algorithm_name, self.website)
