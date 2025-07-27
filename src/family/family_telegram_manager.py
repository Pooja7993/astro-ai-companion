"""
Family Telegram Manager for Astro AI Companion
Personal Family Use - Individual Family Member Access
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from telegram import Update, Bot
from telegram.ext import ContextTypes

from src.database.database import db_manager
from src.database.models import User, FamilyMember
from src.family.family_manager import family_manager
from src.astrology.real_astrology_engine import astrology_engine
from src.utils.multi_language import multi_lang
from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class FamilyTelegramManager:
    """Manages individual Telegram access for family members."""
    
    def __init__(self, bot_token: str):
        self.bot = Bot(token=bot_token)
        self.family_manager = family_manager
        self.astrology_engine = astrology_engine
    
    async def add_family_member_with_telegram(self, user_id: int, family_member: FamilyMember, 
                                            telegram_id: str, language: str = "en") -> bool:
        """Add a family member with their own Telegram access."""
        try:
            # Add family member to database
            success = self.family_manager.add_family_member(
                user_id, family_member.name, family_member.relationship,
                family_member.birth_date, family_member.birth_time, family_member.birth_place
            )
            
            if success:
                # Create user profile for family member
                family_user = User(
                    telegram_id=telegram_id,
                    name=family_member.name,
                    birth_date=family_member.birth_date or "1990-01-01",
                    birth_time=family_member.birth_time or "12:00",
                    birth_place=family_member.birth_place or "Mumbai, India",
                    language=language,
                    daily_reports_enabled=True,
                    realtime_guidance_enabled=True
                )
                
                # Save family member user profile
                db_manager.create_user(family_user)
                
                # Send welcome message to family member
                await self._send_welcome_message_to_family_member(telegram_id, family_member, language)
                
                logger.info(f"Family member {family_member.name} added with Telegram access")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error adding family member with Telegram: {e}")
            return False
    
    async def _send_welcome_message_to_family_member(self, telegram_id: str, 
                                                   family_member: FamilyMember, language: str):
        """Send welcome message to new family member."""
        try:
            # Set language for this message
            multi_lang.set_language(language)
            
            welcome_msg = multi_lang.format_message(
                "family_member_welcome",
                name=family_member.name,
                relationship=family_member.relationship
            )
            
            await self.bot.send_message(
                chat_id=telegram_id,
                text=welcome_msg,
                parse_mode='Markdown'
            )
            
            logger.info(f"Welcome message sent to family member {family_member.name}")
            
        except Exception as e:
            logger.error(f"Error sending welcome message to family member: {e}")
    
    async def send_daily_prediction_to_family(self, user_id: int, language: str = "en"):
        """Send daily prediction to all family members."""
        try:
            # Get main user
            main_user = db_manager.get_user_by_id(user_id)
            if not main_user:
                logger.error(f"Main user not found for ID: {user_id}")
                return
            
            # Get family members
            family_members = self.family_manager.get_family_members(user_id)
            
            # Get birth chart for main user
            birth_chart = self.astrology_engine.calculate_birth_chart(
                main_user.birth_date, main_user.birth_time, main_user.birth_place
            )
            
            # Send predictions to each family member
            for member in family_members:
                await self._send_family_daily_prediction(member, birth_chart, language)
            
            logger.info(f"Daily predictions sent to {len(family_members)} family members")
            
        except Exception as e:
            logger.error(f"Error sending daily predictions to family: {e}")
    
    async def _send_family_daily_prediction(self, member: FamilyMember, 
                                          birth_chart: Dict[str, Any], language: str):
        """Send personalized daily prediction to family member."""
        try:
            # Set language
            multi_lang.set_language(language)
            
            # Generate personalized prediction
            prediction = self.astrology_engine.get_personalized_predictions(birth_chart, "daily")
            
            # Create personalized message
            message = self._create_family_daily_message(member, prediction, language)
            
            # Send message (in real implementation, you'd need the family member's telegram_id)
            # For now, we'll just log the message
            logger.info(f"Daily prediction for {member.name}: {message[:100]}...")
            
        except Exception as e:
            logger.error(f"Error sending daily prediction to {member.name}: {e}")
    
    def _create_family_daily_message(self, member: FamilyMember, 
                                   prediction: Dict[str, Any], language: str) -> str:
        """Create personalized daily message for family member."""
        if language == "mr":
            return f"""🌟 **{member.name} साठी आजचे कॉस्मिक मार्गदर्शन**

**📅 आजची ऊर्जा:**
• **सकाळ:** नवीन सुरुवात आणि महत्वाचे निर्णय घेण्यासाठी परिपूर्ण
• **दुपार:** सर्जनशील क्रियाकलाप आणि शिकण्यावर लक्ष केंद्रित करा
• **संध्याकाळ:** कुटुंब वेळ आणि विश्रांती
• **रात्र:** उद्यासाठी चिंतन आणि नियोजन

