import psycopg2
from configparser import ConfigParser

from app.backend.utility.data_classes import Topic, Source


def handle_database_errors(func):
    """
    Decorator used for every DB method to catch errors and automaticly return None
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            return None
    return wrapper


class DB:
    def __init__(self) -> None:
        self.conn = self.__connect(self.__load_config())
    
    def __load_config(self):
        filename='db.ini'
        section='postgresql'
        parser = ConfigParser()
        parser.read(filename)

        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return config

    @handle_database_errors
    def __connect(self, config):
        """ Connect to the PostgreSQL database server """
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn

    @handle_database_errors
    def create_tables(self):
        commands = [
            "CREATE TABLE IF NOT EXISTS topics(\
                topic_id SERIAL PRIMARY KEY,\
                topic_name VARCHAR(511) NOT NULL UNIQUE,\
                topic_summary VARCHAR(8191),\
                last_update_time INT NOT NULL\
            );\
            ",
            "CREATE TABLE IF NOT EXISTS sources(\
                source_id SERIAL PRIMARY KEY,\
                topic_id INTEGER,\
                source_name VARCHAR(511) NOT NULL UNIQUE,\
                source_description VARCHAR(4091),\
                source_type VARCHAR(255) NOT NULL,\
                source_url VARCHAR(1027) NOT NULL,\
                last_update_time INT,\
                CONSTRAINT fk_topics\
                FOREIGN KEY(topic_id)\
                    REFERENCES topics(topic_id)\
            );"
        ]
        with self.conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
        self.conn.commit()

    @handle_database_errors
    def insert_update_topic(self, topic:Topic):
        command = topic.get_db_command()
        with self.conn.cursor() as cur:
            cur.execute(command)
        self.conn.commit()

    @handle_database_errors
    def insert_update_source(self, source:Source):
        command = source.get_db_command()
        with self.conn.cursor() as cur:
            cur.execute(command)
        self.conn.commit()

    @handle_database_errors
    def get_topic_id_by_name(self, name):
        with self.conn.cursor() as cur:
            cur.execute("SELECT topic_id FROM topics WHERE topic_name = %s;", (name,))
            topic_id = cur.fetchone()
            if topic_id:
                return topic_id[0]
            else:
                return None

    def get_topics(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM topics;")
            topics_data = cur.fetchall()
            topics=[]
            for topic_data in topics_data:
                topic_id, topic_name, topic_summary = topic_data
                topic = Topic(topic_name, topic_summary, topic_id)
                topics.append(topic)
            return topics
        
    @handle_database_errors
    def get_sources_by_topic(self, topic_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM sources WHERE topic_id = %s;", (topic_id,))
            sources_data = cur.fetchall()
            sources = []
            for source_data in sources_data:
                source_id, _, source_name, source_description, source_type, source_url, _ = source_data
                source = Source(topic_id, source_url, source_name, source_type, source_description, source_id)
                sources.append(source)
            return sources
    