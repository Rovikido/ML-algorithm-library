import pytest
from app.backend.utility.constants import SearchEngines, Status
from app.backend.scraper.query_former import GoogelLinkFormer, Query

@pytest.fixture
def sample_query():
    return Query("Machine Learning", search_engine=SearchEngines.google.value)

def test_query_initialization(sample_query):
    assert sample_query.concept_name == "Machine Learning"
    assert sample_query.website is None
    assert sample_query.search_engine == SearchEngines.google.value
    assert sample_query.url is not None
    assert sample_query.status == Status.queued

def test_query_with_website():
    query = Query("Machine Learning", website="example.com")
    assert query.website == "example.com"
    assert query.url is not None

def test_google_link_former():
    former = GoogelLinkFormer()
    url = former.get_url("Machine Learning", "example.com")
    assert url.startswith("https://www.google.com/search?q=")
    assert "Machine+Learning" in url
    assert "site:example.com" in url

def test_query_form_url():
    query = Query("Machine Learning")
    assert query.url.startswith("https://www.google.com/search?q=")
    assert "Machine+Learning" in query.url

def test_query_form_url_with_website():
    query = Query("Machine Learning", website="example.com")
    assert query.url.startswith("https://www.google.com/search?q=")
    assert "Machine+Learning" in query.url
    assert "site:example.com" in query.url

def test_query_form_url_invalid_search_engine():
    with pytest.raises(ValueError):
        Query("Machine Learning", search_engine="invalid")

def test_query_form_url_invalid_website():
    query = Query("Machine Learning", website="invalid website")
    assert query.url.startswith("https://www.google.com/search?q=")
    assert "Machine+Learning" in query.url
