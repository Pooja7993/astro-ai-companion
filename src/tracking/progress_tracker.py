"""
Simple Progress Tracking System for Astro AI Companion
Personal Family Use - Track Family Harmony, Health, and Growth
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from src.database.database import db_manager
from src.database.models import User
from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class SimpleProgressTracker:
    """Simple progress tracking for family harmony and personal growth."""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def track_daily_mood(self, user_id: int, mood_score: int, notes: str = "") -> bool:
        """Track daily mood and energy level."""
        try:
            # Store mood data
            mood_data = {
                "user_id": user_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "mood_score": mood_score,  # 1-10 scale
                "notes": notes,
                "timestamp": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.save_mood_tracking(mood_data)
            
            if success:
                logger.info(f"Mood tracking saved for user {user_id}")
                return True
            else:
                logger.error(f"Failed to save mood tracking for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error tracking daily mood: {e}")
            return False
    
    def track_family_harmony(self, user_id: int, harmony_score: int, activity: str = "") -> bool:
        """Track family harmony improvements."""
        try:
            # Store harmony data
            harmony_data = {
                "user_id": user_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "harmony_score": harmony_score,  # 1-10 scale
                "activity": activity,
                "timestamp": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.save_harmony_tracking(harmony_data)
            
            if success:
                logger.info(f"Family harmony tracking saved for user {user_id}")
                return True
            else:
                logger.error(f"Failed to save harmony tracking for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error tracking family harmony: {e}")
            return False
    
    def track_health_progress(self, user_id: int, health_score: int, activity: str = "") -> bool:
        """Track health and wellness progress."""
        try:
            # Store health data
            health_data = {
                "user_id": user_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "health_score": health_score,  # 1-10 scale
                "activity": activity,
                "timestamp": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.save_health_tracking(health_data)
            
            if success:
                logger.info(f"Health progress tracking saved for user {user_id}")
                return True
            else:
                logger.error(f"Failed to save health tracking for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error tracking health progress: {e}")
            return False
    
    def track_spiritual_growth(self, user_id: int, spiritual_score: int, practice: str = "") -> bool:
        """Track spiritual growth and practices."""
        try:
            # Store spiritual data
            spiritual_data = {
                "user_id": user_id,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "spiritual_score": spiritual_score,  # 1-10 scale
                "practice": practice,
                "timestamp": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.save_spiritual_tracking(spiritual_data)
            
            if success:
                logger.info(f"Spiritual growth tracking saved for user {user_id}")
                return True
            else:
                logger.error(f"Failed to save spiritual tracking for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error tracking spiritual growth: {e}")
            return False
    
    def get_weekly_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """Get weekly progress summary."""
        try:
            # Get last 7 days of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            # Get mood data
            mood_data = self.db_manager.get_mood_tracking(user_id, start_date, end_date)
            
            # Get harmony data
            harmony_data = self.db_manager.get_harmony_tracking(user_id, start_date, end_date)
            
            # Get health data
            health_data = self.db_manager.get_health_tracking(user_id, start_date, end_date)
            
            # Get spiritual data
            spiritual_data = self.db_manager.get_spiritual_tracking(user_id, start_date, end_date)
            
            # Calculate averages
            avg_mood = self._calculate_average(mood_data, 'mood_score')
            avg_harmony = self._calculate_average(harmony_data, 'harmony_score')
            avg_health = self._calculate_average(health_data, 'health_score')
            avg_spiritual = self._calculate_average(spiritual_data, 'spiritual_score')
            
            # Get trends
            mood_trend = self._get_trend(mood_data, 'mood_score')
            harmony_trend = self._get_trend(harmony_data, 'harmony_score')
            health_trend = self._get_trend(health_data, 'health_score')
            spiritual_trend = self._get_trend(spiritual_data, 'spiritual_score')
            
            summary = {
                "period": "Last 7 days",
                "mood": {
                    "average": avg_mood,
                    "trend": mood_trend,
                    "total_entries": len(mood_data)
                },
                "harmony": {
                    "average": avg_harmony,
                    "trend": harmony_trend,
                    "total_entries": len(harmony_data)
                },
                "health": {
                    "average": avg_health,
                    "trend": health_trend,
                    "total_entries": len(health_data)
                },
                "spiritual": {
                    "average": avg_spiritual,
                    "trend": spiritual_trend,
                    "total_entries": len(spiritual_data)
                },
                "overall_score": (avg_mood + avg_harmony + avg_health + avg_spiritual) / 4
            }
            
            logger.info(f"Weekly progress summary generated for user {user_id}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating weekly progress summary: {e}")
            return {
                "period": "Last 7 days",
                "error": "Could not generate progress summary"
            }
    
    def get_monthly_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """Get monthly progress summary."""
        try:
            # Get last 30 days of data
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # Get all tracking data
            mood_data = self.db_manager.get_mood_tracking(user_id, start_date, end_date)
            harmony_data = self.db_manager.get_harmony_tracking(user_id, start_date, end_date)
            health_data = self.db_manager.get_health_tracking(user_id, start_date, end_date)
            spiritual_data = self.db_manager.get_spiritual_tracking(user_id, start_date, end_date)
            
            # Calculate averages
            avg_mood = self._calculate_average(mood_data, 'mood_score')
            avg_harmony = self._calculate_average(harmony_data, 'harmony_score')
            avg_health = self._calculate_average(health_data, 'health_score')
            avg_spiritual = self._calculate_average(spiritual_data, 'spiritual_score')
            
            # Get trends
            mood_trend = self._get_trend(mood_data, 'mood_score')
            harmony_trend = self._get_trend(harmony_data, 'harmony_score')
            health_trend = self._get_trend(health_data, 'health_score')
            spiritual_trend = self._get_trend(spiritual_data, 'spiritual_score')
            
            # Get achievements
            achievements = self._get_achievements(avg_mood, avg_harmony, avg_health, avg_spiritual)
            
            summary = {
                "period": "Last 30 days",
                "mood": {
                    "average": avg_mood,
                    "trend": mood_trend,
                    "total_entries": len(mood_data)
                },
                "harmony": {
                    "average": avg_harmony,
                    "trend": harmony_trend,
                    "total_entries": len(harmony_data)
                },
                "health": {
                    "average": avg_health,
                    "trend": health_trend,
                    "total_entries": len(health_data)
                },
                "spiritual": {
                    "average": avg_spiritual,
                    "trend": spiritual_trend,
                    "total_entries": len(spiritual_data)
                },
                "overall_score": (avg_mood + avg_harmony + avg_health + avg_spiritual) / 4,
                "achievements": achievements
            }
            
            logger.info(f"Monthly progress summary generated for user {user_id}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating monthly progress summary: {e}")
            return {
                "period": "Last 30 days",
                "error": "Could not generate progress summary"
            }
    
    def _calculate_average(self, data: List[Dict], field: str) -> float:
        """Calculate average for a field in data."""
        if not data:
            return 0.0
        
        total = sum(item.get(field, 0) for item in data)
        return round(total / len(data), 1)
    
    def _get_trend(self, data: List[Dict], field: str) -> str:
        """Get trend for a field in data."""
        if len(data) < 2:
            return "Stable"
        
        # Sort by date
        sorted_data = sorted(data, key=lambda x: x.get('date', ''))
        
        # Get first and last values
        first_value = sorted_data[0].get(field, 0)
        last_value = sorted_data[-1].get(field, 0)
        
        if last_value > first_value:
            return "Improving"
        elif last_value < first_value:
            return "Declining"
        else:
            return "Stable"
    
    def _get_achievements(self, mood: float, harmony: float, health: float, spiritual: float) -> List[str]:
        """Get achievements based on scores."""
        achievements = []
        
        if mood >= 8.0:
            achievements.append("Excellent mood management")
        
        if harmony >= 8.0:
            achievements.append("Outstanding family harmony")
        
        if health >= 8.0:
            achievements.append("Great health and wellness")
        
        if spiritual >= 8.0:
            achievements.append("Strong spiritual growth")
        
        if (mood + harmony + health + spiritual) / 4 >= 8.0:
            achievements.append("Overall excellent progress")
        
        if not achievements:
            achievements.append("Good progress - keep going!")
        
        return achievements
    
    def format_progress_summary_message(self, summary: Dict[str, Any], user: User) -> str:
        """Format progress summary into a message."""
        try:
            if "error" in summary:
                return f"❌ {summary['error']}"
            
            message = f"""📊 **Progress Summary for {user.name}**

**📅 {summary['period']}**

**😊 Mood: {summary['mood']['average']}/10** ({summary['mood']['trend']})
**👨‍👩‍👧‍👦 Family Harmony: {summary['harmony']['average']}/10** ({summary['harmony']['trend']})
**🏥 Health: {summary['health']['average']}/10** ({summary['health']['trend']})
**🙏 Spiritual: {summary['spiritual']['average']}/10** ({summary['spiritual']['trend']})

**🌟 Overall Score: {summary['overall_score']}/10**

**🏆 Achievements:**
{chr(10).join([f"• {achievement}" for achievement in summary.get('achievements', [])])}

**📈 Total Entries:**
• Mood: {summary['mood']['total_entries']} days
• Harmony: {summary['harmony']['total_entries']} days
• Health: {summary['health']['total_entries']} days
• Spiritual: {summary['spiritual']['total_entries']} days

Keep up the great work! ✨"""
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting progress summary: {e}")
            return "Error generating progress summary"


# Global progress tracker instance
progress_tracker = SimpleProgressTracker() 