**💫 आजचे लक्ष केंद्र:**
• **वैयक्तिक विकास:** स्वतःच्या सुधारणेसाठी वेळ
• **कुटुंब सुसंवाद:** कुटुंबातील बंध मजबूत करा
• **आरोग्य:** कल्याण आणि जीवनशक्तीवर लक्ष केंद्रित करा
• **आध्यात्मिक:** उच्च चेतनेशी जोडणी

**🎯 आजची संधी:**
• **सकाळचे ध्यान:** हेतूने दिवस सुरु करा
• **कुटुंब बंध:** प्रियजनांसोबत गुणवत्तापूर्ण वेळ
• **आरोग्य क्रियाकलाप:** व्यायाम आणि निरोगी खाणे
• **आध्यात्मिक सराव:** प्रार्थना आणि ध्यान

**💎 आजचे उपाय:**
• **सकाळ:** सकारात्मक ऊर्जेसाठी दिवा लावा
• **दुपार:** तांब्याच्या भांड्यातून पाणी प्या
• **संध्याकाळ:** कुटुंब प्रार्थना आणि कृतज्ञता
• **रात्र:** दिवसाच्या आशीर्वादांवर चिंतन करा

कॉस्मिक आशीर्वादांनी भरलेला एक चांगला दिवस घ्या! ✨"""
        else:
            return f"""🌟 **Daily Cosmic Guidance for {member.name}**

**📅 Today's Energy:**
• **Morning:** Perfect for new beginnings and important decisions
• **Afternoon:** Focus on creative activities and learning
• **Evening:** Family time and relaxation
• **Night:** Reflection and planning for tomorrow

**💫 Today's Focus:**
• **Personal growth:** Time for self-improvement
• **Family harmony:** Strengthen family bonds
• **Health:** Focus on wellness and vitality
• **Spiritual:** Connect with higher consciousness

**🎯 Today's Opportunities:**
• **Morning meditation:** Start day with intention
• **Family bonding:** Quality time with loved ones
• **Health activities:** Exercise and healthy eating
• **Spiritual practice:** Prayer and meditation

**💎 Today's Remedies:**
• **Morning:** Light a diya for positive energy
• **Afternoon:** Drink water from copper vessel
• **Evening:** Family prayer and gratitude
• **Night:** Reflect on the day's blessings

Have a wonderful day filled with cosmic blessings! ✨"""
    
    async def send_family_guidance_to_member(self, member: FamilyMember, 
                                           language: str = "en") -> str:
        """Send personalized family guidance to specific member."""
        try:
            # Set language
            multi_lang.set_language(language)
            
            # Create mock user for family member
            family_user = User(
                telegram_id="family_member",
                name=member.name,
                birth_date=member.birth_date or "1990-01-01",
                birth_time=member.birth_time or "12:00",
                birth_place=member.birth_place or "Mumbai, India",
                language=language,
                daily_reports_enabled=True,
                realtime_guidance_enabled=True
            )
            
            # Get family guidance
            guidance = self.family_manager.get_family_guidance(family_user, [member])
            
            # Translate if needed
            if language == "mr":
                guidance = self._translate_family_guidance_to_marathi(guidance)
            
            return guidance
            
        except Exception as e:
            logger.error(f"Error sending family guidance to {member.name}: {e}")
            return f"Error generating guidance for {member.name}"
    
    def _translate_family_guidance_to_marathi(self, guidance: str) -> str:
        """Translate family guidance to Marathi."""
        # Simplified translation - in real implementation, use proper translation
        marathi_guidance = guidance.replace("Family", "कुटुंब")
        marathi_guidance = marathi_guidance.replace("guidance", "मार्गदर्शन")
        marathi_guidance = marathi_guidance.replace("harmony", "सुसंवाद")
        marathi_guidance = marathi_guidance.replace("relationships", "नातेसंबंध")
        
        return marathi_guidance
    
    async def send_individual_prediction(self, member: FamilyMember, 
                                       prediction_type: str, language: str = "en") -> str:
        """Send individual prediction to family member."""
        try:
            # Set language
            multi_lang.set_language(language)
            
            # Calculate birth chart for member if birth details available
            if member.birth_date and member.birth_time and member.birth_place:
                birth_chart = self.astrology_engine.calculate_birth_chart(
                    member.birth_date, member.birth_time, member.birth_place
                )
                
                # Get personalized prediction
                prediction = self.astrology_engine.get_personalized_predictions(birth_chart, prediction_type)
                
                # Create personalized message
                message = self._create_individual_prediction_message(member, prediction, prediction_type, language)
                
                return message
            else:
                # Generic prediction if birth details not available
                return self._create_generic_prediction_message(member, prediction_type, language)
                
        except Exception as e:
            logger.error(f"Error sending individual prediction to {member.name}: {e}")
            return f"Error generating prediction for {member.name}"
    
    def _create_individual_prediction_message(self, member: FamilyMember, 
                                           prediction: Dict[str, Any], 
                                           prediction_type: str, language: str) -> str:
        """Create individual prediction message."""
        if language == "mr":
            return f"""🌟 **{member.name} साठी वैयक्तिक {prediction_type} भविष्यवाणी**

