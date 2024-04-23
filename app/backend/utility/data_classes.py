from datetime import datetime


class Topic:
    """
    Represents a topic for a general ML concept.

    Attributes:
        topic_id (int or None): The unique identifier for the topic if available, None if not yet assigned.
        topic_name (str): The name of the topic.
        topic_summary (str): A generated summary of the topic.
    """

    def __init__(self, topic_name, topic_summary="", topic_id=None) -> None:
        """
        Initializes a Topic object with the provided attributes.

        Args:
            topic_name (str): The name of the topic.
            topic_summary (str, optional): A generated summary of the topic. Defaults to an empty string.
            topic_id (int or None, optional): The unique identifier for the topic. Defaults to None.
        """
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.topic_summary = topic_summary

    def get_db_command(self):
        """
        Generates a SQL command to insert or update the topic data in the database.

        Returns:
            str: SQL command for inserting or updating the topic data.
        """
        update_time = int(datetime.now().timestamp())
        if self.topic_id is None:
            sql = f"INSERT INTO topics (topic_name, topic_summary, last_update_time)\
                VALUES ('{self.topic_name}', '{self.topic_summary}', {update_time})\
                ON CONFLICT (topic_name) DO UPDATE\
                SET topic_summary = EXCLUDED.topic_summary,\
                    last_update_time = EXCLUDED.last_update_time;\
            "
        else:
            sql = f"UPDATE topics\
                SET topic_name = '{self.topic_name}',\
                    topic_summary = '{self.topic_summary}', \
                    last_update_time = {update_time}\
                WHERE topic_id = {self.topic_id}\
                ON CONFLICT (topic_name) DO UPDATE\
                SET topic_summary = EXCLUDED.topic_summary,\
                    last_update_time = EXCLUDED.last_update_time;\
            "
        return sql


class Source:
    """
    Represents a source related to a topic.

    Attributes:
        topic_id (int): The unique identifier for the associated topic.
        source_id (int or None): The unique identifier for the source if available, None if not yet assigned.
        source_name (str): The name of the source.
        source_description (str): Description of the source.
        source_type (str): Type of the source (website, article(if pdf)).
        source_url (str): The URL of the source.
    """

    def __init__(self, topic_id, source_url, source_name, source_type="website", source_description="", source_id=None) -> None:
        """
        Initializes a Source object with the provided attributes.

        Args:
            topic_id (int): The unique identifier for the associated topic.
            source_url (str): The URL of the source.
            source_name (str): The name of the source.
            source_type (str, optional): Type of the source. Defaults to "website".
            source_description (str, optional): Description of the source. Defaults to an empty string.
            source_id (int or None, optional): The unique identifier for the source. Defaults to None.
        """
        self.topic_id = topic_id
        self.source_id = source_id

        self.source_name = source_name
        self.source_description = source_description
        self.source_type = source_type
        self.source_url = source_url

    def get_db_command(self):
        """
        Generates a SQL command to insert or update the source data in the database.

        Returns:
            str: SQL command for inserting or updating the source data.
        """
        update_time = int(datetime.now().timestamp())
        if self.source_id is None:
            sql = f"INSERT INTO sources (topic_id, source_name, source_description, source_type, source_url, last_update_time)\
                VALUES ({self.topic_id}, '{self.source_name}', '{self.source_description}', '{self.source_type}', '{self.source_url}', {update_time})\
                ON CONFLICT (source_name) DO UPDATE\
                SET topic_id = EXCLUDED.topic_id,\
                    source_description = EXCLUDED.source_description,\
                    source_type = EXCLUDED.source_type,\
                    source_url = EXCLUDED.source_url,\
                    last_update_time = EXCLUDED.last_update_time;\
            "
        else:
            sql = f"UPDATE sources\
                SET topic_id = {self.topic_id},\
                    source_name = '{self.source_name}',\
                    source_description = '{self.source_description}',\
                    source_type = '{self.source_type}',\
                    source_url = '{self.source_url}',\
                    last_update_time = {update_time}\
                WHERE source_id = {self.source_id}\
                ON CONFLICT (source_name) DO UPDATE\
                SET topic_id = EXCLUDED.topic_id,\
                    source_description = EXCLUDED.source_description,\
                    source_type = EXCLUDED.source_type,\
                    source_url = EXCLUDED.source_url,\
                    last_update_time = EXCLUDED.last_update_time;\
            "
        return sql
