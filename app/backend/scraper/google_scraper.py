from typing import Dict, List
from bs4 import BeautifulSoup
import requests
from random import choice

from app.backend.scraper.scraper_base import BaseScraper
from app.backend.scraper.query_former import Query
from app.backend.utility.constants import Status


class GoogleScraper(BaseScraper):
    def __init__(self, ignore_proxies=True) -> None:
        self.headers = self.load_headers()
        self.proxies = []
        if not ignore_proxies:
            self.proxies = self.load_proxie_list()
    
    def load_proxie_list(self) -> List[str]:
        pass

    def load_headers(self) -> List[Dict[str, str]]:
        return [{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'}]

    def scrape_query(self, query:Query):
        data = requests.get(query.url, headers=choice(self.headers))
        if data.status_code != 200:
            query.status = Status.failed
            return None
        soup = BeautifulSoup(data.content, "html.parser")
        results = []
        for g in soup.find_all('div',  {'class':'g'}):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                description="-"
                try:
                    description = g.find('div', {'data-sncf':'1'}).find_all('div')[0].find_all('span')[-1].text

                    # description cleanup
                    description = description.replace('\xa0', "")
                    description = description.replace('...', "")
                except Exception as e:
                    pass
                results.append({"title": str(title), "link": str(link), "description": str(description)})
        return results