**📅 ऊर्जा विश्लेषण:**
• **ऊर्जा पातळी:** {prediction.get('energy_level', 'मध्यम')}
• **लक्ष केंद्रे:** {', '.join(prediction.get('focus_areas', ['वैयक्तिक विकास', 'कुटुंब सुसंवाद']))}
• **आव्हाने:** {', '.join(prediction.get('challenges', ['संवाद', 'संतुलन']))}
• **संधी:** {', '.join(prediction.get('opportunities', ['नवीन सुरुवात', 'कुटुंब बंध']))}

**💎 सल्ले:**
{chr(10).join([f"• {rec}" for rec in prediction.get('recommendations', ['ध्यान सराव करा', 'कुटुंब वेळ घालवा'])])}

**🎯 कॉस्मिक सल्ला:**
{prediction.get('cosmic_advice', 'आजची ऊर्जा वैयक्तिक विकास आणि कुटुंब सुसंवादाला समर्थन देते.')} ✨"""
        else:
            return f"""🌟 **Personal {prediction_type.title()} Prediction for {member.name}**

**📅 Energy Analysis:**
• **Energy Level:** {prediction.get('energy_level', 'Moderate')}
• **Focus Areas:** {', '.join(prediction.get('focus_areas', ['Personal growth', 'Family harmony']))}
• **Challenges:** {', '.join(prediction.get('challenges', ['Communication', 'Balance']))}
• **Opportunities:** {', '.join(prediction.get('opportunities', ['New beginnings', 'Family bonding']))}

**💎 Recommendations:**
{chr(10).join([f"• {rec}" for rec in prediction.get('recommendations', ['Practice meditation', 'Spend family time'])])}

**🎯 Cosmic Advice:**
{prediction.get('cosmic_advice', 'Today\'s energy supports personal growth and family harmony.')} ✨"""
    
    def _create_generic_prediction_message(self, member: FamilyMember, 
                                         prediction_type: str, language: str) -> str:
        """Create generic prediction message when birth details not available."""
        if language == "mr":
            return f"""🌟 **{member.name} साठी सामान्य {prediction_type} मार्गदर्शन**

**📅 आजचे लक्ष केंद्र:**
• वैयक्तिक विकास आणि सुधारणा
• कुटुंब नातेसंबंध मजबूत करणे
• आरोग्य आणि कल्याण
• आध्यात्मिक विकास

**💎 सल्ले:**
• सकाळचे ध्यान सराव करा
• कुटुंबासोबत गुणवत्तापूर्ण वेळ घालवा
• निरोगी आहार राखा
• कृतज्ञता व्यक्त करा

**🎯 कॉस्मिक सल्ला:**
आजची ऊर्जा तुमच्या वैयक्तिक विकास आणि कुटुंब सुसंवादाला समर्थन देते. ✨"""
        else:
            return f"""🌟 **General {prediction_type.title()} Guidance for {member.name}**

**📅 Today's Focus:**
• Personal development and improvement
• Strengthening family relationships
• Health and wellness
• Spiritual growth

**💎 Recommendations:**
• Practice morning meditation
• Spend quality time with family
• Maintain healthy diet
• Express gratitude

**🎯 Cosmic Advice:**
Today's energy supports your personal growth and family harmony. ✨"""
    
    async def send_family_notification(self, user_id: int, message: str, 
                                     language: str = "en") -> bool:
        """Send notification to all family members."""
        try:
            # Get family members
            family_members = self.family_manager.get_family_members(user_id)
            
            # Send message to each family member
            for member in family_members:
                await self._send_notification_to_member(member, message, language)
            
            logger.info(f"Family notification sent to {len(family_members)} members")
            return True
            
        except Exception as e:
            logger.error(f"Error sending family notification: {e}")
            return False
    
    async def _send_notification_to_member(self, member: FamilyMember, 
                                         message: str, language: str):
        """Send notification to individual family member."""
        try:
            # In real implementation, you'd need the family member's telegram_id
            # For now, we'll just log the message
            logger.info(f"Notification for {member.name} ({language}): {message}")
            
        except Exception as e:
            logger.error(f"Error sending notification to {member.name}: {e}")


# Global family telegram manager instance
family_telegram_manager = None  # Will be initialized with bot token 