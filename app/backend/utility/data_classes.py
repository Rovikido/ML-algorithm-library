from datetime import datetime


class Topic:
    def __init__(self, topic_name, topic_summary="", topic_id=None) -> None:
        self.topic_id = topic_id
        self.topic_name = topic_name
        self.topic_summary = topic_summary

    def get_db_command(self):
        update_time = int(datetime.now().timestamp())
        if self.topic_id is None:
            sql = f"""
                INSERT INTO topics (topic_name, topic_summary, last_update_time)
                VALUES ('{self.topic_name}', '{self.topic_summary}', {update_time})
                ON CONFLICT (topic_name) DO UPDATE
                SET topic_summary = EXCLUDED.topic_summary,
                    last_update_time = EXCLUDED.last_update_time
            """
        else:
            sql = f"""
                UPDATE topics
                SET topic_name = '{self.topic_name}',
                    topic_summary = '{self.topic_summary}', 
                    last_update_time = {update_time}
                WHERE topic_id = {self.topic_id}
                ON CONFLICT (topic_name) DO UPDATE
                SET topic_summary = EXCLUDED.topic_summary,
                    last_update_time = EXCLUDED.last_update_time
            """
        return sql


class Source:
    def __init__(self, topic_id, source_url, source_name, source_type="website", source_description="", source_id=None) -> None:
        self.topic_id = topic_id
        self.source_id = source_id

        self.source_name = source_name
        self.source_description = source_description
        self.source_type = source_type
        self.source_url = source_url

    def get_db_command(self):
        update_time = int(datetime.now().timestamp())
        if self.source_id is None:
            sql = f"""
                INSERT INTO sources (topic_id, source_name, source_description, source_type, source_url, last_update_time)
                VALUES ({self.topic_id}, '{self.source_name}', '{self.source_description}', '{self.source_type}', '{self.source_url}', {update_time})
                ON CONFLICT (source_name) DO UPDATE
                SET topic_id = EXCLUDED.topic_id,
                    source_description = EXCLUDED.source_description,
                    source_type = EXCLUDED.source_type,
                    source_url = EXCLUDED.source_url,
                    last_update_time = EXCLUDED.last_update_time
            """
        else:
            sql = f"""
                UPDATE sources
                SET topic_id = {self.topic_id},
                    source_name = '{self.source_name}',
                    source_description = '{self.source_description}',
                    source_type = '{self.source_type}',
                    source_url = '{self.source_url}',
                    last_update_time = {update_time}
                WHERE source_id = {self.source_id}
                ON CONFLICT (source_name) DO UPDATE
                SET topic_id = EXCLUDED.topic_id,
                    source_description = EXCLUDED.source_description,
                    source_type = EXCLUDED.source_type,
                    source_url = EXCLUDED.source_url,
                    last_update_time = EXCLUDED.last_update_time
            """
        return sql
