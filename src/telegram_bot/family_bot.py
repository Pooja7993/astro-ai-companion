"""
Family Telegram Bot - Natural Chat Interface
Each family member has their own chat experience
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from sqlalchemy.orm import Session
from loguru import logger

from src.config.database import get_db
from src.models.user_models import User, Family, BirthChart, Prediction
from src.services.astrology_service import astrology_service
from src.services.openrouter_service import openrouter_service

class FamilyTelegramBot:
    """Telegram bot for family astrology guidance."""
    
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("register", self.register_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("family", self.family_command))
        self.application.add_handler(CommandHandler("guidance", self.guidance_command))
        
        # Callback query handler for buttons
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Message handler for natural chat
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        
        # Check if user exists
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if user:
            message = f"""🌟 Welcome back, {user.full_name}!
            
I'm your personal astrology companion. I provide unified guidance combining:
• Vedic Astrology 🔮
• Numerology 🔢  
• Lal Kitab 📚

How can I help you today? Just chat with me naturally or use the menu below."""
        else:
            message = """🌟 Welcome to Astro AI Companion!

I'm your personal family astrology guide. I combine Vedic astrology, numerology, and Lal Kitab to provide unified guidance for you and your family.

Each family member gets their own personalized chat experience!

To get started, please register your profile."""
        
        # Create inline keyboard
        keyboard = [
            [InlineKeyboardButton("📝 Register Profile", callback_data="register")],
            [InlineKeyboardButton("🔮 Daily Guidance", callback_data="daily_guidance")],
            [InlineKeyboardButton("👨‍👩‍👧‍👦 Family Overview", callback_data="family_overview")],
            [InlineKeyboardButton("📊 My Profile", callback_data="my_profile")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)
    
    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /register command."""
        message = """📝 **Family Member Registration**

Please provide your details in this format:
`FirstName|MiddleName|LastName|YYYY-MM-DD|HH:MM|City,Country|Relationship`

**Example:**
`John|Kumar|Sharma|1990-05-15|14:30|Mumbai,India|head`

**Relationships:** head, spouse, child, parent, sibling, other

This creates your personal astrological profile with unified guidance from Vedic astrology, numerology, and Lal Kitab."""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle natural language messages."""
        user_id = str(update.effective_user.id)
        message_text = update.message.text
        
        # Check if this is registration data
        if '|' in message_text and len(message_text.split('|')) >= 6:
            await self.process_registration(update, context)
            return
        
        # Check if user is registered
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await update.message.reply_text(
                "Please register first using /register to get personalized guidance!"
            )
            return
        
        # Generate AI response based on user's astrological profile
        await self.generate_personalized_response(update, context, user, message_text)
    
    async def process_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process user registration."""
        try:
            user_id = str(update.effective_user.id)
            chat_id = str(update.effective_chat.id)
            data = update.message.text.split('|')
            
            if len(data) < 6:
                await update.message.reply_text(
                    "❌ Please provide all required information in the correct format."
                )
                return
            
            first_name = data[0].strip()
            middle_name = data[1].strip() if data[1].strip() else None
            last_name = data[2].strip()
            birth_date = data[3].strip()
            birth_time = data[4].strip()
            birth_place = data[5].strip()
            relationship = data[6].strip() if len(data) > 6 else "member"
            
            # Validate date format
            try:
                datetime.strptime(birth_date, "%Y-%m-%d")
                datetime.strptime(birth_time, "%H:%M")
            except ValueError:
                await update.message.reply_text(
                    "❌ Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."
                )
                return
            
            db = next(get_db())
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.telegram_id == user_id).first()
            if existing_user:
                await update.message.reply_text("You are already registered!")
                return
            
            # Create new user
            new_user = User(
                telegram_id=user_id,
                telegram_chat_id=chat_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                birth_date=birth_date,
                birth_time=birth_time,
                birth_place=birth_place,
                relationship_to_head=relationship
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Calculate birth chart
            await self.calculate_and_store_birth_chart(new_user, db)
            
            await update.message.reply_text(
                f"✅ Welcome {new_user.full_name}! Your astrological profile has been created.\n\n"
                "I'm now calculating your unified guidance combining Vedic astrology, numerology, and Lal Kitab.\n\n"
                "You can now chat with me naturally for personalized guidance!"
            )
            
        except Exception as e:
            logger.error(f"Error processing registration: {e}")
            await update.message.reply_text(
                "❌ There was an error creating your profile. Please try again."
            )
    
    async def calculate_and_store_birth_chart(self, user: User, db: Session):
        """Calculate and store birth chart data."""
        try:
            # For demo, using default coordinates (Mumbai)
            latitude = 19.0760
            longitude = 72.8777
            
            # Calculate birth chart
            birth_chart = astrology_service.calculate_birth_chart(
                user.birth_date, user.birth_time, user.birth_place, latitude, longitude
            )
            
            # Calculate numerology
            numerology = astrology_service.calculate_numerology(
                user.birth_date, user.full_name
            )
            
            # Generate Lal Kitab analysis
            lal_kitab = astrology_service.generate_lal_kitab_analysis(birth_chart)
            
            # Store in database
            chart_record = BirthChart(
                user_id=user.id,
                sun_sign=birth_chart.get('planets', {}).get('Sun', {}).get('sign'),
                moon_sign=birth_chart.get('planets', {}).get('Moon', {}).get('sign'),
                ascendant=birth_chart.get('ascendant'),
                nakshatra=birth_chart.get('nakshatra', {}).get('name'),
                planetary_positions=str(birth_chart.get('planets', {})),
                house_positions=str(birth_chart.get('houses', {})),
                aspects=str(birth_chart.get('aspects', [])),
                life_path_number=numerology.get('life_path_number'),
                destiny_number=numerology.get('destiny_number'),
                soul_number=numerology.get('soul_number'),
                lal_kitab_analysis=str(lal_kitab)
            )
            
            db.add(chart_record)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error calculating birth chart: {e}")
    
    async def generate_personalized_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                           user: User, message_text: str):
        """Generate personalized AI response."""
        try:
            db = next(get_db())
            birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user.id).first()
            
            if not birth_chart:
                await update.message.reply_text(
                    "Let me calculate your astrological profile first. This may take a moment..."
                )
                await self.calculate_and_store_birth_chart(user, db)
                birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user.id).first()
            
            # Prepare astrological context
            context_data = f"""
            User: {user.full_name}
            Sun Sign: {birth_chart.sun_sign}
            Moon Sign: {birth_chart.moon_sign}
            Ascendant: {birth_chart.ascendant}
            Nakshatra: {birth_chart.nakshatra}
            Life Path Number: {birth_chart.life_path_number}
            Destiny Number: {birth_chart.destiny_number}
            Soul Number: {birth_chart.soul_number}
            """
            
            system_prompt = f"""You are a personal astrology companion for {user.full_name}. 
            You combine Vedic astrology, numerology, and Lal Kitab to provide personalized guidance.
            
            User's Astrological Profile:
            {context_data}
            
            Respond naturally and conversationally. Provide practical, positive guidance that integrates 
            insights from all three systems. Keep responses concise but meaningful (100-200 words).
            Always be supportive and encouraging."""
            
            response = await openrouter_service.generate_response(
                message_text, system_prompt
            )
            
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Error generating personalized response: {e}")
            await update.message.reply_text(
                "I'm having trouble accessing your astrological data right now. Please try again in a moment."
            )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "register":
            await self.register_command(update, context)
        elif query.data == "daily_guidance":
            await self.daily_guidance_callback(update, context)
        elif query.data == "family_overview":
            await self.family_overview_callback(update, context)
        elif query.data == "my_profile":
            await self.profile_callback(update, context)
    
    async def daily_guidance_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle daily guidance callback."""
        user_id = str(update.effective_user.id)
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await update.callback_query.edit_message_text(
                "Please register first to get personalized guidance!"
            )
            return
        
        # Generate daily guidance
        await update.callback_query.edit_message_text(
            "🔮 Generating your personalized daily guidance...\n\n"
            "This combines insights from Vedic astrology, numerology, and Lal Kitab specifically for you."
        )
        
        # Get birth chart
        birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user.id).first()
        
        if birth_chart:
            # Generate unified guidance
            guidance = await astrology_service.generate_unified_guidance(
                user.__dict__, 
                eval(birth_chart.planetary_positions) if birth_chart.planetary_positions else {},
                {
                    'life_path_number': birth_chart.life_path_number,
                    'destiny_number': birth_chart.destiny_number,
                    'soul_number': birth_chart.soul_number
                },
                eval(birth_chart.lal_kitab_analysis) if birth_chart.lal_kitab_analysis else {},
                "daily"
            )
            
            await update.callback_query.edit_message_text(
                f"🌟 **Daily Guidance for {user.full_name}**\n\n{guidance}"
            )
        else:
            await update.callback_query.edit_message_text(
                "Let me calculate your astrological profile first. Please use /register to complete your setup."
            )
    
    async def family_overview_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle family overview callback."""
        user_id = str(update.effective_user.id)
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await update.callback_query.edit_message_text(
                "Please register first!"
            )
            return
        
        # Get family members
        family_members = db.query(User).filter(User.family_id == user.family_id).all() if user.family_id else [user]
        
        message = f"👨‍👩‍👧‍👦 **Family Overview**\n\n"
        for member in family_members:
            birth_chart = db.query(BirthChart).filter(BirthChart.user_id == member.id).first()
            sun_sign = birth_chart.sun_sign if birth_chart else "Unknown"
            message += f"• **{member.full_name}** ({member.relationship_to_head})\n"
            message += f"  Sun Sign: {sun_sign}\n\n"
        
        message += "Each family member has their own personalized chat experience with unified astrological guidance!"
        
        await update.callback_query.edit_message_text(message)
    
    async def profile_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle profile callback."""
        user_id = str(update.effective_user.id)
        db = next(get_db())
        user = db.query(User).filter(User.telegram_id == user_id).first()
        
        if not user:
            await update.callback_query.edit_message_text(
                "Please register first!"
            )
            return
        
        birth_chart = db.query(BirthChart).filter(BirthChart.user_id == user.id).first()
        
        message = f"📊 **Your Astrological Profile**\n\n"
        message += f"**Name:** {user.full_name}\n"
        message += f"**Birth:** {user.birth_date} at {user.birth_time}\n"
        message += f"**Place:** {user.birth_place}\n\n"
        
        if birth_chart:
            message += f"**Vedic Astrology:**\n"
            message += f"• Sun Sign: {birth_chart.sun_sign}\n"
            message += f"• Moon Sign: {birth_chart.moon_sign}\n"
            message += f"• Ascendant: {birth_chart.ascendant}\n"
            message += f"• Nakshatra: {birth_chart.nakshatra}\n\n"
            
            message += f"**Numerology:**\n"
            message += f"• Life Path: {birth_chart.life_path_number}\n"
            message += f"• Destiny: {birth_chart.destiny_number}\n"
            message += f"• Soul: {birth_chart.soul_number}\n\n"
            
            message += "Your guidance combines all these systems for unified insights!"
        else:
            message += "Calculating your astrological data..."
        
        await update.callback_query.edit_message_text(message)
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command."""
        await self.profile_callback(update, context)
    
    async def family_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /family command."""
        await self.family_overview_callback(update, context)
    
    async def guidance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /guidance command."""
        await self.daily_guidance_callback(update, context)
    
    def run(self):
        """Run the bot."""
        logger.info("Starting Family Telegram Bot...")
        self.application.run_polling()

# Global bot instance
family_bot = None