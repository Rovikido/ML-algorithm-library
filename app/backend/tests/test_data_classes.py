import pytest
from app.backend.utility.data_classes import Topic, Source

@pytest.fixture
def sample_topic():
    return Topic("Machine Learning Basics", "Introduction to ML concepts")

@pytest.fixture
def sample_source(sample_topic):
    return Source(sample_topic.topic_id, "https://example.com/ml-basics", "ML Basics Website")

def test_topic_initialization(sample_topic):
    assert sample_topic.topic_name == "Machine Learning Basics"
    assert sample_topic.topic_summary == "Introduction to ML concepts"
    assert sample_topic.topic_id is None

def test_source_initialization(sample_source):
    assert sample_source.source_name == "ML Basics Website"
    assert sample_source.source_type == "website"
    assert sample_source.source_url == "https://example.com/ml-basics"
    assert sample_source.source_id is None

def test_get_db_command_topic(sample_topic):
    db_command = sample_topic.get_db_command()
    assert "INSERT INTO topics" in db_command
    assert ";" in db_command
    assert "\n" not in db_command
    assert "UPDATE topics" not in db_command

def test_get_db_command_source(sample_source):
    db_command = sample_source.get_db_command()
    assert "INSERT INTO sources" in db_command
    assert ";" in db_command
    assert "\n" not in db_command
    assert "UPDATE sources" not in db_command
