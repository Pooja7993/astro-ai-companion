"""
Database Management for Astro AI Companion
Personal Family Use - SQLite/PostgreSQL Database
"""

import os
import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import re

from loguru import logger

from src.database.models import User, FamilyMember
from src.utils.config_simple import get_config

# Check if we're on Render (production environment)
IS_ON_RENDER = os.environ.get('RENDER') == 'true'

# Try to import psycopg2 for PostgreSQL support
try:
    import psycopg2
    from psycopg2.extras import DictCursor
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    if IS_ON_RENDER:
        logger.warning("PostgreSQL support not available but running on Render. Install psycopg2-binary.")


class DatabaseManager:
    """Database manager for Astro AI Companion.
    Supports both SQLite (local development) and PostgreSQL (Render deployment).
    """
    
    def __init__(self):
        self.config = get_config()
        self.db_type = "postgres" if IS_ON_RENDER and POSTGRES_AVAILABLE else "sqlite"
        
        if self.db_type == "sqlite":
            self.db_path = Path("data/astro_companion.db")
            self.db_path.parent.mkdir(exist_ok=True)
            self.conn = None
        else:
            # PostgreSQL connection (for Render)
            self.db_url = os.environ.get('DATABASE_URL')
            if not self.db_url:
                logger.error("DATABASE_URL environment variable not set but running in PostgreSQL mode")
                raise ValueError("DATABASE_URL environment variable must be set when running on Render")
            self.conn = None
        
        self._init_database()
    
    def _get_connection(self):
        """Get a database connection based on the current database type."""
        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.db_path)
            # Enable foreign keys for SQLite
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        else:
            # Return PostgreSQL connection
            if not self.conn or self.conn.closed:
                self.conn = psycopg2.connect(self.db_url)
                self.conn.autocommit = False
            return self.conn
    
    def _init_database(self):
        """Initialize database with tables."""
        try:
            conn = self._get_connection()
            if self.db_type == "sqlite":
                cursor = conn.cursor()
            else:
                cursor = conn.cursor()
                
                # Create users table with database-specific SQL
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            telegram_id TEXT UNIQUE NOT NULL,
                            name TEXT NOT NULL,
                            birth_date TEXT NOT NULL,
                            birth_time TEXT NOT NULL,
                            birth_place TEXT NOT NULL,
                            language TEXT DEFAULT 'en',
                            daily_reports_enabled BOOLEAN DEFAULT 1,
                            realtime_guidance_enabled BOOLEAN DEFAULT 1,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            telegram_id TEXT UNIQUE NOT NULL,
                            name TEXT NOT NULL,
                            birth_date TEXT NOT NULL,
                            birth_time TEXT NOT NULL,
                            birth_place TEXT NOT NULL,
                            language TEXT DEFAULT 'en',
                            daily_reports_enabled BOOLEAN DEFAULT TRUE,
                            realtime_guidance_enabled BOOLEAN DEFAULT TRUE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                
                # Create family_members table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS family_members (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            relationship TEXT NOT NULL,
                            birth_date TEXT,
                            birth_time TEXT,
                            birth_place TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS family_members (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            name TEXT NOT NULL,
                            relationship TEXT NOT NULL,
                            birth_date TEXT,
                            birth_time TEXT,
                            birth_place TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create predictions table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS predictions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            prediction_type TEXT NOT NULL,
                            prediction_text TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS predictions (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            prediction_type TEXT NOT NULL,
                            prediction_text TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create user_preferences table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_preferences (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            preference_key TEXT NOT NULL,
                            preference_value TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            UNIQUE(user_id, preference_key)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_preferences (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            preference_key TEXT NOT NULL,
                            preference_value TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            UNIQUE(user_id, preference_key)
                        )
                    """)
                
                # Create mood_tracking table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS mood_tracking (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            mood_score INTEGER NOT NULL,
                            notes TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS mood_tracking (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            mood_score INTEGER NOT NULL,
                            notes TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create harmony_tracking table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS harmony_tracking (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            harmony_score INTEGER NOT NULL,
                            activity TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS harmony_tracking (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            harmony_score INTEGER NOT NULL,
                            activity TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create health_tracking table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS health_tracking (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            health_score INTEGER NOT NULL,
                            symptoms TEXT,
                            remedies TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS health_tracking (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            health_score INTEGER NOT NULL,
                            symptoms TEXT,
                            remedies TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create spiritual_tracking table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS spiritual_tracking (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            spiritual_score INTEGER NOT NULL,
                            practice TEXT,
                            insights TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS spiritual_tracking (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            date TEXT NOT NULL,
                            spiritual_score INTEGER NOT NULL,
                            practice TEXT,
                            insights TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create user_feedback table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_feedback (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            command TEXT NOT NULL,
                            feedback_score INTEGER NOT NULL,
                            feedback_text TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_feedback (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            command TEXT NOT NULL,
                            feedback_score INTEGER NOT NULL,
                            feedback_text TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create user_interactions table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_interactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            message TEXT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_interactions (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            message TEXT NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                # Create family_goals table
                if self.db_type == "sqlite":
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS family_goals (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            goal_type TEXT NOT NULL,
                            goal_description TEXT NOT NULL,
                            target_date TEXT,
                            status TEXT DEFAULT 'active',
                            progress INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            completed_at TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                else:
                    # PostgreSQL version
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS family_goals (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            goal_type TEXT NOT NULL,
                            goal_description TEXT NOT NULL,
                            target_date TEXT,
                            status TEXT DEFAULT 'active',
                            progress INTEGER DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            completed_at TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def create_user(self, user: User) -> bool:
        """Create a new user in the database."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    INSERT INTO users (telegram_id, name, birth_date, birth_time, birth_place, language)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user.telegram_id, user.name, user.birth_date, user.birth_time, user.birth_place, user.language))
            else:
                cursor.execute("""
                    INSERT INTO users (telegram_id, name, birth_date, birth_time, birth_place, language)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user.telegram_id, user.name, user.birth_date, user.birth_time, user.birth_place, user.language))
            
            conn.commit()
            logger.info(f"User {user.name} created successfully")
            return True
        except (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation) if POSTGRES_AVAILABLE else sqlite3.IntegrityError:
            logger.warning(f"User {user.telegram_id} already exists")
            return False
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, telegram_id: str) -> Optional[User]:
        """Get user by telegram ID."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    SELECT telegram_id, name, birth_date, birth_time, birth_place, language,
                           daily_reports_enabled, realtime_guidance_enabled
                    FROM users WHERE telegram_id = ?
                """, (telegram_id,))
            else:
                cursor.execute("""
                    SELECT telegram_id, name, birth_date, birth_time, birth_place, language,
                           daily_reports_enabled, realtime_guidance_enabled
                    FROM users WHERE telegram_id = %s
                """, (telegram_id,))
            
            row = cursor.fetchone()
            if row:
                return User(
                    telegram_id=row[0],
                    name=row[1],
                    birth_date=row[2],
                    birth_time=row[3],
                    birth_place=row[4],
                    language_preference=row[5],
                    daily_reports_enabled=bool(row[6]),
                    realtime_guidance_enabled=bool(row[7])
                )
            return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def update_user(self, user: User) -> bool:
        """Update user information."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    UPDATE users SET name = ?, birth_date = ?, birth_time = ?, birth_place = ?,
                                   language = ?, daily_reports_enabled = ?, realtime_guidance_enabled = ?,
                                   updated_at = CURRENT_TIMESTAMP
                    WHERE telegram_id = ?
                """, (user.name, user.birth_date, user.birth_time, user.birth_place,
                      user.language, user.daily_reports_enabled, user.realtime_guidance_enabled,
                      user.telegram_id))
            else:
                cursor.execute("""
                    UPDATE users SET name = %s, birth_date = %s, birth_time = %s, birth_place = %s,
                                   language = %s, daily_reports_enabled = %s, realtime_guidance_enabled = %s,
                                   updated_at = CURRENT_TIMESTAMP
                    WHERE telegram_id = %s
                """, (user.name, user.birth_date, user.birth_time, user.birth_place,
                      user.language, user.daily_reports_enabled, user.realtime_guidance_enabled,
                      user.telegram_id))
                
            conn.commit()
            logger.info(f"User {user.name} updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def add_family_member(self, user_id: int, family_member: FamilyMember) -> bool:
        """Add a family member to a user."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    INSERT INTO family_members (user_id, name, relationship, birth_date, birth_time, birth_place)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, family_member.name, family_member.relationship,
                      family_member.birth_date, family_member.birth_time, family_member.birth_place))
            else:
                cursor.execute("""
                    INSERT INTO family_members (user_id, name, relationship, birth_date, birth_time, birth_place)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, family_member.name, family_member.relationship,
                      family_member.birth_date, family_member.birth_time, family_member.birth_place))
                
            conn.commit()
            logger.info(f"Family member {family_member.name} added successfully")
            return True
        except Exception as e:
            logger.error(f"Error adding family member: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def get_family_members(self, user_id: int) -> List[FamilyMember]:
        """Get all family members for a user."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    SELECT name, relationship, birth_date, birth_time, birth_place
                    FROM family_members WHERE user_id = ?
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT name, relationship, birth_date, birth_time, birth_place
                    FROM family_members WHERE user_id = %s
                """, (user_id,))
                
            family_members = []
            for row in cursor.fetchall():
                family_members.append(FamilyMember(
                    name=row[0],
                    relationship=row[1],
                    birth_date=row[2],
                    birth_time=row[3],
                    birth_place=row[4]
                ))
            return family_members
        except Exception as e:
            logger.error(f"Error getting family members: {e}")
            return []
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def save_prediction(self, user_id: int, prediction_type: str, prediction_text: str) -> bool:
        """Save a prediction for a user."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    INSERT INTO predictions (user_id, prediction_type, prediction_text)
                    VALUES (?, ?, ?)
                """, (user_id, prediction_type, prediction_text))
            else:
                cursor.execute("""
                    INSERT INTO predictions (user_id, prediction_type, prediction_text)
                    VALUES (%s, %s, %s)
                """, (user_id, prediction_type, prediction_text))
                
            conn.commit()
            logger.info(f"Prediction saved for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving prediction: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def get_user_preferences(self, user_id: int) -> Dict[str, str]:
        """Get all preferences for a user."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    SELECT preference_key, preference_value
                    FROM user_preferences
                    WHERE user_id = ?
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT preference_key, preference_value
                    FROM user_preferences
                    WHERE user_id = %s
                """, (user_id,))
                
            preferences = {}
            for row in cursor.fetchall():
                preferences[row[0]] = row[1]
            
            return preferences
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {}
        finally:
            if conn:
                conn.close()
    
    def set_user_preference(self, user_id: int, key: str, value: str) -> bool:
        """Set a user preference."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    INSERT OR REPLACE INTO user_preferences (user_id, preference_key, preference_value)
                    VALUES (?, ?, ?)
                """, (user_id, key, value))
            else:
                # PostgreSQL uses ON CONFLICT for upsert
                cursor.execute("""
                    INSERT INTO user_preferences (user_id, preference_key, preference_value)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, preference_key) 
                    DO UPDATE SET preference_value = EXCLUDED.preference_value
                """, (user_id, key, value))
                
            conn.commit()
            logger.info(f"Preference {key} set for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error setting user preference: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    # Progress Tracking Methods
    def save_mood_tracking(self, mood_data: Dict[str, Any]) -> bool:
        """Save mood tracking data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO mood_tracking (user_id, date, mood_score, notes, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (mood_data['user_id'], mood_data['date'], mood_data['mood_score'],
                      mood_data['notes'], mood_data['timestamp']))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving mood tracking: {e}")
            return False
    
    def get_mood_tracking(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get mood tracking data for a period."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, mood_score, notes, timestamp
                    FROM mood_tracking WHERE user_id = ? AND date BETWEEN ? AND ?
                """, (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                return [{'date': row[0], 'mood_score': row[1], 'notes': row[2], 'timestamp': row[3]}
                        for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting mood tracking: {e}")
            return []
    
    def save_harmony_tracking(self, harmony_data: Dict[str, Any]) -> bool:
        """Save harmony tracking data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO harmony_tracking (user_id, date, harmony_score, activity, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (harmony_data['user_id'], harmony_data['date'], harmony_data['harmony_score'],
                      harmony_data['activity'], harmony_data['timestamp']))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving harmony tracking: {e}")
            return False
    
    def get_harmony_tracking(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get harmony tracking data for a period."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, harmony_score, activity, timestamp
                    FROM harmony_tracking WHERE user_id = ? AND date BETWEEN ? AND ?
                """, (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                return [{'date': row[0], 'harmony_score': row[1], 'activity': row[2], 'timestamp': row[3]}
                        for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting harmony tracking: {e}")
            return []
    
    def save_health_tracking(self, health_data: Dict[str, Any]) -> bool:
        """Save health tracking data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO health_tracking (user_id, date, health_score, activity, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (health_data['user_id'], health_data['date'], health_data['health_score'],
                      health_data['activity'], health_data['timestamp']))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving health tracking: {e}")
            return False
    
    def get_health_tracking(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get health tracking data for a period."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, health_score, activity, timestamp
                    FROM health_tracking WHERE user_id = ? AND date BETWEEN ? AND ?
                """, (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                return [{'date': row[0], 'health_score': row[1], 'activity': row[2], 'timestamp': row[3]}
                        for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting health tracking: {e}")
            return []
    
    def save_spiritual_tracking(self, spiritual_data: Dict[str, Any]) -> bool:
        """Save spiritual tracking data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO spiritual_tracking (user_id, date, spiritual_score, practice, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (spiritual_data['user_id'], spiritual_data['date'], spiritual_data['spiritual_score'],
                      spiritual_data['practice'], spiritual_data['timestamp']))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving spiritual tracking: {e}")
            return False
    
    def get_spiritual_tracking(self, user_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get spiritual tracking data for a period."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT date, spiritual_score, practice, timestamp
                    FROM spiritual_tracking WHERE user_id = ? AND date BETWEEN ? AND ?
                """, (user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
                
                return [{'date': row[0], 'spiritual_score': row[1], 'practice': row[2], 'timestamp': row[3]}
                        for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting spiritual tracking: {e}")
            return []
    
    # User Feedback Methods
    def save_user_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Save user feedback."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_feedback (user_id, command, feedback_score, feedback_text, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (feedback_data['user_id'], feedback_data['command'], feedback_data['feedback_score'],
                      feedback_data['feedback_text'], feedback_data['timestamp']))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving user feedback: {e}")
            return False
    
    def get_user_feedback(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get user feedback for a period."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT command, feedback_score, feedback_text, timestamp
                    FROM user_feedback WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
                """.format(days), (user_id,))
                
                return [{'command': row[0], 'feedback_score': row[1], 'feedback_text': row[2], 'timestamp': row[3]}
                        for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting user feedback: {e}")
            return []
    
    def get_user_interactions(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get user interaction patterns."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT message, timestamp
                    FROM user_interactions WHERE user_id = ? AND timestamp >= datetime('now', '-{} days')
                """.format(days), (user_id,))
                
                return [{'message': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting user interactions: {e}")
            return []
    
    # Goal Tracking Methods
    def save_family_goal(self, goal_data: Dict[str, Any]) -> bool:
        """Save a family goal."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    INSERT INTO family_goals (user_id, goal_type, goal_description, target_date, status, progress, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (goal_data['user_id'], goal_data['goal_type'], goal_data['goal_description'],
                      goal_data['target_date'], goal_data['status'], goal_data['progress'], goal_data['created_at']))
            else:
                cursor.execute("""
                    INSERT INTO family_goals (user_id, goal_type, goal_description, target_date, status, progress, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (goal_data['user_id'], goal_data['goal_type'], goal_data['goal_description'],
                      goal_data['target_date'], goal_data['status'], goal_data['progress'], goal_data['created_at']))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error saving family goal: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def get_active_goals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get active goals for a user."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    SELECT id, goal_type, goal_description, target_date, status, progress, created_at
                    FROM family_goals WHERE user_id = ? AND status = 'active'
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT id, goal_type, goal_description, target_date, status, progress, created_at
                    FROM family_goals WHERE user_id = %s AND status = 'active'
                """, (user_id,))
            
            return [{'id': row[0], 'goal_type': row[1], 'goal_description': row[2], 'target_date': row[3],
                    'status': row[4], 'progress': row[5], 'created_at': row[6]} for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting active goals: {e}")
            return []
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def get_all_goals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all goals for a user."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    SELECT id, goal_type, goal_description, target_date, status, progress, created_at, completed_at
                    FROM family_goals WHERE user_id = ?
                """, (user_id,))
            else:
                cursor.execute("""
                    SELECT id, goal_type, goal_description, target_date, status, progress, created_at, completed_at
                    FROM family_goals WHERE user_id = %s
                """, (user_id,))
            
            return [{'id': row[0], 'goal_type': row[1], 'goal_description': row[2], 'target_date': row[3],
                    'status': row[4], 'progress': row[5], 'created_at': row[6], 'completed_at': row[7]}
                    for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting all goals: {e}")
            return []
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def get_goal_by_id(self, goal_id: int) -> Optional[Dict[str, Any]]:
        """Get a goal by ID."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    SELECT id, user_id, goal_type, goal_description, target_date, status, progress, created_at
                    FROM family_goals WHERE id = ?
                """, (goal_id,))
            else:
                cursor.execute("""
                    SELECT id, user_id, goal_type, goal_description, target_date, status, progress, created_at
                    FROM family_goals WHERE id = %s
                """, (goal_id,))
            
            row = cursor.fetchone()
            if row:
                return {'id': row[0], 'user_id': row[1], 'goal_type': row[2], 'goal_description': row[3],
                        'target_date': row[4], 'status': row[5], 'progress': row[6], 'created_at': row[7]}
            return None
        except Exception as e:
            logger.error(f"Error getting goal by ID: {e}")
            return None
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def update_goal_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Update goal progress."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    UPDATE family_goals SET progress = ? WHERE id = ?
                """, (progress_data['progress'], progress_data['goal_id']))
            else:
                cursor.execute("""
                    UPDATE family_goals SET progress = %s WHERE id = %s
                """, (progress_data['progress'], progress_data['goal_id']))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating goal progress: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()
    
    def complete_goal(self, goal_id: int) -> bool:
        """Mark a goal as completed."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            current_time = datetime.now()
            
            if self.db_type == "sqlite":
                cursor.execute("""
                    UPDATE family_goals SET status = 'completed', completed_at = ? WHERE id = ?
                """, (current_time, goal_id))
            else:
                cursor.execute("""
                    UPDATE family_goals SET status = 'completed', completed_at = %s WHERE id = %s
                """, (current_time, goal_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error completing goal: {e}")
            return False
        finally:
            if self.db_type == "sqlite" and conn:
                conn.close()


# Global database manager instance
db_manager = DatabaseManager()