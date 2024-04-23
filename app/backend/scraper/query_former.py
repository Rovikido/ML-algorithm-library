from abc import ABC, abstractmethod

from app.backend.utility.constants import SearchEngines, Status


class LinkFormer(ABC):
    """
    Abstract base class for generating search engine query URLs.
    """

    @abstractmethod
    def get_url(self, concept_name, website):
        """
        Abstract method to be implemented by subclasses for forming the search engine query URL.

        Args:
            concept_name (str): The concept to search for.
            website (str): The website to restrict the search to.

        Returns:
            str: The formed URL.
        """
        pass


class GoogelLinkFormer(LinkFormer):
    """
    Concrete subclass of LinkFormer for forming Google search query URLs.
    """

    def get_url(self, concept_name, website):
        """
        Form the Google search query URL based on the concept name and optional website.

        Args:
            concept_name (str): The concept to search for.
            website (str): The website to restrict the search to.

        Returns:
            str: The formed Google search query URL.
        """
        query = f"site:{website} " if website else ""
        query += f'{concept_name}'
        query = query.replace(" ", "+")
        return f"https://www.google.com/search?q={query}"


class Query:
    """
    Represents a search query.

    Attributes:
        concept_name (str): The concept to search for.
        website (str): The website to restrict the search to.
        search_engine (str): The search engine to use (default is "google").
        url (str): The formed URL for the search query.
        status (Status): The status of the query (default is Status.queued).
    """

    def __init__(self, concept_name, website=None, search_engine="google") -> None:
        """
        Initialize a Query object with the provided attributes.

        Args:
            concept_name (str): General concept name.
            website (str, optional): The website to restrict the search to. Defaults to None.
            search_engine (str, optional): The search engine to use. Defaults to "google".
        """
        self.concept_name = concept_name
        self.website = website
        self.search_engine = search_engine
        self.url = None
        self.form_url()
        self.status = Status.queued

    def form_url(self):
        """
        Form the URL for the search query based on the specified search engine.
        """
        builder = None
        if self.search_engine == SearchEngines.google:
            builder = GoogelLinkFormer()
        self.url = builder.get_url(self.concept_name, self.website)
