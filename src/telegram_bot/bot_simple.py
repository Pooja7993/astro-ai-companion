"""
Simple Astro AI Companion Bot - Personal Family Use Only
Essential features only, no commercial elements
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from loguru import logger

from src.astrology.simple_chart_analyzer import chart_analyzer
from src.database.models import User
from src.utils.config_simple import get_config
from src.family.family_recommendations import family_recommendations

import requests


class SimpleAstroBot:
    """Simple Astro AI Companion Bot for personal family use."""
    
    def __init__(self):
        self.config = get_config()
        self.chart_analyzer = chart_analyzer
        
        # Registration state tracking with detailed state information
        self.pending_registration = {}  # user_id: {step: current_step, data: {collected data}}
        self.pending_profile_update = {}  # user_id: {step: current_step, data: {collected data}}
        
        # Registration steps definition
        self.registration_steps = [
            "first_name", "middle_name", "last_name", 
            "birth_date", "birth_time", "birth_place", "language"
        ]
        
        # Check if telegram token is available
        if not self.config.has_telegram_token():
            raise ValueError("TELEGRAM_BOT_TOKEN is required but not found in environment variables")
        
        # Initialize bot with conflict prevention
        self.application = Application.builder().token(self.config.telegram.telegram_bot_token.get_secret_value()).build()
        
        # Note: delete_webhook removed to avoid async warning
        # The polling mode will handle conflicts automatically
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register essential command handlers."""
        # Basic commands
        self.application.add_handler(CommandHandler('start', self.start_command))
        self.application.add_handler(CommandHandler('register', self.register_command))
        self.application.add_handler(CommandHandler('edit_profile', self.edit_profile_command))
        self.application.add_handler(CommandHandler('help', self.help_command))
        self.application.add_handler(CommandHandler('profile', self.show_profile))
        self.application.add_handler(CommandHandler('commands', self.commands_list))
        self.application.add_handler(CommandHandler('family_members', self.family_members_command))
        self.application.add_handler(CommandHandler('test_openrouter', self.test_openrouter_command))
        
        # Prediction commands
        self.application.add_handler(CommandHandler('daily', self.daily_prediction))
        self.application.add_handler(CommandHandler('weekly', self.weekly_prediction))
        self.application.add_handler(CommandHandler('monthly', self.monthly_prediction))
        self.application.add_handler(CommandHandler('yearly', self.yearly_prediction))
        
        # Personal guidance commands
        self.application.add_handler(CommandHandler('personal', self.personal_guidance))
        self.application.add_handler(CommandHandler('family', self.family_guidance))
        self.application.add_handler(CommandHandler('health', self.health_guidance))
        self.application.add_handler(CommandHandler('relationships', self.relationship_guidance))
        self.application.add_handler(CommandHandler('spiritual', self.spiritual_guidance))
        self.application.add_handler(CommandHandler('life_purpose', self.life_purpose_guidance))
        
        # Other features
        self.application.add_handler(CommandHandler('remedies', self.get_remedies))
        self.application.add_handler(CommandHandler('ask', self.handle_question))
        self.application.add_handler(CommandHandler('family_recommendations', self.family_recommendations_command))
        self.application.add_handler(CommandHandler('ai', self.ai_command))
        
        # Voice and chart commands
        self.application.add_handler(CommandHandler('chart', self.chart_command))
        self.application.add_handler(CommandHandler('prediction_image', self.prediction_image_command))
        self.application.add_handler(CommandHandler('voice_prediction', self.voice_prediction_command))
        
        # Optional enhancements
        self.application.add_handler(CommandHandler('progress', self.show_progress))
        self.application.add_handler(CommandHandler('goals', self.show_goals))
        self.application.add_handler(CommandHandler('set_goal', self.set_goal))
        self.application.add_handler(CommandHandler('timing', self.show_timing))
        self.application.add_handler(CommandHandler('rituals', self.show_rituals))
        
        # Advanced analytics commands
        self.application.add_handler(CommandHandler('analytics', self.analytics_command))
        self.application.add_handler(CommandHandler('dasha', self.dasha_command))
        self.application.add_handler(CommandHandler('transits', self.transits_command))
        self.application.add_handler(CommandHandler('yogas', self.yogas_command))

        # NEW: Moon & Festival commands
        self.application.add_handler(CommandHandler('moon', self.moon_phase_command))
        self.application.add_handler(CommandHandler('festivals', self.festivals_command))
        self.application.add_handler(CommandHandler('auspicious', self.auspicious_command))
        self.application.add_handler(CommandHandler('health', self.health_command))

        # Adaptive learning commands
        self.application.add_handler(CommandHandler('adaptive', self.adaptive_recommendation_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_msg = """🌟 **Welcome to Your Personal Astro AI Companion!**

I'm your personal astrology guide, designed specifically for you and your family. I provide:

**✨ Personal Guidance:**
• Daily cosmic insights and predictions
• Family relationship analysis
• Health and wellness guidance
• Spiritual growth support
• Life purpose discovery

**🎯 How to Use:**
• **Natural chat:** Just type what's on your mind
• **Commands:** Use /daily, /weekly, /family, /health, etc.
• **Questions:** Ask me anything about your life

**👨‍👩‍👧‍👦 Family Features:**
• Personal birth chart analysis
• Family compatibility insights
• Individual guidance for each family member
• Private and secure for your family only

**🚀 Quick Start:**
1. Register with `/register` to create your profile
2. Ask me anything naturally
3. Use commands for specific guidance

Ready to explore your cosmic journey? Start with `/register` or just chat with me! ✨"""
        
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user registration with step-by-step approach."""
        if not update.effective_user or not update.message:
            return
        
        user_id = str(update.effective_user.id)
        from src.database.database import DatabaseManager
        db = DatabaseManager()
        existing_user = db.get_user(user_id)
        if existing_user:
            await update.message.reply_text(
                f"✅ You're already registered! Use /profile to see your details or /edit_profile to update.")
            return
        
        # Initialize registration state with first step
        self.pending_registration[user_id] = {
            "step": "first_name",
            "data": {}
        }
        
        # Start the step-by-step registration process
        await update.message.reply_text(
            "🌟 Welcome to the step-by-step profile creation!\n\n"
            "Let's start with your first name.\n\n"
            "*What is your first name?*", parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural conversation messages."""
        if not update.effective_user or not update.message:
            return
        
        user_id = str(update.effective_user.id)
        message_text = update.message.text.strip()
        from src.database.database import DatabaseManager
        db = DatabaseManager()
        
        # Handle step-by-step registration
        if user_id in self.pending_registration:
            registration_state = self.pending_registration[user_id]
            current_step = registration_state["step"]
            data = registration_state["data"]
            
            # Process current step
            if current_step == "first_name":
                data["first_name"] = message_text
                registration_state["step"] = "middle_name"
                await update.message.reply_text("What is your middle name? (Type 'none' if you don't have one)")
                
            elif current_step == "middle_name":
                if message_text.lower() == "none":
                    data["middle_name"] = ""
                else:
                    data["middle_name"] = message_text
                registration_state["step"] = "last_name"
                await update.message.reply_text("What is your last name?")
                
            elif current_step == "last_name":
                data["last_name"] = message_text
                registration_state["step"] = "birth_date"
                await update.message.reply_text(
                    "What is your date of birth? (Format: YYYY-MM-DD)\n\n"
                    "Example: 1990-01-15")
                
            elif current_step == "birth_date":
                # Validate date format
                import re
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', message_text):
                    await update.message.reply_text(
                        "❌ Invalid date format. Please use YYYY-MM-DD format.\n"
                        "Example: 1990-01-15")
                    return
                
                data["birth_date"] = message_text
                registration_state["step"] = "birth_time"
                await update.message.reply_text(
                    "What is your time of birth? (Format: HH:MM)\n\n"
                    "Example: 14:30")
                
            elif current_step == "birth_time":
                # Validate time format
                import re
                if not re.match(r'^\d{1,2}:\d{2}$', message_text):
                    await update.message.reply_text(
                        "❌ Invalid time format. Please use HH:MM format.\n"
                        "Example: 14:30")
                    return
                
                data["birth_time"] = message_text
                registration_state["step"] = "birth_place"
                await update.message.reply_text(
                    "What is your place of birth?\n\n"
                    "Example: Mumbai, India")
                
            elif current_step == "birth_place":
                data["birth_place"] = message_text
                registration_state["step"] = "language"
                await update.message.reply_text(
                    "What is your preferred language?\n\n"
                    "Options:\n"
                    "- en (English)\n"
                    "- mr (Marathi)")
                
            elif current_step == "language":
                language = message_text.lower()
                if language not in ["en", "mr"]:
                    await update.message.reply_text(
                        "❌ Invalid language. Please choose 'en' for English or 'mr' for Marathi.")
                    return
                
                data["language"] = language
                registration_state["step"] = "confirmation"
                
                # Show summary for confirmation
                first = data["first_name"]
                middle = data["middle_name"]
                last = data["last_name"]
                name = f"{first} {middle} {last}".strip()
                if middle == "":
                    name = f"{first} {last}"
                
                summary = (
                    f"📝 *Profile Summary*\n\n"
                    f"Name: {name}\n"
                    f"Date of Birth: {data['birth_date']}\n"
                    f"Time of Birth: {data['birth_time']}\n"
                    f"Place of Birth: {data['birth_place']}\n"
                    f"Language: {data['language']}\n\n"
                    f"Is this information correct? (yes/no)"
                )
                await update.message.reply_text(summary, parse_mode='Markdown')
                
            elif current_step == "confirmation":
                if message_text.lower() == "yes":
                    # Create user profile
                    first = data["first_name"]
                    middle = data["middle_name"]
                    last = data["last_name"]
                    name = f"{first} {middle} {last}".strip()
                    if middle == "":
                        name = f"{first} {last}"
                    
                    from src.database.models import User
                    user = User(
                        telegram_id=user_id,
                        chat_id=user_id,
                        name=name,
                        birth_date=data["birth_date"],
                        birth_time=data["birth_time"],
                        birth_place=data["birth_place"],
                        language_preference=data["language"],
                        daily_reports_enabled=True,
                        realtime_guidance_enabled=True
                    )
                    db.create_user(user)
                    del self.pending_registration[user_id]
                    await update.message.reply_text(f"✅ Profile created for {name}! Use /profile to view.")
                else:
                    # Restart registration
                    await update.message.reply_text("Let's start over. What is your first name?")
                    self.pending_registration[user_id] = {
                        "step": "first_name",
                        "data": {}
                    }
            return
        if user_id in self.pending_profile_update:
            # Step-by-step profile update flow
            update_state = self.pending_profile_update[user_id]
            current_step = update_state["step"]
            data = update_state["data"]
            
            # Process current step
            if current_step == "first_name":
                if message_text.lower() != "keep":
                    data["first_name"] = message_text
                update_state["step"] = "middle_name"
                await update.message.reply_text(
                    f"Your current middle name is: *{data['middle_name']}*\n"
                    f"Enter your new middle name, type 'none' for no middle name, or type 'keep' to keep the current value:", 
                    parse_mode='Markdown')
                
            elif current_step == "middle_name":
                if message_text.lower() == "none":
                    data["middle_name"] = ""
                elif message_text.lower() != "keep":
                    data["middle_name"] = message_text
                update_state["step"] = "last_name"
                await update.message.reply_text(
                    f"Your current last name is: *{data['last_name']}*\n"
                    f"Enter your new last name or type 'keep' to keep the current value:", 
                    parse_mode='Markdown')
                
            elif current_step == "last_name":
                if message_text.lower() != "keep":
                    data["last_name"] = message_text
                update_state["step"] = "birth_date"
                await update.message.reply_text(
                    f"Your current date of birth is: *{data['birth_date']}*\n"
                    f"Enter your new date of birth (Format: YYYY-MM-DD) or type 'keep' to keep the current value:", 
                    parse_mode='Markdown')
                
            elif current_step == "birth_date":
                if message_text.lower() != "keep":
                    # Validate date format
                    import re
                    if not re.match(r'^\d{4}-\d{2}-\d{2}$', message_text):
                        await update.message.reply_text(
                            "❌ Invalid date format. Please use YYYY-MM-DD format.\n"
                            "Example: 1990-01-15\n"
                            "Or type 'keep' to keep your current value.")
                        return
                    data["birth_date"] = message_text
                
                update_state["step"] = "birth_time"
                await update.message.reply_text(
                    f"Your current time of birth is: *{data['birth_time']}*\n"
                    f"Enter your new time of birth (Format: HH:MM) or type 'keep' to keep the current value:", 
                    parse_mode='Markdown')
                
            elif current_step == "birth_time":
                if message_text.lower() != "keep":
                    # Validate time format
                    import re
                    if not re.match(r'^\d{1,2}:\d{2}$', message_text):
                        await update.message.reply_text(
                            "❌ Invalid time format. Please use HH:MM format.\n"
                            "Example: 14:30\n"
                            "Or type 'keep' to keep your current value.")
                        return
                    data["birth_time"] = message_text
                
                update_state["step"] = "birth_place"
                await update.message.reply_text(
                    f"Your current place of birth is: *{data['birth_place']}*\n"
                    f"Enter your new place of birth or type 'keep' to keep the current value:", 
                    parse_mode='Markdown')
                
            elif current_step == "birth_place":
                if message_text.lower() != "keep":
                    data["birth_place"] = message_text
                update_state["step"] = "language"
                await update.message.reply_text(
                    f"Your current language preference is: *{data['language']}*\n"
                    f"Enter your new language preference (en/mr) or type 'keep' to keep the current value:\n\n"
                    f"Options:\n"
                    f"- en (English)\n"
                    f"- mr (Marathi)", 
                    parse_mode='Markdown')
                
            elif current_step == "language":
                if message_text.lower() != "keep":
                    language = message_text.lower()
                    if language not in ["en", "mr"]:
                        await update.message.reply_text(
                            "❌ Invalid language. Please choose 'en' for English or 'mr' for Marathi.\n"
                            "Or type 'keep' to keep your current value.")
                        return
                    data["language"] = language
                
                update_state["step"] = "confirmation"
                
                # Show summary for confirmation
                first = data["first_name"]
                middle = data["middle_name"]
                last = data["last_name"]
                name = f"{first} {middle} {last}".strip()
                if middle == "":
                    name = f"{first} {last}"
                
                summary = (
                    f"📝 *Updated Profile Summary*\n\n"
                    f"Name: {name}\n"
                    f"Date of Birth: {data['birth_date']}\n"
                    f"Time of Birth: {data['birth_time']}\n"
                    f"Place of Birth: {data['birth_place']}\n"
                    f"Language: {data['language']}\n\n"
                    f"Is this information correct? (yes/no)"
                )
                await update.message.reply_text(summary, parse_mode='Markdown')
                
            elif current_step == "confirmation":
                if message_text.lower() == "yes":
                    # Update user profile
                    first = data["first_name"]
                    middle = data["middle_name"]
                    last = data["last_name"]
                    name = f"{first} {middle} {last}".strip()
                    if middle == "":
                        name = f"{first} {last}"
                    
                    from src.database.models import User
                    user = User(
                        telegram_id=user_id,
                        chat_id=user_id,
                        name=name,
                        birth_date=data["birth_date"],
                        birth_time=data["birth_time"],
                        birth_place=data["birth_place"],
                        language_preference=data["language"],
                        daily_reports_enabled=True,
                        realtime_guidance_enabled=True
                    )
                    db.update_user(user)
                    del self.pending_profile_update[user_id]
                    await update.message.reply_text(f"✅ Profile updated for {name}! Use /profile to view.")
                else:
                    # Restart profile update
                    await update.message.reply_text("Let's start over. What is your first name?")
                    # Re-initialize with existing data
                    existing_user = db.get_user(user_id)
                    name_parts = existing_user.name.split()
                    first_name = name_parts[0] if name_parts else ""
                    last_name = name_parts[-1] if len(name_parts) > 1 else ""
                    middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
                    
                    self.pending_profile_update[user_id] = {
                        "step": "first_name",
                        "data": {
                            "first_name": first_name,
                            "middle_name": middle_name,
                            "last_name": last_name,
                            "birth_date": existing_user.birth_date,
                            "birth_time": existing_user.birth_time,
                            "birth_place": existing_user.birth_place,
                            "language": existing_user.language_preference
                        }
                    }
                    await update.message.reply_text(
                        f"Your current first name is: *{first_name}*\n"
                        f"Enter your new first name or type 'keep' to keep the current value:", 
                        parse_mode='Markdown')
            return
        # Default: handle as general query
        user = db.get_user(user_id)
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        await self._handle_general_query(update, message_text, user)
    
    async def _handle_registration(self, update: Update, message_text: str, user_id: str):
        """Handle user registration with birth details."""
        try:
            parts = message_text.split('|')
            if len(parts) < 4 or len(parts) > 5:
                await update.message.reply_text(
                    "❌ Please provide all details in the correct format:\n"
                    "**Name|Date of Birth|Time of Birth|Place of Birth|Language**\n\n"
                    "Example:\n"
                    "`John Doe|1990-01-15|14:30|Mumbai, India|en`\n\n"
                    "Language: en (English) or mr (Marathi)"
                )
                return
            
            name, dob, tob, place = [part.strip() for part in parts[:4]]
            language = parts[4].strip() if len(parts) == 5 else 'en'
            
            # Validate language
            if language not in ['en', 'mr']:
                language = 'en'
            
            # Get chat_id for direct messaging
            chat_id = str(update.effective_user.id)
            
            # Create user profile
            user = User(
                telegram_id=user_id,
                chat_id=chat_id,
                name=name,
                birth_date=dob,
                birth_time=tob,
                birth_place=place,
                language_preference=language,
                daily_reports_enabled=True,
                realtime_guidance_enabled=True
            )
            
            # Save to database (simplified for this example)
            # In real implementation, save to actual database
            
            await update.message.reply_text(
                f"✅ **Welcome to your personal astrology companion, {name}!**\n\n"
                f"**Profile Created Successfully:**\n"
                f"• **Name:** {name}\n"
                f"• **Birth Date:** {dob}\n"
                f"• **Birth Time:** {tob}\n"
                f"• **Birth Place:** {place}\n"
                f"• **Language:** {language.upper()}\n\n"
                "I can now provide you with:\n\n"
                "• **Personal daily guidance** based on your birth chart\n"
                "• **Family insights** and relationship analysis\n"
                "• **Health and wellness** cosmic guidance\n"
                "• **Spiritual growth** and life purpose insights\n\n"
                "Try asking me anything naturally, or use commands like:\n"
                "• `/daily` - Today's guidance\n"
                "• `/family` - Family insights\n"
                "• `/health` - Wellness guidance\n"
                "• `/personal` - Personal life guidance\n"
                "• `/edit_profile` - Update your profile\n\n"
                "What would you like to know about your cosmic journey? ✨",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            await update.message.reply_text(
                "❌ Sorry, there was an error creating your profile. Please try again with the correct format."
            )
    
    async def _handle_general_query(self, update: Update, message_text: str, user):
        """Handle general user queries."""
        try:
            # Generate personalized response
            response = self._generate_personal_response(message_text, user.name)
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error handling general query: {e}")
            await update.message.reply_text(
                "❌ Sorry, I couldn't process your request right now. Please try again."
            )
    
    def _generate_personal_response(self, message_text: str, user_name: str) -> str:
        """Generate personalized response based on message."""
        message_lower = message_text.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            return f"🌟 Hello {user_name}! How can I help you with your cosmic journey today?"
        
        elif any(word in message_lower for word in ['daily', 'today', 'day']):
            return f"📅 **Today's Guidance for {user_name}**\n\nToday is perfect for new beginnings and important decisions. Focus on your personal growth and family harmony. The cosmic energy supports your spiritual journey and inner peace."
        
        elif any(word in message_lower for word in ['family', 'relationship', 'love']):
            return f"👨‍👩‍👧‍👦 **Family Guidance for {user_name}**\n\nYour family bonds are strong and supportive. Focus on open communication and quality time together. The cosmic energy favors family harmony and emotional connections."
        
        elif any(word in message_lower for word in ['health', 'wellness', 'fitness']):
            return f"🏥 **Health Guidance for {user_name}**\n\nFocus on physical and mental wellness. Practice morning meditation and maintain a balanced diet. The cosmic energy supports your vitality and inner peace."
        
        elif any(word in message_lower for word in ['spiritual', 'purpose', 'meaning']):
            return f"🙏 **Spiritual Guidance for {user_name}**\n\nYour spiritual path is clear and purposeful. Focus on meditation, prayer, and service to others. The cosmic energy supports your spiritual growth and wisdom."
        
        elif any(word in message_lower for word in ['career', 'work', 'job']):
            return f"💼 **Career Guidance for {user_name}**\n\nYour professional path involves helping others through meaningful work. Focus on service, teaching, and guidance. The cosmic energy supports your leadership and wisdom."
        
        else:
            return f"🌟 **Personal Guidance for {user_name}**\n\nI sense you're seeking guidance. Based on your cosmic energy, focus on personal growth, family harmony, and spiritual development. Trust your intuition and follow your heart's calling."
    
    def _get_user_sync(self, telegram_id: str) -> Optional[User]:
        """Get user from database (simplified)."""
        from src.database.database import DatabaseManager
        db = DatabaseManager()
        return db.get_user(telegram_id)
    
    async def personal_guidance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Provide comprehensive personal life guidance."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            personal_msg = f"""🌟 **Personal Life Guidance for {user.name}**

**🎯 Your Personal Energy Analysis:**
Based on your birth chart, here's your complete personal guidance:

**💫 Personal Strengths:**
• **Natural talents:** Strong intuition and empathy
• **Life purpose:** Service to others and spiritual growth
• **Best timing:** Morning hours for important decisions

**🌙 Daily Personal Routine:**
• **Morning (6-8 AM):** Meditation and intention setting
• **Mid-morning (9-11 AM):** Focus on important decisions
• **Afternoon (2-4 PM):** Creative activities and learning
• **Evening (6-8 PM):** Family time and relaxation
• **Night (9-10 PM):** Reflection and planning

**💝 Personal Growth Areas:**
• **Self-improvement:** Patience, compassion, and wisdom
• **Challenges to overcome:** Balancing personal and family needs
• **Opportunities:** Spiritual growth and family harmony

**🎯 Personal Success Formula:**
1. **Morning routine:** Start with gratitude and intention
2. **Decision timing:** Trust your intuition during strong periods
3. **Personal development:** Focus on your unique talents
4. **Life balance:** Maintain harmony between all life areas

Want specific personal guidance? Ask me naturally or use:
/family /health /relationships /spiritual /life_purpose ✨"""
            
            await update.message.reply_text(personal_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Personal guidance error: {e}")
            await update.message.reply_text("❌ Error generating personal guidance. Please try again.")
    
    async def family_guidance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Specialized family and relationship guidance."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            current_time = datetime.now()
            
            family_msg = f"""👨‍👩‍👧‍👦 **Family & Relationship Guidance for {user.name}**

**💝 FAMILY ENERGY ANALYSIS ({current_time.strftime('%A, %B %d')}):**

**🏠 FAMILY DYNAMICS:**
• **Family harmony:** Strong bonds with supportive environment
• **Communication style:** Open and warm family communication
• **Family strengths:** Emotional support and mutual understanding

**💑 RELATIONSHIP INSIGHTS:**
• **Love compatibility:** High compatibility with caring partners
• **Marriage timing:** Venus strong periods bring relationship opportunities
• **Relationship challenges:** Communication during Mercury retrograde

**👶 FAMILY PLANNING:**
• **Children timing:** Jupiter periods favorable for family expansion
• **Parent-child bonds:** Strong emotional connections
• **Family growth:** Steady family development and harmony

**🎯 FAMILY SUCCESS FORMULA:**
1. **Morning family time:** Start day with family bonding
2. **Communication hours:** 6-8 PM best for family discussions
3. **Weekend activities:** Plan family activities during Venus strong periods
4. **Family rituals:** Create meaningful family traditions

**💎 FAMILY REMEDIES:**
• **Daily practice:** Light a diya for family harmony
• **Monday ritual:** Offer water to Sun for family strength
• **Friday offering:** White flowers for Venus's love blessing
• **Family protection:** Keep a small Ganesh idol in family area

Want more specific guidance? Ask me: "How can I improve family relationships?" or "What's best for my family?" 👨‍👩‍👧‍👦"""
            
            await update.message.reply_text(family_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Family guidance error: {e}")
            await update.message.reply_text("❌ Error generating family guidance. Please try again.")

    async def health_guidance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Specialized health and wellness guidance."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            current_time = datetime.now()
            
            health_msg = f"""🏥 **Health & Wellness Guidance for {user.name}**

**💪 HEALTH ENERGY ANALYSIS ({current_time.strftime('%A, %B %d')}):**

**🌿 WELLNESS FOCUS:**
• **Physical health:** Strong constitution with good vitality
• **Mental wellness:** Balanced emotional and mental state
• **Energy levels:** High energy during Sun strong periods

**🏃‍♂️ FITNESS GUIDANCE:**
• **Best exercise times:** 6-8 AM for maximum energy
• **Workout types:** Yoga and meditation for mental peace
• **Recovery periods:** Rest during Moon weak periods

**🍎 NUTRITION ADVICE:**
• **Diet focus:** Fresh fruits and vegetables
• **Hydration:** Drink water with copper vessel benefits
• **Fasting:** Tuesday fasting for health benefits

**😴 SLEEP & REST:**
• **Sleep timing:** 10 PM to 6 AM for optimal rest
• **Sleep quality:** Deep sleep during Moon strong periods
• **Relaxation:** Evening meditation for peace

**💎 HEALTH REMEDIES:**
• **Daily practice:** Morning sun salutation
• **Tuesday ritual:** Fasting for health purification
• **Wednesday offering:** Green vegetables for health
• **Health protection:** Keep basil plant for wellness

Want more specific guidance? Ask me: "How can I improve my health?" or "What's best for my wellness?" 🏥"""
            
            await update.message.reply_text(health_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Health guidance error: {e}")
            await update.message.reply_text("❌ Error generating health guidance. Please try again.")

    async def relationship_guidance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Specialized relationship and love guidance."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            current_time = datetime.now()
            
            relationship_msg = f"""💕 **Relationship & Love Guidance for {user.name}**

**💝 LOVE ENERGY ANALYSIS ({current_time.strftime('%A, %B %d')}):**

**💑 RELATIONSHIP INSIGHTS:**
• **Love compatibility:** High compatibility with caring partners
• **Marriage timing:** Venus strong periods bring relationship opportunities
• **Relationship challenges:** Communication during Mercury retrograde

**💕 LOVE LIFE FOCUS:**
• **Romantic timing:** Friday evenings for romantic activities
• **Communication:** Open and honest communication style
• **Emotional bonds:** Deep emotional connections

**💍 MARRIAGE GUIDANCE:**
• **Marriage timing:** Jupiter periods favorable for marriage
• **Partner qualities:** Caring, supportive, and understanding
• **Marriage success:** Strong foundation with mutual respect

**💎 RELATIONSHIP REMEDIES:**
• **Daily practice:** Light rose incense for love
• **Friday ritual:** Wear pink for Venus's love blessing
• **Love offering:** White flowers for relationship harmony
• **Love protection:** Keep rose quartz for love energy

Want more specific guidance? Ask me: "How can I improve my relationships?" or "What's best for my love life?" 💕"""
            
            await update.message.reply_text(relationship_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Relationship guidance error: {e}")
            await update.message.reply_text("❌ Error generating relationship guidance. Please try again.")

    async def spiritual_guidance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Specialized spiritual and life purpose guidance."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            current_time = datetime.now()
            
            spiritual_msg = f"""🙏 **Spiritual & Life Purpose Guidance for {user.name}**

**🌟 SPIRITUAL ENERGY ANALYSIS ({current_time.strftime('%A, %B %d')}):**

**🧘 SPIRITUAL FOCUS:**
• **Life purpose:** Service to others and spiritual growth
• **Spiritual path:** Meditation and self-realization
• **Inner peace:** Strong connection with higher consciousness

**🎯 LIFE PURPOSE:**
• **Career calling:** Helping others through service
• **Personal mission:** Spiritual teaching and guidance
• **Life lessons:** Learning patience and compassion

**🙏 SPIRITUAL PRACTICES:**
• **Meditation timing:** 4-6 AM for spiritual connection
• **Prayer focus:** Devotion and gratitude practices
• **Spiritual growth:** Continuous learning and self-improvement

**💎 SPIRITUAL REMEDIES:**
• **Daily practice:** Morning meditation and prayer
• **Thursday ritual:** Visit temple for spiritual blessings
• **Spiritual offering:** White flowers for purity
• **Spiritual protection:** Keep sacred texts for wisdom

Want more specific guidance? Ask me: "What's my life purpose?" or "How can I grow spiritually?" 🙏"""
            
            await update.message.reply_text(spiritual_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Spiritual guidance error: {e}")
            await update.message.reply_text("❌ Error generating spiritual guidance. Please try again.")

    async def life_purpose_guidance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Specialized life purpose and career guidance."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            current_time = datetime.now()
            
            purpose_msg = f"""🎯 **Life Purpose & Career Guidance for {user.name}**

**🌟 LIFE PURPOSE ANALYSIS ({current_time.strftime('%A, %B %d')}):**

**💼 CAREER FOCUS:**
• **Natural talents:** Leadership and service abilities
• **Career calling:** Helping others through meaningful work
• **Success areas:** Teaching, counseling, and guidance

**🎯 LIFE MISSION:**
• **Personal mission:** Making a positive impact on others
• **Life lessons:** Learning patience, compassion, and wisdom
• **Life purpose:** Service to family and community

**💪 STRENGTHS & GIFTS:**
• **Natural abilities:** Strong intuition and empathy
• **Leadership qualities:** Inspiring and guiding others
• **Creative talents:** Artistic and spiritual expression

**💎 LIFE PURPOSE REMEDIES:**
• **Daily practice:** Morning intention setting
• **Career ritual:** Light yellow candle for success
• **Purpose offering:** Yellow flowers for wisdom
• **Success protection:** Keep citrine crystal for abundance

Want more specific guidance? Ask me: "What's my true calling?" or "How can I fulfill my purpose?" 🎯"""
            
            await update.message.reply_text(purpose_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Life purpose guidance error: {e}")
            await update.message.reply_text("❌ Error generating life purpose guidance. Please try again.")

    async def daily_prediction(self, update: Update, context: Optional[ContextTypes.DEFAULT_TYPE]):
        """Provide daily prediction using advanced analytics and adaptive recommendations."""
        if not update.effective_user or not update.message:
            return
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        try:
            from src.astrology.advanced_analytics import advanced_analytics
            from src.utils.feedback_learning import feedback_learning
            
            user_data = {
                'name': user.name,
                'birth_date': user.birth_date,
                'birth_time': user.birth_time,
                'birth_place': user.birth_place
            }
            
            # Get adaptive recommendation
            adaptive_prediction = feedback_learning.generate_adaptive_recommendation(
                str(update.effective_user.id), 'daily', user.name
            )
            
            # Try advanced analytics first
            prediction = advanced_analytics.get_advanced_prediction(user_data, 'daily')
            if 'error' in prediction:
                # Use adaptive recommendation as fallback
                await update.message.reply_text(adaptive_prediction, parse_mode='Markdown')
            else:
                # Combine advanced analytics with adaptive elements
                combined_prediction = prediction['prediction'] + "\n\n" + adaptive_prediction
                await update.message.reply_text(combined_prediction, parse_mode='Markdown')
            
            # Add feedback prompt
            feedback_prompt = feedback_learning.create_feedback_prompt('daily')
            await update.message.reply_text(feedback_prompt, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Daily prediction error: {e}")
            await update.message.reply_text("❌ Error generating daily prediction. Please try again.")

    async def handle_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user feedback reactions."""
        if not update.effective_user or not update.message:
            return
        
        user_id = str(update.effective_user.id)
        message_text = update.message.text.lower()
        
        # Determine feedback score based on message
        if any(word in message_text for word in ['👍', 'helpful', 'good', 'great', 'love']):
            feedback_score = 5
        elif any(word in message_text for word in ['👎', 'not helpful', 'bad', 'useless']):
            feedback_score = 1
        else:
            feedback_score = 3  # Neutral
        
        try:
            from src.utils.feedback_learning import feedback_learning
            
            # Store feedback
            success = feedback_learning.collect_feedback(
                user_id, 'general', feedback_score, update.message.text
            )
            
            if success:
                if feedback_score >= 4:
                    await update.message.reply_text("🌟 Thank you for your positive feedback! We'll continue to provide helpful guidance for you and your family! ✨")
                elif feedback_score <= 2:
                    await update.message.reply_text("🙏 Thank you for your feedback! We'll work to improve and provide better guidance for you! ✨")
                else:
                    await update.message.reply_text("💫 Thank you for your feedback! We're here to support your cosmic journey! ✨")
            else:
                await update.message.reply_text("❌ Error saving feedback. Please try again.")
                
        except Exception as e:
            logger.error(f"Feedback handling error: {e}")
            await update.message.reply_text("❌ Error processing feedback. Please try again.")

    async def adaptive_recommendation_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get personalized adaptive recommendation."""
        if not update.effective_user or not update.message:
            return
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        try:
            from src.utils.feedback_learning import feedback_learning
            
            # Get user preferences
            preferences = feedback_learning.get_user_preferences(str(update.effective_user.id))
            
            # Generate adaptive recommendation
            recommendation = feedback_learning.generate_adaptive_recommendation(
                str(update.effective_user.id), 'personal', user.name
            )
            
            # Add preferences summary
            preferences_summary = f"""

**📊 Your Learning Profile:**
• **Favorite Topics:** {', '.join(preferences.get('favorite_categories', ['Daily', 'Family']))}
• **Preferred Style:** {preferences.get('preferred_style', 'Balanced').title()}
• **Feedback Score:** {preferences.get('feedback_score', 3):.1f}/5.0
• **Total Feedback:** {preferences.get('total_feedback', 0)} responses

**💫 Your personalized guidance is based on your feedback and preferences!** ✨"""
            
            full_recommendation = recommendation + preferences_summary
            await update.message.reply_text(full_recommendation, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Adaptive recommendation error: {e}")
            await update.message.reply_text("❌ Error generating adaptive recommendation. Please try again.")

    async def weekly_prediction(self, update: Update, context: Optional[ContextTypes.DEFAULT_TYPE]):
        """Handle weekly prediction command."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            weekly_msg = f"""📅 **Weekly Cosmic Forecast for {user.name}**

**🌟 This Week's Energy:**
• **Monday:** New beginnings and fresh starts
• **Tuesday:** Overcoming challenges and obstacles
• **Wednesday:** Learning and skill development
• **Thursday:** Major decisions and investments
• **Friday:** Relationship building and networking
• **Saturday:** Review progress and course corrections
• **Sunday:** Planning and spiritual activities

**💫 Weekly Focus Areas:**
• **Personal development:** Self-improvement and growth
• **Family relationships:** Strengthening family bonds
• **Health and wellness:** Physical and mental well-being
• **Spiritual growth:** Inner peace and wisdom

**🎯 Weekly Opportunities:**
• **Career growth:** Professional development
• **Family harmony:** Quality time with loved ones
• **Health improvement:** Wellness activities
• **Spiritual connection:** Meditation and prayer

**💎 Weekly Remedies:**
• **Monday:** Start week with positive intentions
• **Tuesday:** Fasting for health and purification
• **Wednesday:** Green vegetables for wellness
• **Thursday:** Temple visit for blessings
• **Friday:** White flowers for love and harmony
• **Saturday:** Family rituals and bonding
• **Sunday:** Planning and spiritual activities

May this week bring you abundant blessings and growth! ✨"""
            
            await update.message.reply_text(weekly_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Weekly prediction error: {e}")
            await update.message.reply_text("❌ Error generating weekly prediction. Please try again.")

    async def monthly_prediction(self, update: Update, context: Optional[ContextTypes.DEFAULT_TYPE]):
        """Handle monthly prediction command."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            monthly_msg = f"""🌙 **Monthly Cosmic Overview for {user.name}**

**📅 This Month's Energy:**
• **Week 1:** New beginnings and fresh starts
• **Week 2:** Growth and development phase
• **Week 3:** Challenges and learning opportunities
• **Week 4:** Achievement and celebration

**💫 Monthly Focus Areas:**
• **Personal growth:** Self-improvement and development
• **Family harmony:** Strengthening family relationships
• **Health and wellness:** Physical and mental well-being
• **Spiritual connection:** Inner peace and wisdom

**🎯 Monthly Opportunities:**
• **Career advancement:** Professional growth
• **Family bonding:** Quality time with loved ones
• **Health improvement:** Wellness activities
• **Spiritual growth:** Meditation and prayer

**💎 Monthly Remedies:**
• **Daily practice:** Morning meditation and prayer
• **Weekly rituals:** Family bonding activities
• **Health focus:** Balanced diet and exercise
• **Spiritual practice:** Regular temple visits

May this month bring you abundant blessings and success! ✨"""
            
            await update.message.reply_text(monthly_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Monthly prediction error: {e}")
            await update.message.reply_text("❌ Error generating monthly prediction. Please try again.")

    async def yearly_prediction(self, update: Update, context: Optional[ContextTypes.DEFAULT_TYPE]):
        """Handle yearly prediction command."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            yearly_msg = f"""🎯 **Annual Cosmic Forecast for {user.name}**

**🌟 This Year's Energy:**
• **Quarter 1:** New beginnings and fresh starts
• **Quarter 2:** Growth and development phase
• **Quarter 3:** Challenges and learning opportunities
• **Quarter 4:** Achievement and celebration

**💫 Annual Focus Areas:**
• **Personal growth:** Self-improvement and development
• **Family harmony:** Strengthening family relationships
• **Health and wellness:** Physical and mental well-being
• **Spiritual connection:** Inner peace and wisdom

**🎯 Annual Opportunities:**
• **Career advancement:** Professional growth and success
• **Family bonding:** Quality time with loved ones
• **Health improvement:** Wellness activities and vitality
• **Spiritual growth:** Meditation, prayer, and wisdom

**💎 Annual Remedies:**
• **Daily practice:** Morning meditation and prayer
• **Weekly rituals:** Family bonding activities
• **Monthly focus:** Health and wellness activities
• **Quarterly goals:** Spiritual growth and development

May this year bring you abundant blessings, success, and fulfillment! ✨"""
            
            await update.message.reply_text(yearly_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Yearly prediction error: {e}")
            await update.message.reply_text("❌ Error generating yearly prediction. Please try again.")

    async def show_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user profile."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            profile_msg = f"""👤 **Your Personal Profile**

**📋 Basic Information:**
• **Name:** {user.name}
• **Birth Date:** {user.birth_date}
• **Birth Time:** {user.birth_time}
• **Birth Place:** {user.birth_place}
• **Language:** {user.language_preference}

**⚙️ Settings:**
• **Daily Reports:** {'✅ Enabled' if user.daily_reports_enabled else '❌ Disabled'}
• **Real-time Guidance:** {'✅ Enabled' if user.realtime_guidance_enabled else '❌ Disabled'}

**🎯 Your Cosmic Profile:**
• **Life Purpose:** Service to others and spiritual growth
• **Natural Talents:** Strong intuition and empathy
• **Family Focus:** Loving and supportive family bonds
• **Health Energy:** Strong constitution and vitality

**💎 Personal Remedies:**
• **Daily:** Morning meditation and prayer
• **Weekly:** Family bonding activities
• **Monthly:** Health and wellness focus
• **Yearly:** Spiritual growth and development

Your profile is set up for personalized cosmic guidance! ✨"""
            
            await update.message.reply_text(profile_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Profile error: {e}")
            await update.message.reply_text("❌ Error showing profile. Please try again.")

    async def get_remedies(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Provide personalized remedies."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            remedies_msg = f"""💎 **Personalized Remedies for {user.name}**

**🌅 Daily Remedies:**
• **Morning:** Light a diya and chant "Om Namah Shivaya"
• **Afternoon:** Drink water from copper vessel
• **Evening:** Family prayer and gratitude practice
• **Night:** Reflect on the day's blessings

**📅 Weekly Remedies:**
• **Monday:** Offer water to Sun for strength
• **Tuesday:** Fasting for health purification
• **Wednesday:** Green vegetables for wellness
• **Thursday:** Visit temple for spiritual blessings
• **Friday:** White flowers for love and harmony
• **Saturday:** Family rituals and bonding
• **Sunday:** Planning and spiritual activities

**🌙 Monthly Remedies:**
• **New Moon:** New beginnings and fresh starts
• **Full Moon:** Achievement and celebration
• **Waxing Moon:** Growth and development
• **Waning Moon:** Reflection and purification

**🎯 Special Remedies:**
• **Health:** Keep basil plant for wellness
• **Family:** Light diya for family harmony
• **Love:** Rose quartz for love energy
• **Success:** Citrine crystal for abundance
• **Spiritual:** Sacred texts for wisdom

**💫 Personalized Practices:**
• **Meditation:** 4-6 AM for spiritual connection
• **Prayer:** Devotion and gratitude practices
• **Family Time:** 6-8 PM for family bonding
• **Self-Care:** Regular health and wellness activities

These remedies will bring harmony, health, and happiness to your life! ✨"""
            
            await update.message.reply_text(remedies_msg, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Remedies error: {e}")
            await update.message.reply_text("❌ Error generating remedies. Please try again.")

    async def handle_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle specific questions."""
        if not update.effective_user or not update.message:
            return
        
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Extract question from command
            question = ' '.join(context.args) if context.args else "general guidance"
            
            response = self._generate_personal_response(question, user.name)
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Question handling error: {e}")
            await update.message.reply_text("❌ Error processing your question. Please try again.")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        if not update.effective_user or not update.message:
            return
        
        help_text = """🌟 **Astro AI Companion Help** 🌟

**🌙 Core Commands:**
/start - Start the bot
/register - Create your profile
/edit_profile - Update your profile
/profile - View your details
/help - Show this help

**📅 Predictions:**
/daily - Today's cosmic guidance
/weekly - This week's forecast
/monthly - Monthly overview
/yearly - Annual predictions

**🌙 New Moon & Festival Features:**
/moon - Current moon phase guidance
/festivals - Upcoming festivals
/auspicious - Auspicious days
/health - Health & wellness guidance

**🔮 Advanced Analytics:**
/analytics - Comprehensive analysis
/dasha - Current dasha period
/transits - Planetary transits
/yogas - Active yogas

**🖼️ Voice & Charts:**
/chart - Generate birth chart
/prediction_image - Prediction as image
/voice_prediction - Voice prediction

**🤖 AI Features:**
/ai - Advanced AI chat
/adaptive - Adaptive recommendations
/test_openrouter - Test OpenRouter API connection

**👨‍👩‍👧‍👦 Family:**
/family_recommendations - Family guidance
/family_members - View family members

**💫 Personal Guidance:**
/personal - Personal life guidance
/family - Family insights
/health - Health guidance
/relationships - Relationship advice
/spiritual - Spiritual growth
/life_purpose - Life purpose guidance

**📊 Optional Features:**
/progress - Track progress
/goals - View goals
/set_goal - Set new goals
/timing - Timing recommendations
/rituals - Family rituals

**🔮 Consultation:**
/ask [question] - Ask specific questions
/remedies - Personalized remedies

**Need more details? Use /commands for complete list!** ✨"""
        
        await update.message.reply_text(help_text)

    async def family_recommendations_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle family recommendations command."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get simple family recommendations (1 remedy + warnings only)
            recommendations = family_recommendations.get_simple_family_recommendations(user)
            
            if "error" in recommendations:
                await update.message.reply_text("❌ Error generating family recommendations. Please try again.")
                return
            
            # Format and send the message (English only)
            message = family_recommendations.format_simple_family_recommendations_message(recommendations, user)
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Family recommendations error: {e}")
            await update.message.reply_text("❌ Error generating family recommendations. Please try again.")

    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show progress tracking summary."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get progress summary
            from src.tracking.progress_tracker import progress_tracker
            summary = progress_tracker.get_weekly_progress_summary(1)  # Assuming user_id = 1
            
            # Format and send message
            message = progress_tracker.format_progress_summary_message(summary, user)
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Progress tracking error: {e}")
            await update.message.reply_text("❌ Error showing progress. Please try again.")

    async def show_goals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show goal tracking summary."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get goal summary
            from src.goals.goal_tracker import goal_tracker
            summary = goal_tracker.get_goal_progress_summary(1)  # Assuming user_id = 1
            
            # Format and send message
            message = goal_tracker.format_goal_summary_message(summary, user)
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Goal tracking error: {e}")
            await update.message.reply_text("❌ Error showing goals. Please try again.")

    async def set_goal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set a new goal."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get suggested goals
            from src.goals.goal_tracker import goal_tracker
            suggested_goals = goal_tracker.get_suggested_goals(1)  # Assuming user_id = 1
            
            if not suggested_goals:
                await update.message.reply_text("❌ No suggested goals available. Please try again.")
                return
            
            # Format suggested goals
            message = "🎯 **Suggested Goals:**\n\n"
            for i, goal in enumerate(suggested_goals[:5], 1):
                message += f"{i}. **{goal['goal_type'].title()}:** {goal['goal_description']}\n"
            
            message += "\nUse `/set_goal [goal_number]` to set a goal!"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Set goal error: {e}")
            await update.message.reply_text("❌ Error setting goal. Please try again.")

    async def show_timing(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show personalized timing recommendations."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get personalized timing
            from src.personalization.adaptive_system import adaptive_system
            timing = adaptive_system.get_personalized_timing(1)  # Assuming user_id = 1
            
            # Format timing message
            message = f"""⏰ **Personalized Timing for {user.name}**

**🌅 Best Morning Time:** {timing.get('best_morning_time', '6:00 AM')}
**🌆 Best Evening Time:** {timing.get('best_evening_time', '6:00 PM')}

**⚠️ Avoid Times:** {', '.join(timing.get('avoid_times', ['12:00 PM', '6:00 PM']))}

**🌟 Cosmic Auspicious:** {timing.get('cosmic_auspicious', 'Morning 6-8')}
**⚠️ Cosmic Challenging:** {timing.get('cosmic_challenging', 'Afternoon 12-2')}

**🎯 Recommended Activities:** {', '.join(timing.get('recommended_activities', ['Meditation', 'Family time']))}

Use these timings for best results! ✨"""
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Timing error: {e}")
            await update.message.reply_text("❌ Error showing timing. Please try again.")

    async def show_rituals(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show custom family rituals."""
        if not update.effective_user or not update.message:
            return
            
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get custom rituals
            from src.personalization.adaptive_system import adaptive_system
            rituals = adaptive_system.get_custom_family_rituals(1)  # Assuming user_id = 1
            
            if not rituals:
                await update.message.reply_text("❌ No rituals available. Please try again.")
                return
            
            # Format rituals message
            message = f"""🙏 **Custom Family Rituals for {user.name}**

"""
            for i, ritual in enumerate(rituals, 1):
                message += f"""**{i}. {ritual['name']}**
• **Description:** {ritual['description']}
• **Timing:** {ritual['timing']}
• **Duration:** {ritual['duration']}
• **Benefits:** {', '.join(ritual['benefits'])}

"""
            
            message += "Practice these rituals for family harmony! ✨"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Rituals error: {e}")
            await update.message.reply_text("❌ Error showing rituals. Please try again.")

    async def edit_profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle profile editing with step-by-step approach."""
        if not update.effective_user or not update.message:
            return
        
        user_id = str(update.effective_user.id)
        from src.database.database import DatabaseManager
        db = DatabaseManager()
        existing_user = db.get_user(user_id)
        if not existing_user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        # Get existing user data to pre-fill
        name_parts = existing_user.name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        middle_name = " ".join(name_parts[1:-1]) if len(name_parts) > 2 else ""
        
        # Initialize profile update state with first step and pre-filled data
        self.pending_profile_update[user_id] = {
            "step": "first_name",
            "data": {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "birth_date": existing_user.birth_date,
                "birth_time": existing_user.birth_time,
                "birth_place": existing_user.birth_place,
                "language": existing_user.language_preference
            }
        }
        
        # Start the step-by-step profile update process
        await update.message.reply_text(
            f"✏️ Let's update your profile step by step.\n\n"
            f"Your current first name is: *{first_name}*\n"
            f"Enter your new first name or type 'keep' to keep the current value:", 
            parse_mode='Markdown')

    async def commands_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /commands command."""
        if not update.effective_user or not update.message:
            return
        
        commands_text = """📋 **Complete Commands List** 📋

**🌙 Core Commands:**
/start - Start the bot
/register - Create your profile
/edit_profile - Update your profile
/profile - View your details
/help - Show help guide
/commands - This commands list

**📅 Prediction Commands:**
/daily - Today's cosmic guidance
/weekly - This week's forecast
/monthly - Monthly overview
/yearly - Annual predictions

**🌙 NEW: Moon & Festival Features:**
/moon - Current moon phase guidance
/festivals - Upcoming festivals (30 days)
/auspicious - Auspicious days (14 days)
/health - Health & wellness guidance

**🔮 Advanced Analytics:**
/analytics - Comprehensive astrology analysis
/dasha - Current dasha period information
/transits - Current planetary transits
/yogas - Active yogas in your chart

**🖼️ Voice & Chart Features:**
/chart - Generate your birth chart image
/prediction_image - Get prediction as beautiful image
/voice_prediction - Voice prediction (coming soon)

**🤖 AI-Powered Chat:**
/ai - Advanced AI chat (requires Ollama)
/ai model:prompt - Use specific LLM model
/test_openrouter - Test OpenRouter API connection

**💫 Personal Guidance:**
/personal - Personal life guidance
/family - Family and relationship insights
/health - Health and wellness guidance
/relationships - Love and relationship advice
/spiritual - Spiritual growth guidance
/life_purpose - Life purpose and career guidance

**👨‍👩‍👧‍👦 Family Commands:**
/family_recommendations - Family peace, harmony, health, wealth & happiness
/family_members - View registered family members

**🔮 Consultation Commands:**
/ask [question] - Ask specific questions
/remedies - Personalized remedies

**📊 Optional Enhancement Commands:**
/progress - Track your progress and achievements
/goals - View and manage your goals
/set_goal - Set new family or personal goals
/timing - Get personalized timing recommendations
/rituals - View custom family rituals

**🤖 AI & Learning:**
/adaptive - Get personalized adaptive recommendations

**Examples:**
• `/ai What should I focus on today?`
• `/ai mistral:Give me a health prediction`
• `/moon` - Get moon phase guidance
• `/festivals` - See upcoming festivals
• `/health` - Get wellness guidance

**Natural conversation also works!** Just type anything naturally! 🌟"""
        
        await update.message.reply_text(commands_text)

    async def family_members_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show registered family members."""
        if not update.effective_user or not update.message:
            return
        
        user_id = str(update.effective_user.id)
        user = self._get_user_sync(user_id)
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        
        try:
            # Get family members from database
            from src.database.database import DatabaseManager
            db = DatabaseManager()
            family_members = db.get_family_members()
            
            if not family_members:
                await update.message.reply_text(
                    "👨‍👩‍👧‍👦 **Family Members**\n\n"
                    "No family members registered yet.\n\n"
                    "To add family members, use the registration process.\n"
                    "Each family member should register individually."
                )
                return
            
            # Format family members message
            message = "👨‍👩‍👧‍👦 **Registered Family Members**\n\n"
            
            for i, member in enumerate(family_members, 1):
                message += f"""**{i}. {member.name}**
• **Relationship:** {member.relationship}
• **Birth Date:** {member.birth_date or 'Not set'}
• **Birth Time:** {member.birth_time or 'Not set'}
• **Birth Place:** {member.birth_place or 'Not set'}

"""
            
            message += "Each family member can register individually for personalized guidance! ✨"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Family members error: {e}")
            await update.message.reply_text("❌ Error showing family members. Please try again.")

    async def ai_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ai command for LLM-powered chat via OpenRouter or Ollama."""
        if not update.effective_user or not update.message:
            return
        
        from src.utils.config_simple import get_llm_config
        llm_config = get_llm_config()
        provider = llm_config.provider
        
        prompt = update.message.text[len('/ai'):].strip()
        if not prompt:
            # Show help based on configured provider
            if provider == "openrouter":
                await update.message.reply_text(
                    "🤖 **AI Chat Help**\n\n"
                    "**Usage:**\n"
                    "• `/ai What is my astrological forecast today?`\n"
                    "• `/ai gpt-3.5:Give me a prediction for next week`\n"
                    "• `/ai claude:How can I improve my relationships?`\n\n"
                    "**Available Models:** gpt-3.5, gpt-4, claude, llama, mistral\n\n"
                    "Using OpenRouter for AI chat capabilities."
                )
            else:  # ollama
                await update.message.reply_text(
                    "🤖 **AI Chat Help**\n\n"
                    "**Usage:**\n"
                    "• `/ai What is my astrological forecast today?`\n"
                    "• `/ai mistral:Give me a prediction for next week`\n"
                    "• `/ai llama3:How can I improve my relationships?`\n\n"
                    "**Available Models:** llama3, mistral, codellama, phi3, gemma\n\n"
                    "**Setup Required:** Install Ollama and run `ollama serve` locally."
                )
            return
        
        # Process model selection from prompt
        model = None
        if ':' in prompt:
            model_prefix, prompt_text = prompt.split(':', 1)
            model_prefix = model_prefix.strip().lower()
            prompt = prompt_text.strip()
            
            # Map model prefix to actual model name based on provider
            if provider == "openrouter":
                model_mapping = {
                    'gpt-3.5': 'openai/gpt-3.5-turbo',
                    'gpt-4': 'openai/gpt-4',
                    'claude': 'anthropic/claude-3-haiku',
                    'llama': 'meta-llama/llama-3-8b-instruct',
                    'mistral': 'mistralai/mistral-7b-instruct'
                }
                model = model_mapping.get(model_prefix, llm_config.openrouter_default_model)
            else:  # ollama
                if model_prefix in ['llama3', 'mistral', 'codellama', 'phi3', 'gemma']:
                    model = model_prefix
                else:
                    model = llm_config.ollama_default_model
        
        # Use default model if none specified
        if not model:
            model = llm_config.openrouter_default_model if provider == "openrouter" else llm_config.ollama_default_model
        
        try:
            # Use appropriate client based on provider
            if provider == "openrouter":
                from src.utils.openrouter_client import OpenRouterClient
                
                # Get API key from config
                api_key = llm_config.openrouter_api_key
                if not api_key or not api_key.get_secret_value():
                    await update.message.reply_text(
                        "❌ **OpenRouter API Key Missing**\n\n"
                        "Please set your OpenRouter API key in the environment variables:\n"
                        "```\nLLM_OPENROUTER_API_KEY=your_api_key_here\n```\n\n"
                        "Get your API key at: [openrouter.ai](https://openrouter.ai)"
                    )
                    return
                
                client = OpenRouterClient(api_key=api_key.get_secret_value())
                await update.message.reply_text(f"🤖 Thinking... (using {model} on OpenRouter)")
                
                # Get system prompt from config
                system_prompt = llm_config.system_prompt
                
                response = client.chat(prompt, model=model, system_prompt=system_prompt)
            else:  # ollama
                from src.utils.ollama_client import OllamaClient
                
                client = OllamaClient(host=llm_config.ollama_host)
                await update.message.reply_text(f"🤖 Thinking... (using {model} on Ollama)")
                
                # Get system prompt from config
                system_prompt = llm_config.system_prompt
                
                response = client.chat(prompt, model=model, system_prompt=system_prompt)
            
            if response and response.strip():
                await update.message.reply_text(response)
            else:
                if provider == "openrouter":
                    await update.message.reply_text(
                        "❌ **OpenRouter Error**\n\n"
                        "**Possible Issues:**\n"
                        "• Invalid API key\n"
                        "• Model not available\n"
                        "• Network connection issue\n\n"
                        "**Solutions:**\n"
                        "1. Check your API key\n"
                        "2. Try a different model\n"
                        "3. Check your internet connection\n\n"
                        "**Fallback:** Try our regular commands like `/daily` or `/personal` for guidance!"
                    )
                else:  # ollama
                    await update.message.reply_text(
                        "❌ **Ollama Error**\n\n"
                        "**Possible Issues:**\n"
                        "• Ollama server not running\n"
                        "• Model not downloaded\n"
                        "• Network connection issue\n\n"
                        "**Solutions:**\n"
                        "1. Start Ollama: `ollama serve`\n"
                        "2. Download model: `ollama pull {model}`\n"
                        "3. Check your internet connection\n\n"
                        "**Fallback:** Try our regular commands like `/daily` or `/personal` for guidance!"
                    )
                
        except requests.exceptions.ConnectionError:
            if provider == "openrouter":
                await update.message.reply_text(
                    "❌ **OpenRouter Connection Error**\n\n"
                    "**Could not connect to OpenRouter API.**\n\n"
                    "**To fix this:**\n"
                    "1. Check your internet connection\n"
                    "2. Verify your API key\n"
                    "3. Try again later (service might be down)\n\n"
                    "**For now, try:**\n"
                    "• `/daily` - Daily prediction\n"
                    "• `/personal` - Personal guidance\n"
                    "• `/family` - Family advice\n\n"
                    "Your astrology companion works perfectly without AI chat! ✨"
                )
            else:  # ollama
                await update.message.reply_text(
                    "❌ **Ollama Connection Error**\n\n"
                    "**Ollama server is not running or not accessible.**\n\n"
                    "**To fix this:**\n"
                    "1. Install Ollama: [ollama.ai](https://ollama.ai)\n"
                    "2. Start server: `ollama serve`\n"
                    "3. Download model: `ollama pull {model}`\n\n"
                    "**For now, try:**\n"
                    "• `/daily` - Daily prediction\n"
                    "• `/personal` - Personal guidance\n"
                    "• `/family` - Family advice\n\n"
                    "Your astrology companion works perfectly without AI chat! ✨"
                )
            
        except Exception as e:
            logger.error(f"AI command error: {e}")
            await update.message.reply_text(
                "❌ **AI Chat Error**\n\n"
                f"**Error:** {str(e)}\n\n"
                "**Try these instead:**\n"
                "• `/daily` - Daily cosmic guidance\n"
                "• `/analytics` - Advanced astrology analysis\n"
                "• `/personal` - Personal life guidance\n"
                "• `/family` - Family recommendations\n\n"
                "Your astrology companion is here to help! ✨"
            )

    async def analytics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show comprehensive astrology analytics."""
        if not update.effective_user or not update.message:
            return
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        try:
            from src.astrology.advanced_analytics import advanced_analytics
            user_data = {
                'name': user.name,
                'birth_date': user.birth_date,
                'birth_time': user.birth_time,
                'birth_place': user.birth_place
            }
            analytics = advanced_analytics.get_advanced_prediction(user_data, 'comprehensive')
            if 'error' in analytics:
                await update.message.reply_text("❌ Error generating analytics. Please try again.")
                return
            await update.message.reply_text(analytics['prediction'], parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            await update.message.reply_text("❌ Error showing analytics. Please try again.")

    async def dasha_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current dasha information."""
        if not update.effective_user or not update.message:
            return
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        try:
            from src.astrology.advanced_analytics import advanced_analytics
            dasha_info = advanced_analytics.calculate_dasha(user.birth_date, user.birth_time)
            if 'error' in dasha_info:
                await update.message.reply_text("❌ Error calculating dasha. Please try again.")
                return
            message = f"""🕉️ **Dasha Analysis for {user.name}**

**Current Dasha Lord:** {dasha_info.get('current_dasha', 'Unknown')}
**Years Remaining:** {dasha_info.get('years_remaining', 0):.1f} years
**Dasha Period:** {dasha_info.get('dasha_start', 0):.1f} - {dasha_info.get('dasha_end', 0):.1f} years

**💫 Dasha Guidance:**
Based on your current dasha period, focus on:
• Personal growth and spiritual development
• Family harmony and relationships
• Career advancement and life purpose
• Health and wellness practices

**🌟 Cosmic Blessings:** Your dasha period brings opportunities for growth and success! ✨"""
            await update.message.reply_text(message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Dasha error: {e}")
            await update.message.reply_text("❌ Error showing dasha. Please try again.")

    async def transits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show current planetary transits."""
        if not update.effective_user or not update.message:
            return
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        try:
            from src.astrology.advanced_analytics import advanced_analytics
            transits = advanced_analytics.calculate_transits(user.birth_date, user.birth_time, user.birth_place)
            if 'error' in transits:
                await update.message.reply_text("❌ Error calculating transits. Please try again.")
                return
            message = f"""🌞 **Current Transits for {user.name}**

**Planetary Positions:**
"""
            for planet, data in transits.items():
                if isinstance(data, dict) and 'longitude' in data:
                    message += f"• **{planet}:** {data['longitude']:.1f}°\n"
            message += f"""

**💫 Transit Guidance:**
Current planetary transits influence your:
• Personal energy and mood
• Relationships and communication
• Career and life decisions
• Health and wellness

**🌟 Cosmic Energy:** Use these transits for positive growth and harmony! ✨"""
            await update.message.reply_text(message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Transits error: {e}")
            await update.message.reply_text("❌ Error showing transits. Please try again.")

    async def yogas_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show active yogas in birth chart."""
        if not update.effective_user or not update.message:
            return
        user = self._get_user_sync(str(update.effective_user.id))
        if not user:
            await update.message.reply_text("❌ Please register first using /register")
            return
        try:
            from src.astrology.advanced_analytics import advanced_analytics
            transits = advanced_analytics.calculate_transits(user.birth_date, user.birth_time, user.birth_place)
            yogas = advanced_analytics.detect_yogas(transits)
            if not yogas:
                message = f"""✨ **Yoga Analysis for {user.name}**

**Active Yogas:** No major yogas currently active

**💫 Guidance:** Focus on your natural talents and strengths for personal growth and family harmony! ✨"""
            else:
                message = f"""✨ **Yoga Analysis for {user.name}**

**Active Yogas:**
"""
                for yoga in yogas:
                    message += f"• **{yoga['name']}** ({yoga['strength']}): {yoga['description']}\n"
                message += f"""

**💫 Cosmic Blessings:** These yogas enhance your natural abilities and bring positive energy! ✨"""
            await update.message.reply_text(message, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Yogas error: {e}")
            await update.message.reply_text("❌ Error showing yogas. Please try again.")

    async def moon_phase_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /moon command for moon phase guidance."""
        if not update.effective_user or not update.message:
            return
        
        try:
            from src.astrology.moon_phase_engine import MoonPhaseEngine
            moon_engine = MoonPhaseEngine()
            moon_phase = moon_engine.get_current_moon_phase()
            
            message = f"""🌙 **Moon Phase Guidance** - {datetime.now().strftime('%B %d, %Y')}

**Current Phase:** {moon_phase.phase.replace('_', ' ').title()}
**Illumination:** {moon_phase.illumination:.1%}
**Moon Age:** {moon_phase.age:.1f} days

**Guidance:**
{moon_phase.guidance}

**Recommended Remedies:**
{chr(10).join([f"• {remedy}" for remedy in moon_phase.remedies])}

**Next Full Moon:** {moon_phase.next_full.strftime('%B %d, %Y')}
**Next New Moon:** {moon_phase.next_new.strftime('%B %d, %Y')}

**Use this lunar energy wisely!** 🌙✨"""
            
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Moon phase error: {e}")
            await update.message.reply_text(
                "❌ **Moon Phase Error**\n\n"
                "Sorry, there was an error getting moon phase information.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )
    
    async def festivals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /festivals command for upcoming festivals."""
        if not update.effective_user or not update.message:
            return
        
        try:
            from src.astrology.festival_calendar import FestivalCalendar
            festival_calendar = FestivalCalendar()
            upcoming_festivals = festival_calendar.get_upcoming_festivals(30)
            
            if not upcoming_festivals:
                await update.message.reply_text(
                    "📅 **No Upcoming Festivals**\n\n"
                    "No major festivals in the next 30 days.\n"
                    "Use `/auspicious` to check auspicious days instead!"
                )
                return
            
            message = "📅 **Upcoming Festivals**\n\n"
            
            for festival in upcoming_festivals:
                days_until = (festival.date - datetime.now()).days
                message += f"""🎉 **{festival.name}** - {festival.date.strftime('%B %d, %Y')}
**Days until:** {days_until} days
**Significance:** {festival.significance}

**Quick Rituals:**
{chr(10).join([f"• {ritual}" for ritual in festival.rituals[:2]])}

**Family Activities:**
{chr(10).join([f"• {activity}" for activity in festival.family_activities[:2]])}

---
"""
            
            message += "\n**Use `/festival_details` for complete guidance!** 🙏"
            
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Festivals error: {e}")
            await update.message.reply_text(
                "❌ **Festival Error**\n\n"
                "Sorry, there was an error getting festival information.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )
    
    async def auspicious_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /auspicious command for auspicious days."""
        if not update.effective_user or not update.message:
            return
        
        try:
            from src.astrology.festival_calendar import FestivalCalendar
            festival_calendar = FestivalCalendar()
            auspicious_days = festival_calendar.get_auspicious_days(datetime.now(), 14)
            
            if not auspicious_days:
                await update.message.reply_text(
                    "📅 **Auspicious Days**\n\n"
                    "No highly auspicious days in the next 14 days.\n"
                    "Every day has its own blessings! 🙏"
                )
                return
            
            message = "📅 **Auspicious Days (Next 14 Days)**\n\n"
            
            for day in auspicious_days:
                message += f"""✨ **{day['date']}** - {day['day_name']}
**Reason:** {day['reason']}

**Recommended Activities:**
{chr(10).join([f"• {activity}" for activity in day['activities']])}

---
"""
            
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Auspicious days error: {e}")
            await update.message.reply_text(
                "❌ **Auspicious Days Error**\n\n"
                "Sorry, there was an error getting auspicious days.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )
    
    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /health command for health and wellness guidance."""
        if not update.effective_user or not update.message:
            return
        
        try:
            from src.astrology.health_wellness_engine import HealthWellnessEngine
            health_engine = HealthWellnessEngine()
            
            # Get user for birth time
            user = self._get_user_sync(update.effective_user.id)
            if not user:
                await update.message.reply_text(
                    "❌ **Health Guidance Error**\n\n"
                    "Please register first with `/register` to get personalized health guidance."
                )
                return
            
            # Get seasonal health tips
            seasonal_tips = health_engine.get_seasonal_health_tips()
            current_season = seasonal_tips['en']
            
            # Get exercise timing
            exercise_timing = health_engine.get_exercise_timing(user.birth_time)
            
            # Get daily routine
            daily_routine = health_engine.get_daily_health_routine()
            
            message = f"""🌿 **Health & Wellness Guidance** - {datetime.now().strftime('%B %d, %Y')}

**Current Season:** {current_season['name']}
**Dosha Focus:** {current_season['dosha']}
**Description:** {current_season['description']}

**Seasonal Diet:**
{chr(10).join([f"• {item}" for item in current_season['diet'][:3]])}

**Lifestyle Tips:**
{chr(10).join([f"• {item}" for item in current_season['lifestyle'][:3]])}

**Best Exercise Time:** {exercise_timing['best_time']}
**Exercise Type:** {exercise_timing['exercise_type']}

**Daily Health Routine:**
**Morning:** {daily_routine['morning'][0]}
**Afternoon:** {daily_routine['afternoon'][0]}
**Evening:** {daily_routine['evening'][0]}
**Night:** {daily_routine['night'][0]}

**Use `/health_details` for complete wellness guide!** 🌿✨"""
            
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Health guidance error: {e}")
            await update.message.reply_text(
                "❌ **Health Guidance Error**\n\n"
                "Sorry, there was an error getting health guidance.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )
    
    async def chart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /chart command for birth chart image generation."""
        if not update.effective_user or not update.message:
            return
        
        try:
            user = self._get_user_sync(update.effective_user.id)
            if not user:
                await update.message.reply_text(
                    "❌ **Chart Generation Error**\n\n"
                    "Please register first with `/register` to generate your birth chart."
                )
                return
            
            await update.message.reply_text(
                "🖼️ **Birth Chart Generation**\n\n"
                "Generating your birth chart image...\n\n"
                "**Coming Soon:**\n"
                "• Beautiful birth chart visualization\n"
                "• Planetary positions and aspects\n"
                "• Zodiac signs and houses\n\n"
                "For now, use `/daily` for your personalized guidance! ✨"
            )
            
        except Exception as e:
            logger.error(f"Chart generation error: {e}")
            await update.message.reply_text(
                "❌ **Chart Generation Error**\n\n"
                "Sorry, there was an error generating your birth chart.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )
    
    async def prediction_image_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /prediction_image command for prediction image generation."""
        if not update.effective_user or not update.message:
            return
        
        try:
            user = self._get_user_sync(update.effective_user.id)
            if not user:
                await update.message.reply_text(
                    "❌ **Prediction Image Error**\n\n"
                    "Please register first with `/register` to get prediction images."
                )
                return
            
            await update.message.reply_text(
                "🖼️ **Prediction Image Generation**\n\n"
                "Generating your prediction image...\n\n"
                "**Coming Soon:**\n"
                "• Beautiful prediction graphics\n"
                "• Styled cosmic guidance\n"
                "• Visual astrology insights\n\n"
                "For now, use `/daily` for your personalized guidance! ✨"
            )
            
        except Exception as e:
            logger.error(f"Prediction image error: {e}")
            await update.message.reply_text(
                "❌ **Prediction Image Error**\n\n"
                "Sorry, there was an error generating your prediction image.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )
    
    async def voice_prediction_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /voice_prediction command for voice prediction."""
        if not update.effective_user or not update.message:
            return
        
        try:
            user = self._get_user_sync(update.effective_user.id)
            if not user:
                await update.message.reply_text(
                    "❌ **Voice Prediction Error**\n\n"
                    "Please register first with `/register` to get voice predictions."
                )
                return
            
            await update.message.reply_text(
                "🎤 **Voice Prediction**\n\n"
                "Generating your voice prediction...\n\n"
                "**Coming Soon:**\n"
                "• Text-to-speech predictions\n"
                "• Audio cosmic guidance\n"
                "• Voice-based insights\n\n"
                "For now, use `/daily` for your personalized guidance! ✨"
            )
            
        except Exception as e:
            logger.error(f"Voice prediction error: {e}")
            await update.message.reply_text(
                "❌ **Voice Prediction Error**\n\n"
                "Sorry, there was an error generating your voice prediction.\n"
                "Please try again later or use other commands like `/daily` for guidance."
            )

    def run_sync(self):
        """Run the bot synchronously."""
        try:
            # Use the built-in run_polling method (sync version) with conflict prevention
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise

    async def test_openrouter_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /test_openrouter command to test OpenRouter API connection."""
        if not update.effective_user or not update.message:
            return
            
        # Check if user is admin (optional security measure)
        user_id = str(update.effective_user.id)
        # You can implement admin check here if needed
        
        await update.message.reply_text("🔄 Testing OpenRouter API connection...")
        
        try:
            from src.utils.config_simple import get_llm_config
            from src.utils.openrouter_client import OpenRouterClient
            
            llm_config = get_llm_config()
            
            # Check if OpenRouter is configured as the provider
            if llm_config.provider != "openrouter":
                await update.message.reply_text(
                    "❌ **OpenRouter Test Failed**\n\n"
                    f"Current LLM provider is set to '{llm_config.provider}', not 'openrouter'.\n"
                    "Please update your configuration to use OpenRouter."
                )
                return
                
            # Check if API key is configured
            if not llm_config.openrouter_api_key:
                await update.message.reply_text(
                    "❌ **OpenRouter Test Failed**\n\n"
                    "OpenRouter API key is not configured.\n"
                    "Please set the LLM_OPENROUTER_API_KEY environment variable."
                )
                return
                
            # Create OpenRouter client and test connection
            client = OpenRouterClient(llm_config.openrouter_api_key.get_secret_value())
            success, message = client.test_connection()
            
            if success:
                await update.message.reply_text(
                    "✅ **OpenRouter Connection Successful**\n\n"
                    f"{message}\n\n"
                    "You can now use the /ai command for AI-powered chat."
                )
            else:
                await update.message.reply_text(
                    "❌ **OpenRouter Test Failed**\n\n"
                    f"Error: {message}\n\n"
                    "Please check your API key and try again."
                )
                
        except Exception as e:
            logger.error(f"OpenRouter test error: {e}")
            await update.message.reply_text(
                "❌ **OpenRouter Test Error**\n\n"
                f"An unexpected error occurred: {str(e)}\n"
                "Please check your configuration and try again."
            )
    
    async def run(self):
        """Run the bot asynchronously."""
        try:
            # Use the built-in run_polling method (async version) with conflict prevention
            await self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                close_loop=False
            )
        except Exception as e:
            logger.error(f"Error running bot: {e}")
            raise
        finally:
            # Cleanup
            await self.application.stop()
            await self.application.shutdown()


# Global bot instance
bot = SimpleAstroBot()