"""
Family Management for Astro AI Companion
Personal Family Use - Family Member Management
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.database.database import db_manager
from src.database.models import User, FamilyMember
from src.astrology.chart_analyzer import ChartAnalyzer
from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class FamilyManager:
    """Family management system for Astro AI Companion."""
    
    def __init__(self):
        self.chart_analyzer = ChartAnalyzer()
    
    def add_family_member(self, user_id: int, name: str, relationship: str, 
                         birth_date: str = None, birth_time: str = None, 
                         birth_place: str = None) -> bool:
        """Add a family member to a user's family."""
        try:
            family_member = FamilyMember(
                name=name,
                relationship=relationship,
                birth_date=birth_date,
                birth_time=birth_time,
                birth_place=birth_place
            )
            
            success = db_manager.add_family_member(user_id, family_member)
            if success:
                logger.info(f"Family member {name} added successfully for user {user_id}")
            return success
            
        except Exception as e:
            logger.error(f"Error adding family member: {e}")
            return False
    
    def get_family_members(self, user_id: int) -> List[FamilyMember]:
        """Get all family members for a user."""
        try:
            family_members = db_manager.get_family_members(user_id)
            logger.info(f"Retrieved {len(family_members)} family members for user {user_id}")
            return family_members
        except Exception as e:
            logger.error(f"Error getting family members: {e}")
            return []
    
    def get_family_compatibility(self, user: User, family_members: List[FamilyMember]) -> Dict[str, Any]:
        """Get family compatibility analysis."""
        try:
            compatibility_analysis = {
                "user_name": user.name,
                "family_members": [],
                "overall_harmony": "Strong",
                "recommendations": []
            }
            
            for member in family_members:
                member_analysis = {
                    "name": member.name,
                    "relationship": member.relationship,
                    "compatibility": self._analyze_relationship_compatibility(user, member),
                    "strengths": self._get_relationship_strengths(user, member),
                    "challenges": self._get_relationship_challenges(user, member),
                    "recommendations": self._get_relationship_recommendations(user, member)
                }
                compatibility_analysis["family_members"].append(member_analysis)
            
            # Overall family harmony
            compatibility_analysis["overall_harmony"] = self._calculate_family_harmony(compatibility_analysis)
            compatibility_analysis["recommendations"] = self._get_family_recommendations(compatibility_analysis)
            
            logger.info(f"Family compatibility analysis completed for user {user.name}")
            return compatibility_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing family compatibility: {e}")
            return {"error": "Could not analyze family compatibility"}
    
    def _analyze_relationship_compatibility(self, user: User, member: FamilyMember) -> str:
        """Analyze compatibility between user and family member."""
        # Simple compatibility analysis based on relationship type
        relationship_compatibility = {
            "spouse": "High compatibility - Strong emotional bond",
            "parent": "Very high compatibility - Natural authority and care",
            "child": "Very high compatibility - Natural nurturing bond",
            "sibling": "High compatibility - Shared background and experiences",
            "grandparent": "High compatibility - Wisdom and guidance",
            "cousin": "Moderate compatibility - Extended family connection",
            "friend": "Moderate compatibility - Chosen relationship"
        }
        
        return relationship_compatibility.get(member.relationship.lower(), "Good compatibility")
    
    def _get_relationship_strengths(self, user: User, member: FamilyMember) -> List[str]:
        """Get strengths of the relationship."""
        strengths = []
        
        if member.relationship.lower() in ["spouse", "partner"]:
            strengths.extend([
                "Strong emotional connection",
                "Shared life goals",
                "Mutual support and understanding",
                "Deep love and commitment"
            ])
        elif member.relationship.lower() in ["parent", "child"]:
            strengths.extend([
                "Natural nurturing bond",
                "Unconditional love",
                "Life guidance and wisdom",
                "Strong family foundation"
            ])
        elif member.relationship.lower() == "sibling":
            strengths.extend([
                "Shared childhood experiences",
                "Lifelong friendship",
                "Mutual understanding",
                "Family loyalty"
            ])
        else:
            strengths.extend([
                "Family connection",
                "Mutual care and support",
                "Shared values",
                "Emotional bond"
            ])
        
        return strengths
    
    def _get_relationship_challenges(self, user: User, member: FamilyMember) -> List[str]:
        """Get potential challenges in the relationship."""
        challenges = []
        
        if member.relationship.lower() in ["spouse", "partner"]:
            challenges.extend([
                "Communication differences",
                "Life balance",
                "Personal space needs",
                "Decision-making conflicts"
            ])
        elif member.relationship.lower() in ["parent", "child"]:
            challenges.extend([
                "Generation gap",
                "Different life perspectives",
                "Independence vs guidance",
                "Expectation differences"
            ])
        elif member.relationship.lower() == "sibling":
            challenges.extend([
                "Competition and comparison",
                "Different life paths",
                "Family dynamics",
                "Personal boundaries"
            ])
        else:
            challenges.extend([
                "Communication gaps",
                "Different perspectives",
                "Life stage differences",
                "Personal boundaries"
            ])
        
        return challenges
    
    def _get_relationship_recommendations(self, user: User, member: FamilyMember) -> List[str]:
        """Get recommendations for improving the relationship."""
        recommendations = []
        
        if member.relationship.lower() in ["spouse", "partner"]:
            recommendations.extend([
                "Practice active listening and empathy",
                "Schedule regular quality time together",
                "Communicate openly about feelings and needs",
                "Support each other's personal growth",
                "Create shared goals and dreams"
            ])
        elif member.relationship.lower() in ["parent", "child"]:
            recommendations.extend([
                "Show appreciation and gratitude",
                "Spend quality time together",
                "Listen to each other's perspectives",
                "Respect boundaries and independence",
                "Share family traditions and values"
            ])
        elif member.relationship.lower() == "sibling":
            recommendations.extend([
                "Maintain regular communication",
                "Support each other's goals",
                "Respect individual differences",
                "Create shared memories",
                "Be there for each other"
            ])
        else:
            recommendations.extend([
                "Regular family gatherings",
                "Open and honest communication",
                "Mutual respect and understanding",
                "Support each other's growth",
                "Create meaningful connections"
            ])
        
        return recommendations
    
    def _calculate_family_harmony(self, compatibility_analysis: Dict[str, Any]) -> str:
        """Calculate overall family harmony level."""
        member_count = len(compatibility_analysis["family_members"])
        
        if member_count == 0:
            return "Individual"
        elif member_count <= 2:
            return "Strong"
        elif member_count <= 4:
            return "Good"
        else:
            return "Moderate"
    
    def _get_family_recommendations(self, compatibility_analysis: Dict[str, Any]) -> List[str]:
        """Get overall family recommendations."""
        recommendations = [
            "Schedule regular family time and activities",
            "Practice open and honest communication",
            "Show appreciation and gratitude to each other",
            "Support individual growth and goals",
            "Create and maintain family traditions",
            "Respect personal boundaries and space",
            "Celebrate each other's successes",
            "Be there for each other during challenges"
        ]
        
        return recommendations
    
    def get_family_guidance(self, user: User, family_members: List[FamilyMember]) -> str:
        """Get personalized family guidance."""
        try:
            compatibility = self.get_family_compatibility(user, family_members)
            
            guidance = f"""👨‍👩‍👧‍👦 **Family Guidance for {user.name}**

**🌟 Family Harmony Level: {compatibility['overall_harmony']}**

**💝 Family Members:**
"""
            
            for member in compatibility["family_members"]:
                guidance += f"""• **{member['name']}** ({member['relationship']})
  - Compatibility: {member['compatibility']}
  - Strengths: {', '.join(member['strengths'][:2])}
  - Focus: {member['challenges'][0] if member['challenges'] else 'Maintain harmony'}

"""
            
            guidance += f"""**🎯 Family Recommendations:**
"""
            for rec in compatibility["recommendations"][:5]:
                guidance += f"• {rec}\n"
            
            guidance += f"""

**💎 Family Remedies:**
• Light a diya for family harmony
• Practice daily family prayer
• Share meals together regularly
• Create family traditions and rituals

Your family bonds are strong and supportive! Focus on open communication and quality time together. ✨"""
            
            return guidance
            
        except Exception as e:
            logger.error(f"Error generating family guidance: {e}")
            return "❌ Error generating family guidance. Please try again."


# Global family manager instance
family_manager = FamilyManager() 