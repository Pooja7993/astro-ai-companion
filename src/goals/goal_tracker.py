"""
Simple Goal Setting & Tracking System for Astro AI Companion
Personal Family Use - Family Goals and Personal Growth
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from src.database.database import db_manager
from src.database.models import User
from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class SimpleGoalTracker:
    """Simple goal setting and tracking system."""
    
    def __init__(self):
        self.db_manager = db_manager
    
    def set_family_goal(self, user_id: int, goal_type: str, goal_description: str, 
                        target_date: str = None) -> bool:
        """Set a family goal."""
        try:
            # Create goal data
            goal_data = {
                "user_id": user_id,
                "goal_type": goal_type,  # family_harmony, health, spiritual, etc.
                "goal_description": goal_description,
                "target_date": target_date,
                "status": "active",
                "progress": 0,
                "created_at": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.save_family_goal(goal_data)
            
            if success:
                logger.info(f"Family goal set for user {user_id}: {goal_description}")
                return True
            else:
                logger.error(f"Failed to set family goal for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error setting family goal: {e}")
            return False
    
    def update_goal_progress(self, user_id: int, goal_id: int, progress: int, 
                           notes: str = "") -> bool:
        """Update goal progress."""
        try:
            # Update progress data
            progress_data = {
                "goal_id": goal_id,
                "progress": progress,  # 0-100
                "notes": notes,
                "updated_at": datetime.now()
            }
            
            # Save to database
            success = self.db_manager.update_goal_progress(progress_data)
            
            if success:
                logger.info(f"Goal progress updated for user {user_id}: {progress}%")
                return True
            else:
                logger.error(f"Failed to update goal progress for user {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error updating goal progress: {e}")
            return False
    
    def get_active_goals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get active goals for user."""
        try:
            # Get active goals from database
            goals = self.db_manager.get_active_goals(user_id)
            
            logger.info(f"Retrieved {len(goals)} active goals for user {user_id}")
            return goals
            
        except Exception as e:
            logger.error(f"Error getting active goals: {e}")
            return []
    
    def get_goal_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """Get goal progress summary."""
        try:
            # Get all goals and their progress
            goals = self.db_manager.get_all_goals(user_id)
            
            if not goals:
                return {
                    "total_goals": 0,
                    "completed_goals": 0,
                    "active_goals": 0,
                    "average_progress": 0,
                    "recent_achievements": []
                }
            
            # Calculate summary
            total_goals = len(goals)
            completed_goals = len([g for g in goals if g.get("status") == "completed"])
            active_goals = len([g for g in goals if g.get("status") == "active"])
            
            # Calculate average progress
            progress_values = [g.get("progress", 0) for g in goals if g.get("status") == "active"]
            average_progress = sum(progress_values) / len(progress_values) if progress_values else 0
            
            # Get recent achievements
            recent_achievements = self._get_recent_achievements(goals)
            
            summary = {
                "total_goals": total_goals,
                "completed_goals": completed_goals,
                "active_goals": active_goals,
                "average_progress": round(average_progress, 1),
                "recent_achievements": recent_achievements
            }
            
            logger.info(f"Goal progress summary generated for user {user_id}")
            return summary
            
        except Exception as e:
            logger.error(f"Error getting goal progress summary: {e}")
            return {
                "total_goals": 0,
                "completed_goals": 0,
                "active_goals": 0,
                "average_progress": 0,
                "recent_achievements": []
            }
    
    def celebrate_goal_achievement(self, user_id: int, goal_id: int) -> Dict[str, Any]:
        """Celebrate goal achievement."""
        try:
            # Get goal details
            goal = self.db_manager.get_goal_by_id(goal_id)
            
            if not goal:
                return {"error": "Goal not found"}
            
            # Create celebration message
            celebration = self._create_celebration_message(goal)
            
            # Mark goal as completed
            self.db_manager.complete_goal(goal_id)
            
            logger.info(f"Goal achievement celebrated for user {user_id}")
            return celebration
            
        except Exception as e:
            logger.error(f"Error celebrating goal achievement: {e}")
            return {"error": "Could not celebrate achievement"}
    
    def get_suggested_goals(self, user_id: int) -> List[Dict[str, Any]]:
        """Get suggested goals based on user profile."""
        try:
            # Get user profile
            user = self.db_manager.get_user_by_id(user_id)
            
            if not user:
                return []
            
            # Generate suggested goals based on user profile
            suggested_goals = self._generate_suggested_goals(user)
            
            logger.info(f"Generated {len(suggested_goals)} suggested goals for user {user_id}")
            return suggested_goals
            
        except Exception as e:
            logger.error(f"Error getting suggested goals: {e}")
            return []
    
    def _get_recent_achievements(self, goals: List[Dict]) -> List[Dict[str, Any]]:
        """Get recent achievements from goals."""
        try:
            achievements = []
            
            # Get completed goals from last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            for goal in goals:
                if (goal.get("status") == "completed" and 
                    goal.get("completed_at") and 
                    goal.get("completed_at") > thirty_days_ago):
                    
                    achievement = {
                        "goal_description": goal.get("goal_description", ""),
                        "completed_at": goal.get("completed_at"),
                        "goal_type": goal.get("goal_type", "")
                    }
                    achievements.append(achievement)
            
            # Sort by completion date (most recent first)
            achievements.sort(key=lambda x: x.get("completed_at", datetime.now()), reverse=True)
            
            return achievements[:5]  # Return top 5 recent achievements
            
        except Exception as e:
            logger.error(f"Error getting recent achievements: {e}")
            return []
    
    def _create_celebration_message(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """Create celebration message for goal achievement."""
        try:
            goal_type = goal.get("goal_type", "")
            goal_description = goal.get("goal_description", "")
            
            # Create celebration based on goal type
            celebrations = {
                "family_harmony": {
                    "title": "🎉 Family Harmony Goal Achieved!",
                    "message": f"Congratulations! You've successfully achieved: {goal_description}",
                    "celebration": "Your family is stronger and more united!",
                    "next_step": "Set a new family harmony goal to continue building bonds"
                },
                "health": {
                    "title": "🏥 Health Goal Achieved!",
                    "message": f"Amazing! You've successfully achieved: {goal_description}",
                    "celebration": "Your health and wellness are improving!",
                    "next_step": "Set a new health goal to maintain your progress"
                },
                "spiritual": {
                    "title": "🙏 Spiritual Growth Goal Achieved!",
                    "message": f"Wonderful! You've successfully achieved: {goal_description}",
                    "celebration": "Your spiritual journey is flourishing!",
                    "next_step": "Set a new spiritual goal to deepen your practice"
                },
                "wealth": {
                    "title": "💰 Wealth Goal Achieved!",
                    "message": f"Excellent! You've successfully achieved: {goal_description}",
                    "celebration": "Your financial prosperity is growing!",
                    "next_step": "Set a new wealth goal to continue building abundance"
                },
                "happiness": {
                    "title": "😊 Happiness Goal Achieved!",
                    "message": f"Fantastic! You've successfully achieved: {goal_description}",
                    "celebration": "Your joy and contentment are increasing!",
                    "next_step": "Set a new happiness goal to spread more joy"
                }
            }
            
            celebration = celebrations.get(goal_type, {
                "title": "🎉 Goal Achieved!",
                "message": f"Congratulations! You've successfully achieved: {goal_description}",
                "celebration": "You're making great progress!",
                "next_step": "Set a new goal to continue your journey"
            })
            
            return celebration
            
        except Exception as e:
            logger.error(f"Error creating celebration message: {e}")
            return {
                "title": "🎉 Goal Achieved!",
                "message": "Congratulations on achieving your goal!",
                "celebration": "You're making great progress!",
                "next_step": "Set a new goal to continue your journey"
            }
    
    def _generate_suggested_goals(self, user: User) -> List[Dict[str, Any]]:
        """Generate suggested goals based on user profile."""
        try:
            suggested_goals = []
            
            # Family harmony goals
            family_goals = [
                {
                    "goal_type": "family_harmony",
                    "goal_description": "Spend 30 minutes daily quality time with family",
                    "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                },
                {
                    "goal_type": "family_harmony",
                    "goal_description": "Have one family meal together every day",
                    "target_date": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d")
                },
                {
                    "goal_type": "family_harmony",
                    "goal_description": "Express gratitude to each family member daily",
                    "target_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                }
            ]
            
            # Health goals
            health_goals = [
                {
                    "goal_type": "health",
                    "goal_description": "Exercise for 30 minutes daily",
                    "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                },
                {
                    "goal_type": "health",
                    "goal_description": "Drink 8 glasses of water daily",
                    "target_date": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d")
                },
                {
                    "goal_type": "health",
                    "goal_description": "Practice meditation for 10 minutes daily",
                    "target_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                }
            ]
            
            # Spiritual goals
            spiritual_goals = [
                {
                    "goal_type": "spiritual",
                    "goal_description": "Pray or meditate for 15 minutes daily",
                    "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                },
                {
                    "goal_type": "spiritual",
                    "goal_description": "Read spiritual texts for 20 minutes daily",
                    "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                },
                {
                    "goal_type": "spiritual",
                    "goal_description": "Practice gratitude journaling daily",
                    "target_date": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d")
                }
            ]
            
            # Add goals based on user preferences
            suggested_goals.extend(family_goals[:2])  # Top 2 family goals
            suggested_goals.extend(health_goals[:2])  # Top 2 health goals
            suggested_goals.extend(spiritual_goals[:2])  # Top 2 spiritual goals
            
            return suggested_goals
            
        except Exception as e:
            logger.error(f"Error generating suggested goals: {e}")
            return []
    
    def format_goal_summary_message(self, summary: Dict[str, Any], user: User) -> str:
        """Format goal summary into a message."""
        try:
            message = f"""🎯 **Goal Progress Summary for {user.name}**

**📊 Overview:**
• Total Goals: {summary['total_goals']}
• Completed Goals: {summary['completed_goals']}
• Active Goals: {summary['active_goals']}
• Average Progress: {summary['average_progress']}%

**🏆 Recent Achievements:**
{chr(10).join([f"• {achievement['goal_description']}" for achievement in summary['recent_achievements'][:3]]) if summary['recent_achievements'] else "• No recent achievements yet"}

**💪 Keep Going:**
You're making great progress! Continue working towards your goals for family harmony and personal growth.

Set new goals with `/set_goal` to keep improving! ✨"""
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting goal summary: {e}")
            return "Error generating goal summary"


# Global goal tracker instance
goal_tracker = SimpleGoalTracker() 