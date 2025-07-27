"""
Advanced Personalization System for Astro AI Companion
Personal Family Use - Learn from Preferences and Adapt
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from src.database.database import db_manager
from src.database.models import User
from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class AdaptivePersonalizationSystem:
    """Advanced personalization system that learns from user preferences."""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def learn_from_user_feedback(self, user_id: int, command: str, feedback_score: int, 
                                feedback_text: str = "") -> bool:
        """Learn from user feedback on commands and recommendations."""
        try:
            # Store feedback data
            feedback_data = {
                "user_id": user_id,
                "command": command,
                "feedback_score": feedback_score,  # 1-10 scale
                "feedback_text": feedback_text,
                "timestamp": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.save_user_feedback(feedback_data)
            
            if success:
                logger.info(f"User feedback saved for command {command}")
                return True
            else:
                logger.error(f"Failed to save user feedback for command {command}")
                return False
                
        except Exception as e:
            logger.error(f"Error learning from user feedback: {e}")
            return False
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences based on learning."""
        try:
            # Get user's feedback history
            feedback_history = self.db_manager.get_user_feedback(user_id, days=30)
            
            # Analyze preferences
            preferences = self._analyze_preferences(feedback_history)
            
            # Get user's interaction patterns
            interaction_patterns = self.db_manager.get_user_interactions(user_id, days=30)
            
            # Analyze patterns
            patterns = self._analyze_interaction_patterns(interaction_patterns)
            
            # Combine preferences and patterns
            user_preferences = {
                "preferred_commands": preferences.get("preferred_commands", []),
                "preferred_topics": preferences.get("preferred_topics", []),
                "best_timing": patterns.get("best_timing", "Morning"),
                "communication_style": patterns.get("communication_style", "Direct"),
                "detail_level": patterns.get("detail_level", "Moderate"),
                "language_preference": patterns.get("language_preference", "English"),
                "focus_areas": preferences.get("focus_areas", ["Family", "Health"]),
                "avoided_topics": preferences.get("avoided_topics", [])
            }
            
            logger.info(f"User preferences generated for user {user_id}")
            return user_preferences
            
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {
                "preferred_commands": ["daily", "family_recommendations"],
                "preferred_topics": ["Family", "Health"],
                "best_timing": "Morning",
                "communication_style": "Direct",
                "detail_level": "Moderate",
                "language_preference": "English",
                "focus_areas": ["Family", "Health"],
                "avoided_topics": []
            }
    
    def adapt_recommendations(self, user_id: int, base_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt recommendations based on user preferences."""
        try:
            # Get user preferences
            preferences = self.get_user_preferences(user_id)
            
            # Adapt recommendations based on preferences
            adapted_recommendations = self._adapt_to_preferences(base_recommendations, preferences)
            
            logger.info(f"Recommendations adapted for user {user_id}")
            return adapted_recommendations
            
        except Exception as e:
            logger.error(f"Error adapting recommendations: {e}")
            return base_recommendations
    
    def get_personalized_timing(self, user_id: int) -> Dict[str, Any]:
        """Get personalized timing recommendations."""
        try:
            # Get user's interaction patterns
            patterns = self.db_manager.get_user_interactions(user_id, days=30)
            
            # Analyze timing patterns
            timing_analysis = self._analyze_timing_patterns(patterns)
            
            # Get cosmic timing
            cosmic_timing = self._get_cosmic_timing()
            
            # Combine personal and cosmic timing
            personalized_timing = {
                "best_morning_time": timing_analysis.get("best_morning", "6:00 AM"),
                "best_evening_time": timing_analysis.get("best_evening", "6:00 PM"),
                "avoid_times": timing_analysis.get("avoid_times", ["12:00 PM", "6:00 PM"]),
                "cosmic_auspicious": cosmic_timing.get("auspicious", "Morning 6-8"),
                "cosmic_challenging": cosmic_timing.get("challenging", "Afternoon 12-2"),
                "recommended_activities": timing_analysis.get("recommended_activities", [])
            }
            
            logger.info(f"Personalized timing generated for user {user_id}")
            return personalized_timing
            
        except Exception as e:
            logger.error(f"Error getting personalized timing: {e}")
            return {
                "best_morning_time": "6:00 AM",
                "best_evening_time": "6:00 PM",
                "avoid_times": ["12:00 PM", "6:00 PM"],
                "cosmic_auspicious": "Morning 6-8",
                "cosmic_challenging": "Afternoon 12-2",
                "recommended_activities": ["Meditation", "Family time"]
            }
    
    def get_custom_family_rituals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get custom family rituals based on preferences."""
        try:
            # Get user preferences
            preferences = self.get_user_preferences(user_id)
            
            # Get family members
            family_members = self.db_manager.get_family_members(user_id)
            
            # Generate custom rituals
            custom_rituals = self._generate_custom_rituals(preferences, family_members)
            
            logger.info(f"Custom family rituals generated for user {user_id}")
            return custom_rituals
            
        except Exception as e:
            logger.error(f"Error getting custom family rituals: {e}")
            return [
                {
                    "name": "Morning Family Prayer",
                    "description": "Light a diya and pray together",
                    "timing": "Morning 6-8 AM",
                    "duration": "10 minutes",
                    "benefits": ["Family harmony", "Peace", "Unity"]
                }
            ]
    
    def _analyze_preferences(self, feedback_history: List[Dict]) -> Dict[str, Any]:
        """Analyze user preferences from feedback history."""
        try:
            if not feedback_history:
                return {}
            
            # Analyze command preferences
            command_scores = {}
            topic_scores = {}
            focus_areas = set()
            avoided_topics = set()
            
            for feedback in feedback_history:
                command = feedback.get("command", "")
                score = feedback.get("feedback_score", 5)
                text = feedback.get("feedback_text", "").lower()
                
                # Track command preferences
                if command not in command_scores:
                    command_scores[command] = []
                command_scores[command].append(score)
                
                # Analyze topics from feedback text
                topics = self._extract_topics_from_text(text)
                for topic in topics:
                    if topic not in topic_scores:
                        topic_scores[topic] = []
                    topic_scores[topic].append(score)
                
                # Track focus areas and avoided topics
                if score >= 7:
                    focus_areas.update(topics)
                elif score <= 3:
                    avoided_topics.update(topics)
            
            # Calculate average scores
            preferred_commands = []
            for command, scores in command_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score >= 7:
                    preferred_commands.append(command)
            
            preferred_topics = []
            for topic, scores in topic_scores.items():
                avg_score = sum(scores) / len(scores)
                if avg_score >= 7:
                    preferred_topics.append(topic)
            
            return {
                "preferred_commands": preferred_commands,
                "preferred_topics": preferred_topics,
                "focus_areas": list(focus_areas),
                "avoided_topics": list(avoided_topics)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing preferences: {e}")
            return {}
    
    def _analyze_interaction_patterns(self, interactions: List[Dict]) -> Dict[str, Any]:
        """Analyze user interaction patterns."""
        try:
            if not interactions:
                return {}
            
            # Analyze timing patterns
            morning_interactions = 0
            evening_interactions = 0
            night_interactions = 0
            
            # Analyze communication style
            short_messages = 0
            long_messages = 0
            
            for interaction in interactions:
                timestamp = interaction.get("timestamp", datetime.now())
                hour = timestamp.hour
                message_length = len(interaction.get("message", ""))
                
                # Timing analysis
                if 6 <= hour < 12:
                    morning_interactions += 1
                elif 12 <= hour < 18:
                    evening_interactions += 1
                else:
                    night_interactions += 1
                
                # Communication style analysis
                if message_length < 50:
                    short_messages += 1
                else:
                    long_messages += 1
            
            # Determine best timing
            total_interactions = len(interactions)
            if total_interactions > 0:
                morning_ratio = morning_interactions / total_interactions
                evening_ratio = evening_interactions / total_interactions
                night_ratio = night_interactions / total_interactions
                
                if morning_ratio > 0.5:
                    best_timing = "Morning"
                elif evening_ratio > 0.5:
                    best_timing = "Evening"
                else:
                    best_timing = "Flexible"
            else:
                best_timing = "Morning"
            
            # Determine communication style
            if short_messages > long_messages:
                communication_style = "Direct"
            else:
                communication_style = "Detailed"
            
            # Determine detail level
            if short_messages > long_messages:
                detail_level = "Brief"
            else:
                detail_level = "Detailed"
            
            return {
                "best_timing": best_timing,
                "communication_style": communication_style,
                "detail_level": detail_level,
                "language_preference": "English"  # Default for now
            }
            
        except Exception as e:
            logger.error(f"Error analyzing interaction patterns: {e}")
            return {}
    
    def _adapt_to_preferences(self, base_recommendations: Dict[str, Any], 
                             preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt recommendations to user preferences."""
        try:
            adapted = base_recommendations.copy()
            
            # Adapt detail level
            detail_level = preferences.get("detail_level", "Moderate")
            if detail_level == "Brief":
                # Simplify recommendations
                if "remedy" in adapted:
                    adapted["remedy"] = self._simplify_text(adapted["remedy"])
                if "warnings" in adapted:
                    adapted["warnings"] = [self._simplify_text(w) for w in adapted["warnings"]]
            
            # Adapt communication style
            communication_style = preferences.get("communication_style", "Direct")
            if communication_style == "Direct":
                # Make recommendations more direct
                if "remedy" in adapted:
                    adapted["remedy"] = self._make_direct(adapted["remedy"])
            
            # Focus on preferred topics
            preferred_topics = preferences.get("preferred_topics", [])
            if preferred_topics:
                # Add focus on preferred topics
                adapted["focus_areas"] = preferred_topics[:3]  # Top 3 preferred topics
            
            return adapted
            
        except Exception as e:
            logger.error(f"Error adapting to preferences: {e}")
            return base_recommendations
    
    def _analyze_timing_patterns(self, patterns: List[Dict]) -> Dict[str, Any]:
        """Analyze timing patterns from interactions."""
        try:
            if not patterns:
                return {}
            
            morning_times = []
            evening_times = []
            
            for pattern in patterns:
                timestamp = pattern.get("timestamp", datetime.now())
                hour = timestamp.hour
                
                if 6 <= hour < 12:
                    morning_times.append(hour)
                elif 18 <= hour < 22:
                    evening_times.append(hour)
            
            # Calculate best times
            best_morning = "6:00 AM"
            if morning_times:
                avg_morning = sum(morning_times) / len(morning_times)
                best_morning = f"{int(avg_morning):02d}:00 AM"
            
            best_evening = "6:00 PM"
            if evening_times:
                avg_evening = sum(evening_times) / len(evening_times)
                best_evening = f"{int(avg_evening):02d}:00 PM"
            
            return {
                "best_morning": best_morning,
                "best_evening": best_evening,
                "avoid_times": ["12:00 PM", "6:00 PM"],
                "recommended_activities": ["Meditation", "Family time"]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing timing patterns: {e}")
            return {}
    
    def _get_cosmic_timing(self) -> Dict[str, Any]:
        """Get cosmic timing recommendations."""
        try:
            current_date = datetime.now()
            day_of_week = current_date.strftime("%A")
            
            cosmic_timing = {
                "auspicious": "Morning 6-8",
                "challenging": "Afternoon 12-2"
            }
            
            # Adjust based on day
            if day_of_week in ["Monday", "Thursday"]:
                cosmic_timing["auspicious"] = "Morning 6-8 and Evening 6-8"
            elif day_of_week in ["Tuesday", "Saturday"]:
                cosmic_timing["challenging"] = "Morning 6-10"
            
            return cosmic_timing
            
        except Exception as e:
            logger.error(f"Error getting cosmic timing: {e}")
            return {
                "auspicious": "Morning 6-8",
                "challenging": "Afternoon 12-2"
            }
    
    def _generate_custom_rituals(self, preferences: Dict[str, Any], 
                                family_members: List[Dict]) -> List[Dict[str, Any]]:
        """Generate custom family rituals."""
        try:
            rituals = []
            
            # Morning ritual
            morning_ritual = {
                "name": "Morning Family Prayer",
                "description": "Light a diya and pray together for family harmony",
                "timing": "Morning 6-8 AM",
                "duration": "10 minutes",
                "benefits": ["Family unity", "Peace", "Positive energy"]
            }
            rituals.append(morning_ritual)
            
            # Evening ritual
            evening_ritual = {
                "name": "Evening Gratitude",
                "description": "Share gratitude and appreciation with family",
                "timing": "Evening 6-8 PM",
                "duration": "15 minutes",
                "benefits": ["Family bonding", "Gratitude", "Love"]
            }
            rituals.append(evening_ritual)
            
            # Weekly ritual
            weekly_ritual = {
                "name": "Weekly Family Meal",
                "description": "Share a special meal together",
                "timing": "Sunday Evening",
                "duration": "1 hour",
                "benefits": ["Family bonding", "Communication", "Joy"]
            }
            rituals.append(weekly_ritual)
            
            return rituals
            
        except Exception as e:
            logger.error(f"Error generating custom rituals: {e}")
            return []
    
    def _extract_topics_from_text(self, text: str) -> List[str]:
        """Extract topics from text."""
        topics = []
        
        # Simple topic extraction
        topic_keywords = {
            "family": ["family", "harmony", "bonding", "love"],
            "health": ["health", "wellness", "exercise", "diet"],
            "wealth": ["wealth", "money", "finance", "prosperity"],
            "spiritual": ["spiritual", "meditation", "prayer", "peace"],
            "relationships": ["relationship", "love", "marriage", "partnership"],
            "career": ["career", "work", "job", "business"]
        }
        
        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    topics.append(topic)
                    break
        
        return topics
    
    def _simplify_text(self, text: str) -> str:
        """Simplify text for brief communication."""
        # Simple text simplification
        if len(text) > 100:
            return text[:100] + "..."
        return text
    
    def _make_direct(self, text: str) -> str:
        """Make text more direct."""
        # Simple directness improvement
        if "you should" not in text.lower():
            text = "You should " + text.lower()
        return text


# Global adaptive personalization instance
adaptive_system = AdaptivePersonalizationSystem() 