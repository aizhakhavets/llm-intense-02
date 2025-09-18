import sqlite3
import json
import logging
from datetime import datetime, timezone
from config import MAX_CONTEXT_MESSAGES

DB_NAME = "user_data.db"

def get_db_connection():
    """Returns a new database connection."""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    try:
        with get_db_connection() as conn:
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
            # Add interaction_count column if it doesn't exist for backward compatibility
            try:
                cursor.execute("ALTER TABLE user_profiles ADD COLUMN interaction_count INTEGER DEFAULT 0")
            except sqlite3.OperationalError:
                pass # column already exists
            
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
            logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database initialization failed: {e}")

def get_user_profile(user_id: int, conn=None) -> dict | None:
    """Retrieves a user's profile from the database."""
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute("SELECT user_id, journey_stage, preferences, interaction_count FROM user_profiles WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            if user:
                preferences = json.loads(user[2]) if user[2] else {}
                return {"user_id": user[0], "journey_stage": user[1], "preferences": preferences, "interaction_count": user[3]}
            return None
    except sqlite3.Error as e:
        logging.error(f"Failed to get user profile for {user_id}: {e}")
        return None

def create_user_profile(user_id: int, conn=None):
    """Creates a new user profile if one doesn't already exist."""
    if get_user_profile(user_id, conn=conn):
        logging.info(f"User profile for {user_id} already exists.")
        return

    now = datetime.now(timezone.utc).isoformat()
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute(
                "INSERT INTO user_profiles (user_id, preferences, created_at, updated_at, interaction_count) VALUES (?, ?, ?, ?, 0)",
                (user_id, json.dumps({}), now, now)
            )
    except sqlite3.Error as e:
        logging.error(f"Failed to create user profile for {user_id}: {e}")

def _get_or_create_user_profile(user_id: int, conn=None) -> dict | None:
    """Internal helper to get a user profile, creating one if it doesn't exist."""
    profile = get_user_profile(user_id, conn=conn)
    if not profile:
        create_user_profile(user_id, conn=conn)
        profile = get_user_profile(user_id, conn=conn)
    return profile

def update_user_preferences(user_id: int, preferences: dict, conn=None):
    """Updates a user's preferences."""
    profile = _get_or_create_user_profile(user_id, conn=conn)
    if not profile:
        logging.error(f"Could not get or create profile for user {user_id} to update preferences.")
        return

    existing_preferences = profile.get('preferences', {})
    existing_preferences.update(preferences)
    new_preferences_json = json.dumps(existing_preferences)
    now = datetime.now(timezone.utc).isoformat()
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute(
                "UPDATE user_profiles SET preferences = ?, updated_at = ? WHERE user_id = ?",
                (new_preferences_json, now, user_id)
            )
    except sqlite3.Error as e:
        logging.error(f"Failed to update preferences for user {user_id}: {e}")

def update_journey_stage(user_id: int, journey_stage: str, conn=None):
    """Updates a user's journey stage."""
    profile = _get_or_create_user_profile(user_id, conn=conn)
    if not profile:
        logging.error(f"Could not get or create profile for user {user_id} to update journey stage.")
        return

    now = datetime.now(timezone.utc).isoformat()
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute(
                "UPDATE user_profiles SET journey_stage = ?, updated_at = ? WHERE user_id = ?",
                (journey_stage, now, user_id)
            )
    except sqlite3.Error as e:
        logging.error(f"Failed to update journey stage for user {user_id}: {e}")

def increment_interaction_count(user_id: int, conn=None):
    """Increments the interaction count for a user."""
    profile = _get_or_create_user_profile(user_id, conn=conn)
    if not profile:
        logging.error(f"Could not get or create profile for user {user_id} to increment interaction count.")
        return

    new_count = profile.get('interaction_count', 0) + 1
    now = datetime.now(timezone.utc).isoformat()
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute(
                "UPDATE user_profiles SET interaction_count = ?, updated_at = ? WHERE user_id = ?",
                (new_count, now, user_id)
            )
    except sqlite3.Error as e:
        logging.error(f"Failed to increment interaction count for user {user_id}: {e}")

def reset_interaction_count(user_id: int, conn=None):
    """Resets the interaction count for a user."""
    profile = _get_or_create_user_profile(user_id, conn=conn)
    if not profile:
        logging.error(f"Could not get or create profile for user {user_id} to reset interaction count.")
        return

    now = datetime.now(timezone.utc).isoformat()
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute(
                "UPDATE user_profiles SET interaction_count = 0, updated_at = ? WHERE user_id = ?",
                (now, user_id)
            )
    except sqlite3.Error as e:
        logging.error(f"Failed to reset interaction count for user {user_id}: {e}")

def delete_user_profile(user_id: int, conn=None):
    """Deletes a user's profile from the database."""
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
    except sqlite3.Error as e:
        logging.error(f"Failed to delete user profile for {user_id}: {e}")

# --- Conversation History Functions ---

def add_message_to_history(user_id: int, role: str, content: str, conn=None):
    """Adds a message to the conversation history."""
    now = datetime.now(timezone.utc).isoformat()
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute(
                "INSERT INTO conversation_history (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (user_id, role, content, now)
            )
    except sqlite3.Error as e:
        logging.error(f"Failed to add message to history for user {user_id}: {e}")

def get_conversation_history(user_id: int, limit: int, conn=None) -> list[dict]:
    """Retrieves the last N messages for a user, maintaining order."""
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            # Fetch the last `limit` messages in ascending order of their timestamp
            cursor.execute("""
                SELECT role, content FROM (
                    SELECT role, content, timestamp 
                    FROM conversation_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ) ORDER BY timestamp ASC
            """, (user_id, limit))
            
            history = cursor.fetchall()
            return [{"role": role, "content": content} for role, content in history]
            
    except sqlite3.Error as e:
        logging.error(f"Failed to get conversation history for user {user_id}: {e}")
        return []

def delete_conversation_history(user_id: int, conn=None):
    """Deletes the entire conversation history for a user."""
    db_conn = conn or get_db_connection()
    try:
        with db_conn as conn_context:
            cursor = conn_context.cursor()
            cursor.execute("DELETE FROM conversation_history WHERE user_id = ?", (user_id,))
            logging.info(f"Deleted conversation history for user {user_id}.")
    except sqlite3.Error as e:
        logging.error(f"Failed to delete conversation history for user {user_id}: {e}")
