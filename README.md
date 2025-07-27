# 🌟 Personal Family Astro AI Companion

A **personal family astrology companion** designed specifically for you and your family. This system provides real astrology calculations, personalized predictions, and family guidance in a simple, private environment.

## ✨ Features

### **🔮 Core Astrology Engine**
- **Real Swiss Ephemeris calculations** - NASA-grade astrological accuracy
- **Birth chart analysis** - Complete planetary positions and aspects
- **Personalized predictions** - Daily, weekly, monthly, yearly guidance
- **Multi-language support** - English and Marathi

### **👨‍👩‍👧‍👦 Family Features**
- **Simple family recommendations** - 1 remedy + warnings only
- **Individual family member access** - Each member gets personal Telegram access
- **Family compatibility analysis** - Relationship insights and guidance
- **Personalized language** - Each member chooses English or Marathi

### **📊 Optional Enhancements**
- **Daily reminders system** - Automatic daily messages
- **Progress tracking** - Track mood, harmony, health, spiritual growth
- **Goal setting & tracking** - Set and achieve family and personal goals
- **Advanced personalization** - Learns and adapts to your preferences
- **Enhanced notifications** - Smart alerts for important events

## 🚀 Quick Start

### **1. Setup**
```bash
# Install dependencies
pip install -r requirements_simple.txt

# Set your Telegram bot token
cp env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN
```

### **2. Run the Bot**
```bash
python run_simple.py
```

### **3. Register and Use**
1. Start a chat with your bot on Telegram
2. Use `/register` to create your profile
3. Use `/family_recommendations` for daily family guidance
4. Explore other commands for personalized features

## 📱 Available Commands

### **Core Commands**
- `/start` - Welcome and setup
- `/register` - Create your profile
- `/help` - Show all available commands

### **Predictions**
- `/daily` - Daily predictions
- `/weekly` - Weekly forecasts
- `/monthly` - Monthly analysis
- `/yearly` - Yearly predictions

### **Personal Guidance**
- `/personal` - Personal guidance
- `/family` - Family guidance
- `/health` - Health and wellness
- `/relationships` - Relationship advice
- `/spiritual` - Spiritual growth
- `/life_purpose` - Life purpose analysis

### **Family Features**
- `/family_recommendations` - Simple family recommendations (1 remedy + warnings)
- `/remedies` - Personalized remedies
- `/ask [question]` - Ask specific questions

### **Optional Enhancements**
- `/progress` - View your progress tracking
- `/goals` - Manage your goals
- `/set_goal` - Set new goals
- `/timing` - Get personalized timing
- `/rituals` - View custom family rituals

## 🏗️ System Architecture

### **Core Components**
```
src/
├── astrology/           # Real astrology calculations
│   ├── real_astrology_engine.py
│   ├── chart_analyzer.py
│   ├── prediction_generator.py
│   └── remedy_engine.py
├── database/           # User and family data
│   ├── database.py
│   └── models.py
├── family/            # Family management
│   ├── family_manager.py
│   ├── family_recommendations.py
│   └── family_telegram_manager.py
├── telegram_bot/      # Main bot interface
│   └── bot_simple.py
└── utils/             # Utilities
    ├── config.py
    ├── logging_setup.py
    ├── multi_language.py
    └── error_handler.py
```

### **Optional Enhancements**
```
src/
├── scheduler/         # Daily reminders
│   └── daily_reminders.py
├── tracking/          # Progress tracking
│   └── progress_tracker.py
├── personalization/   # Advanced personalization
│   └── adaptive_system.py
├── goals/            # Goal setting & tracking
│   └── goal_tracker.py
└── notifications/    # Enhanced notifications
    └── enhanced_notifications.py
```

## 🔧 Configuration

### **Environment Variables**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### **Database**
- **SQLite database** - Stored in `data/astro_companion.db`
- **User profiles** - Personal information and preferences
- **Family members** - Family member data and relationships
- **Predictions** - Stored predictions and guidance
- **Progress tracking** - Mood, harmony, health, spiritual data

## 📊 Data Privacy

- **Personal use only** - Designed for your family
- **Local database** - All data stored locally
- **No external sharing** - Your data stays private
- **Family-focused** - All features designed for family harmony

## 🎯 Family Recommendations

The system provides **simple, focused family recommendations**:

- **1 remedy per day** - Simple, actionable advice
- **Warnings only when needed** - No unnecessary alerts
- **English only** - Clean, simple language
- **Only you receive** - Personal delivery to your Telegram

Example output:
```
🌟 Family Recommendations for [Your Name]

🔮 Today's Remedy:
Light a candle and meditate for 10 minutes with family

⚠️ Warnings:
• No major warnings today - good day for family activities

🎯 Today's Focus: Family Harmony and Peace
⏰ Best Timing: Morning 6-8 and Evening 6-8

Peace and harmony for your family! ✨
```

## 🌟 Benefits

### **✅ Simple & Practical**
- **Easy to use** - Simple commands and clear guidance
- **Real astrology** - NASA-grade calculations for accuracy
- **Family-focused** - All features designed for family harmony
- **Personal privacy** - Your data stays with you

### **✅ Comprehensive Features**
- **Real predictions** - Based on actual birth chart data
- **Multi-language** - English and Marathi support
- **Individual access** - Each family member gets personal access
- **Progress tracking** - Monitor improvements over time

### **✅ Optional Enhancements**
- **Daily reminders** - Automatic daily guidance
- **Goal tracking** - Set and achieve family goals
- **Personalization** - Learns from your preferences
- **Smart notifications** - Important event alerts

## 🎉 Getting Started

1. **Setup your bot** - Follow the setup instructions above
2. **Register your profile** - Use `/register` in Telegram
3. **Get daily guidance** - Use `/family_recommendations`
4. **Explore features** - Try other commands for personalized guidance
5. **Add family members** - Register each family member individually

**Your personal family astrology companion is ready to bring peace, harmony, health, wealth, and happiness to your family!** 🌟✨

---

**Note:** This system is designed for **personal family use only**. All features are focused on bringing peace, harmony, and well-being to your family through authentic astrology guidance.
