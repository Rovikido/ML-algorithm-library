from app.backend.scraper.google_scraper import GoogleScraper
from app.backend.scraper.query_former import Query
from app.backend.utility.constants import SearchEngines
from app.backend.utility.data_classes import Topic, Source
from app.backend.summarizer.summarizer import ChatGPTScraperSummarizerStrategy, Context
from app.backend.database.db import DB


# db = DB()
# db.create_tables()


def process_topic(topic_name, db):
    query = Query(topic_name, "sci-hub.se", SearchEngines.google.value)
    print(query.url)
    scraper = GoogleScraper()
    res = scraper.scrape_query(query)

    chat_scrapper = ChatGPTScraperSummarizerStrategy()
    context = Context(chat_scrapper)
    summary = context.summarize_topic_from_name(topic_name)
    
    print(summary)
    chat_scrapper.end_connection()

    topic = Topic(topic_name=topic_name, topic_summary=summary)
    db.insert_update_topic(topic)
    topic_id = db.get_topic_id_by_name(topic_name)
    Topic.topic_id = topic_id
    for src in res[:20]:
        source_type = 'artice' if src['link'].endswith(".pdf") else 'website'
        source = Source(topic_id=topic_id, source_url=src['link'], 
                        source_name=src['title'], source_type=source_type, 
                        source_description=src['description'])
        db.insert_update_source(source)

# process_topic("Deep neural networks")
# Query("Machine Learning")