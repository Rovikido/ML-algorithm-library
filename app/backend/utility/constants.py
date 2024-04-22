from enum import Enum


class SearchEngines(Enum):
    google = 'google.com'
    bing = 'bing.com'
    startpage = 'startpage.com'


class Status(Enum):
    queued = -1
    failed = 0
    success = 1
    
