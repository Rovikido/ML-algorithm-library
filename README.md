# Neural Network Library

## Introduction

The Neural Network Library is a Python-based project designed to gather information about neural networks from online sources, sumarize it, and store their sources. 
## Components

1. **GoogleScraper:** Responsible for scraping search results from Google based on a specified query. Utilizes the Google Search API to retrieve relevant links and descriptions.

2. **Query:** Helps in forming structured queries for the GoogleScraper. It takes a topic name, a specific search engine (in this case, "sci-hub.se"), and the type of search engine (here, SearchEngines.google.value).

3. **ChatGPTScraperSummarizerStrategy:** Handles the summarization process using the GPT-based ChatGPT model.

4. **Context:** Provides a context for the summarization strategy. Encapsulates the strategy and facilitates its usage in the summarization process.

5. **DB:** Manages interactions with the database. Includes methods for creating tables, inserting/updating topic and source information, and retrieving topic IDs.

## Usage

1. **Initialization:** Instantiate the DB class to set up the database tables.

    ```python
    db = DB()
    db.create_tables()
    ```

2. **Process Topic:** Use the `process_topic()` function to scrape and summarize information about a specific topic. Pass the topic name as an argument to the function.

    ```python
    process_topic("Deep neural networks")
    ```

3. **Summarization:** The function first forms a query using the Query class, then utilizes the GoogleScraper to fetch relevant search results. Subsequently, it summarizes the collected information using the ChatGPTScraperSummarizerStrategy.

4. **Database Interaction:** The summarized information along with the relevant sources is then stored in the database for future reference.

## Dependencies

- See requerements.txt

