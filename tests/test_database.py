import pytest
import sqlite3
import os
import json
from datetime import datetime, timezone
from unittest.mock import patch

# Mock the DB_NAME to use an in-memory database for all tests
@pytest.fixture(scope="module", autouse=True)
def mock_db_name():
    with patch('database.DB_NAME', ':memory:') as _fixture:
        yield _fixture

# Now import the database module
from database import (
    init_db,
    create_user_profile,
    get_user_profile,
    add_message_to_history,
    get_conversation_history,
    delete_conversation_history,
    delete_user_profile,
)

@pytest.fixture(scope="function")
def test_db_conn():
    """Fixture to set up a single in-memory db connection and initialize tables."""
    conn = sqlite3.connect(':memory:')
    # Manually initialize the schema using this connection
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id INTEGER PRIMARY KEY,
            journey_stage TEXT NOT NULL DEFAULT 'new_user',
            preferences TEXT,
            interaction_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        )
    """)
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def test_user(test_db_conn):
    """Fixture to create a test user."""
    user_id = 12345
    create_user_profile(user_id, conn=test_db_conn)
    return user_id

def test_add_and_get_conversation_history(test_user, test_db_conn):
    """Test adding and retrieving conversation history."""
    user_id = test_user
    
    # Add messages
    add_message_to_history(user_id, "user", "Hello", conn=test_db_conn)
    add_message_to_history(user_id, "assistant", "Hi there!", conn=test_db_conn)
    
    # Retrieve history
    history = get_conversation_history(user_id, 10, conn=test_db_conn)
    
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "Hello"}
    assert history[1] == {"role": "assistant", "content": "Hi there!"}

def test_get_conversation_history_limit(test_user, test_db_conn):
    """Test the limit parameter for retrieving conversation history."""
    user_id = test_user
    
    for i in range(5):
        add_message_to_history(user_id, "user", f"Message {i}", conn=test_db_conn)
        
    history = get_conversation_history(user_id, 3, conn=test_db_conn)
    
    assert len(history) == 3
    assert history[0]['content'] == "Message 2"
    assert history[1]['content'] == "Message 3"
    assert history[2]['content'] == "Message 4"

def test_delete_conversation_history(test_user, test_db_conn):
    """Test deleting conversation history."""
    user_id = test_user
    
    add_message_to_history(user_id, "user", "This will be deleted", conn=test_db_conn)
    history_before = get_conversation_history(user_id, 10, conn=test_db_conn)
    assert len(history_before) == 1
    
    delete_conversation_history(user_id, conn=test_db_conn)
    history_after = get_conversation_history(user_id, 10, conn=test_db_conn)
    
    assert len(history_after) == 0

def test_history_is_user_specific(test_db_conn):
    """Test that conversation history is isolated between users."""
    user_id_1 = 111
    user_id_2 = 222
    create_user_profile(user_id_1, conn=test_db_conn)
    create_user_profile(user_id_2, conn=test_db_conn)
    
    add_message_to_history(user_id_1, "user", "Message for user 1", conn=test_db_conn)
    add_message_to_history(user_id_2, "assistant", "Message for user 2", conn=test_db_conn)
    
    history1 = get_conversation_history(user_id_1, 10, conn=test_db_conn)
    history2 = get_conversation_history(user_id_2, 10, conn=test_db_conn)
    
    assert len(history1) == 1
    assert history1[0]['content'] == "Message for user 1"
    
    assert len(history2) == 1
    assert history2[0]['content'] == "Message for user 2"
