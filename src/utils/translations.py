"""
Translation utilities for multi-language support
"""

import yaml
from pathlib import Path
from typing import Dict, Any

translations_path = Path("config/languages/translations.yaml")
with open(translations_path, 'r', encoding='utf-8') as f:
    TRANSLATIONS = yaml.safe_load(f)

def get_translation(key: str, language: str = 'en') -> str:
    """Get translation for a key in specified language."""
    
    translation_map = {
        'welcome_back': {
            'en': "Welcome back, {name}! 🌟",
            'mr': "परत स्वागत आहे, {name}! 🌟"
        },
        'welcome_new': {
            'en': "Welcome to Astro AI Companion! 🌟\nYour personalized astrology guide.",
            'mr': "ज्योतिष AI साथीदारामध्ये आपले स्वागत आहे! 🌟\nआपला वैयक्तिक ज्योतिष मार्गदर्शक."
        },
        'register_prompt': {
            'en': "To get started, please register your profile using /register command.",
            'mr': "/register कमांड वापरून आपली प्रोफाइल नोंदवा."
        },
        'registration_start': {
            'en': "Let's create your astrological profile! ✨",
            'mr': "चला आपली ज्योतिषीय प्रोफाइल तयार करूया! ✨"
        },
        'ask_name': {
            'en': "Please enter your full name:",
            'mr': "कृपया आपले पूर्ण नाव टाका:"
        },
        'ask_dob': {
            'en': "Please enter your date of birth (DD/MM/YYYY):",
            'mr': "कृपया आपली जन्मतारीख टाका (DD/MM/YYYY):"
        },
        'ask_tob': {
            'en': "Please enter your time of birth (HH:MM in 24-hour format):",
            'mr': "कृपया आपला जन्मवेळ टाका (HH:MM 24-तास स्वरूपात):"
        },
        'ask_location': {
            'en': "Please enter your birth location (City, Country):",
            'mr': "कृपया आपले जन्मस्थान टाका (शहर, देश):"
        },
        'ask_language': {
            'en': "Please select your preferred language:",
            'mr': "कृपया आपली पसंतीची भाषा निवडा:"
        },
        'profile_created': {
            'en': "Your profile has been created successfully! ✨\nYou can now get personalized predictions and remedies.",
            'mr': "आपली प्रोफाइल यशस्वीरित्या तयार झाली आहे! ✨\nआता आपण वैयक्तिक भविष्यवाणी आणि उपाय मिळवू शकता."
        },
        'registration_cancelled': {
            'en': "Registration cancelled. You can start again with /register command.",
            'mr': "नोंदणी रद्द केली. आपण /register कमांडसह पुन्हा सुरुवात करू शकता."
        },
        'registration_error': {
            'en': "Sorry, there was an error creating your profile. Please try again.",
            'mr': "माफ करा, आपली प्रोफाइल तयार करताना त्रुटी झाली. कृपया पुन्हा प्रयत्न करा."
        },
        'invalid_date': {
            'en': "Invalid date format. Please use DD/MM/YYYY format (e.g., 15/08/1990).",
            'mr': "अवैध तारीख स्वरूप. कृपया DD/MM/YYYY स्वरूप वापरा (उदा., 15/08/1990)."
        },
        'invalid_time': {
            'en': "Invalid time format. Please use HH:MM format (e.g., 14:30).",
            'mr': "अवैध वेळ स्वरूप. कृपया HH:MM स्वरूप वापरा (उदा., 14:30)."
        },
        'main_menu': {
            'en': "🌟 Main Menu 🌟\nSelect an option below:",
            'mr': "🌟 मुख्य मेनू 🌟\nखाली एक पर्याय निवडा:"
        },
        'daily_prediction': {
            'en': "📅 Daily Prediction",
            'mr': "📅 दैनिक भविष्यवाणी"
        },
        'weekly_prediction': {
            'en': "📊 Weekly Forecast",
            'mr': "📊 साप्ताहिक अंदाज"
        },
        'monthly_prediction': {
            'en': "📈 Monthly Overview",
            'mr': "📈 मासिक विहंगावलोकन"
        },
        'remedies': {
            'en': "🔮 Remedies",
            'mr': "🔮 उपाय"
        },
        'profile': {
            'en': "👤 Profile",
            'mr': "👤 प्रोफाइल"
        },
        'not_registered': {
            'en': "You are not registered yet. Please use /register command to create your profile.",
            'mr': "आपण अजून नोंदणीकृत नाही. कृपया आपली प्रोफाइल तयार करण्यासाठी /register कमांड वापरा."
        },
        'prediction_error': {
            'en': "Sorry, there was an error generating your prediction. Please try again later.",
            'mr': "माफ करा, आपली भविष्यवाणी तयार करताना त्रुटी झाली. कृपया नंतर पुन्हा प्रयत्न करा."
        },
        'remedies_error': {
            'en': "Sorry, there was an error generating your remedies. Please try again later.",
            'mr': "माफ करा, आपले उपाय तयार करताना त्रुटी झाली. कृपया नंतर पुन्हा प्रयत्न करा."
        },
        'change_language': {
            'en': "Please select your preferred language:",
            'mr': "कृपया आपली पसंतीची भाषा निवडा:"
        },
        'help_text': {
            'en': """🌟 *Astro AI Companion Help* 🌟

*Available Commands:*
/start - Start the bot
/register - Register your profile
/daily - Get daily prediction
/weekly - Get weekly forecast
/monthly - Get monthly overview
/remedies - Get personalized remedies
/profile - View your profile
/language - Change language
/help - Show this help

*Features:*
• Personalized Vedic astrology predictions
• Daily, weekly, and monthly forecasts
• Customized remedies and suggestions
• Master remedies for major life improvements
• Support for English and Marathi languages
• Completely offline and private

*How to use:*
1. Register with /register command
2. Provide your birth details
3. Get daily predictions automatically
4. Use menu buttons for easy navigation

For support, contact the administrator.""",
            'mr': """🌟 *ज्योतिष AI साथीदार मदत* 🌟

*उपलब्ध कमांड्स:*
/start - बॉट सुरू करा
/register - आपली प्रोफाइल नोंदवा
/daily - दैनिक भविष्यवाणी मिळवा
/weekly - साप्ताहिक अंदाज मिळवा
/monthly - मासिक विहंगावलोकन मिळवा
/remedies - वैयक्तिक उपाय मिळवा
/profile - आपली प्रोफाइल पहा
/language - भाषा बदला
/help - ही मदत दाखवा

*वैशिष्ट्ये:*
• वैयक्तिक वैदिक ज्योतिष भविष्यवाणी
• दैनिक, साप्ताहिक आणि मासिक अंदाज
• सानुकूलित उपाय आणि सूचना
• मुख्य जीवन सुधारणांसाठी मास्टर उपाय
• इंग्रजी आणि मराठी भाषांचा आधार
• पूर्णपणे ऑफलाइन आणि खाजगी

*कसे वापरावे:*
1. /register कमांडसह नोंदणी करा
2. आपले जन्म तपशील द्या
3. आपोआप दैनिक भविष्यवाणी मिळवा
4. सुलभ नेव्हिगेशनसाठी मेनू बटणे वापरा

समर्थनासाठी, प्रशासकाशी संपर्क साधा."""
        },
        'daily_greeting': {
            'en': "🌅 Good morning! Here's your daily astrological insight:",
            'mr': "🌅 सुप्रभात! आजचा आपला ज्योतिषीय अंतर्दृष्टी:"
        },
        'default_response': {
            'en': "I didn't understand that. Please use the menu buttons or /help for available commands.",
            'mr': "मला ते समजले नाही. कृपया मेनू बटणे किंवा उपलब्ध कमांड्ससाठी /help वापरा."
        }
    }
    
    if key in translation_map:
        return translation_map[key].get(language, translation_map[key]['en'])
    
    try:
        if language == 'mr':
            return TRANSLATIONS.get('marathi', {}).get(key, key)
        else:
            return TRANSLATIONS.get('english', {}).get(key, key)
    except:
        return key
