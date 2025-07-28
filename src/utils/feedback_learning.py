"""
Adaptive AI-Driven Recommendations System
Collects user feedback and uses it to personalize future recommendations
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger

class FeedbackLearningSystem:
    """Adaptive recommendation system based on user feedback."""
    
    def __init__(self):
        self.feedback_categories = {
            'daily': 'Daily predictions',
            'health': 'Health guidance',
            'family': 'Family advice',
            'career': 'Career guidance',
            'spiritual': 'Spiritual growth',
            'relationships': 'Relationship advice',
            'general': 'General guidance'
        }
    
    def collect_feedback(self, user_id: str, prediction_type: str, 
                        feedback_score: int, feedback_text: str = "") -> bool:
        """Collect and store user feedback."""
        try:
            from src.database.database import DatabaseManager
            db = DatabaseManager()
            
            feedback_data = {
                'user_id': user_id,
                'prediction_type': prediction_type,
                'feedback_score': feedback_score,  # 1-5 scale
                'feedback_text': feedback_text,
                'timestamp': datetime.now(),
                'category': self._categorize_prediction(prediction_type)
            }
            
            # Store feedback in database
            success = db.save_user_feedback(feedback_data)
            
            if success:
                logger.info(f"Feedback collected for user {user_id}: {prediction_type} - Score: {feedback_score}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error collecting feedback: {e}")
            return False
    
    def _categorize_prediction(self, prediction_type: str) -> str:
        """Categorize prediction type for feedback analysis."""
        prediction_lower = prediction_type.lower()
        
        if any(word in prediction_lower for word in ['health', 'wellness', 'fitness']):
            return 'health'
        elif any(word in prediction_lower for word in ['family', 'home', 'children']):
            return 'family'
        elif any(word in prediction_lower for word in ['career', 'work', 'job', 'business']):
            return 'career'
        elif any(word in prediction_lower for word in ['spiritual', 'meditation', 'prayer']):
            return 'spiritual'
        elif any(word in prediction_lower for word in ['relationship', 'love', 'marriage']):
            return 'relationships'
        elif any(word in prediction_lower for word in ['daily', 'today', 'prediction']):
            return 'daily'
        else:
            return 'general'
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences based on feedback history."""
        try:
            from src.database.database import DatabaseManager
            db = DatabaseManager()
            
            # Get recent feedback (last 30 days)
            recent_feedback = db.get_user_feedback(user_id, days=30)
            
            if not recent_feedback:
                return self._get_default_preferences()
            
            # Analyze feedback patterns
            preferences = self._analyze_feedback_patterns(recent_feedback)
            
            return preferences
            
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return self._get_default_preferences()
    
    def _analyze_feedback_patterns(self, feedback_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze feedback patterns to determine user preferences."""
        preferences = {
            'favorite_categories': [],
            'avoid_categories': [],
            'preferred_style': 'balanced',  # detailed, concise, spiritual, practical
            'feedback_score': 0,
            'total_feedback': len(feedback_list)
        }
        
        if not feedback_list:
            return preferences
        
        # Calculate average feedback score
        total_score = sum(f.get('feedback_score', 3) for f in feedback_list)
        preferences['feedback_score'] = total_score / len(feedback_list)
        
        # Analyze category preferences
        category_scores = {}
        for feedback in feedback_list:
            category = feedback.get('category', 'general')
            score = feedback.get('feedback_score', 3)
            
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(score)
        
        # Determine favorite and avoid categories
        for category, scores in category_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score >= 4:
                preferences['favorite_categories'].append(category)
            elif avg_score <= 2:
                preferences['avoid_categories'].append(category)
        
        # Determine preferred style based on feedback text
        detailed_count = sum(1 for f in feedback_list if 'detailed' in f.get('feedback_text', '').lower())
        concise_count = sum(1 for f in feedback_list if 'concise' in f.get('feedback_text', '').lower())
        spiritual_count = sum(1 for f in feedback_list if 'spiritual' in f.get('feedback_text', '').lower())
        practical_count = sum(1 for f in feedback_list if 'practical' in f.get('feedback_text', '').lower())
        
        style_counts = {
            'detailed': detailed_count,
            'concise': concise_count,
            'spiritual': spiritual_count,
            'practical': practical_count
        }
        
        if max(style_counts.values()) > 0:
            preferences['preferred_style'] = max(style_counts, key=style_counts.get)
        
        return preferences
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default preferences for new users."""
        return {
            'favorite_categories': ['daily', 'family'],
            'avoid_categories': [],
            'preferred_style': 'balanced',
            'feedback_score': 3,
            'total_feedback': 0
        }
    
    def generate_adaptive_recommendation(self, user_id: str, prediction_type: str, 
                                       user_name: str) -> str:
        """Generate personalized recommendation based on user feedback."""
        try:
            preferences = self.get_user_preferences(user_id)
            
            # Base recommendation
            base_recommendation = self._get_base_recommendation(prediction_type, user_name)
            
            # Adapt based on preferences
            adapted_recommendation = self._adapt_recommendation(
                base_recommendation, preferences, prediction_type
            )
            
            return adapted_recommendation
            
        except Exception as e:
            logger.error(f"Error generating adaptive recommendation: {e}")
            return self._get_base_recommendation(prediction_type, user_name)
    
    def _get_base_recommendation(self, prediction_type: str, user_name: str) -> str:
        """Get base recommendation for prediction type."""
        if prediction_type == 'daily':
            return f"""📅 **Daily Guidance for {user_name}**

**Today's Focus:**
• Personal growth and spiritual development
• Family harmony and emotional well-being
• Health and wellness practices
• Career and life purpose alignment

**🌟 Cosmic Energy:** Trust your intuition and follow your heart's calling! ✨"""
        
        elif prediction_type == 'health':
            return f"""🏥 **Health Guidance for {user_name}**

**Wellness Focus:**
• Physical and mental wellness
• Balanced diet and exercise
• Meditation and stress relief
• Natural healing practices

**🌟 Health Energy:** Nurture your body and mind for optimal well-being! ✨"""
        
        elif prediction_type == 'family':
            return f"""👨‍👩‍👧‍👦 **Family Guidance for {user_name}**

**Family Harmony:**
• Open communication and understanding
• Quality time together
• Emotional support and love
• Shared activities and traditions

**🌟 Family Energy:** Strengthen bonds and create lasting memories! ✨"""
        
        else:
            return f"""🌟 **Personal Guidance for {user_name}**

**Life Focus:**
• Personal growth and development
• Spiritual awakening and wisdom
• Relationship harmony and love
• Career success and purpose

**🌟 Cosmic Blessings:** Embrace your unique journey and potential! ✨"""
    
    def _adapt_recommendation(self, base_recommendation: str, preferences: Dict[str, Any], 
                             prediction_type: str) -> str:
        """Adapt recommendation based on user preferences."""
        adapted = base_recommendation
        
        # Adapt based on preferred style
        if preferences['preferred_style'] == 'detailed':
            adapted += "\n\n**📊 Detailed Analysis:** Based on your feedback, you prefer comprehensive guidance."
        elif preferences['preferred_style'] == 'concise':
            adapted = adapted.replace('\n\n', '\n').replace('**🌟', '🌟')
        elif preferences['preferred_style'] == 'spiritual':
            adapted += "\n\n**🙏 Spiritual Focus:** Your spiritual journey is blessed with divine guidance."
        elif preferences['preferred_style'] == 'practical':
            adapted += "\n\n**🎯 Practical Tips:** Focus on actionable steps for immediate results."
        
        # Adapt based on favorite categories
        if prediction_type in preferences['favorite_categories']:
            adapted += "\n\n**💫 Your Favorite Area:** This guidance aligns with your preferred topics!"
        
        # Add feedback encouragement if low feedback
        if preferences['total_feedback'] < 5:
            adapted += "\n\n**💡 Help Us Improve:** Rate this guidance with 👍 or 👎 to personalize your experience!"
        
        return adapted
    
    def create_feedback_prompt(self, prediction_type: str) -> str:
        """Create a feedback prompt for users."""
        return f"""💬 **How was this {prediction_type} guidance?**

Please rate your experience:
👍 **Helpful** - This guidance was useful
👎 **Not Helpful** - This guidance wasn't relevant

Your feedback helps personalize future recommendations for you and your family! ✨"""

# Global instance
feedback_learning = FeedbackLearningSystem() 