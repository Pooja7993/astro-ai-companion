# 🌟 Astro AI Companion - Personal Family Edition

**Your personal family astrology companion for peace, harmony, health, wealth, and happiness!**

## ✨ **Features**

### **🎯 Core Astrology Features:**
- **Birth Chart Analysis** - Personalized planetary positions and zodiac signs
- **Daily Predictions** - Cosmic insights for your day
- **Family Recommendations** - Simple remedies and warnings for family harmony
- **Multi-language Support** - English and Marathi
- **Personal Guidance** - Health, relationships, spiritual growth, life purpose

### **👨‍👩‍👧‍👦 Family Features:**
- **Family Member Management** - Add and manage family members
- **Individual Telegram Access** - Each family member gets personal guidance
- **Family Compatibility** - Analyze relationships and harmony
- **Simple Recommendations** - One remedy and warnings for peace

### **🚀 Optional Enhancements:**
- **Daily Reminders** - Automated morning and evening guidance
- **Progress Tracking** - Track mood, harmony, health, spiritual growth
- **Goal Setting** - Set and track personal and family goals
- **Advanced Personalization** - Learns from your feedback
- **Enhanced Notifications** - Smart alerts for important events

## 🛠️ **Quick Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/Pooja7993/astro-ai-companion.git
cd astro-ai-companion
```

### **2. Install Dependencies**
```bash
pip install -r requirements_simple.txt
```

### **3. Set Environment Variables**
Create a `.env` file:
```env
telegram_bot_token=your_bot_token_here
telegram_chat_id=5929651379
```

### **4. Run Locally**
```bash
python run_simple.py
```

## 🚀 **Deploy to Render**

### **1. Create Render Account**
- Go to [render.com](https://render.com)
- Sign up with GitHub

### **2. Create Web Service**
- Click "New +" → "Web Service"
- Connect to your GitHub repository
- Set build command: `pip install -r requirements_simple.txt`
- Set start command: `python run_simple.py`

### **3. Set Environment Variables**
In Render dashboard, add:
- `telegram_bot_token=your_bot_token_here`
- `telegram_chat_id=5929651379`

### **4. Deploy**
- Click "Create Web Service"
- Monitor deployment logs
- Test your bot on Telegram

## 📱 **Bot Commands**

### **Basic Commands:**
- `/start` - Welcome message
- `/help` - Show all commands
- `/register` - Create your profile
- `/profile` - View your details

### **Predictions:**
- `/daily` - Daily prediction
- `/weekly` - Weekly forecast
- `/monthly` - Monthly insights
- `/yearly` - Yearly guidance

### **Personal Guidance:**
- `/personal` - Personal guidance
- `/family` - Family recommendations
- `/health` - Health guidance
- `/relationships` - Relationship advice
- `/spiritual` - Spiritual growth
- `/life_purpose` - Life purpose discovery

### **Optional Features:**
- `/progress` - Track your progress
- `/goals` - Set and view goals
- `/timing` - Best timing for activities
- `/rituals` - Custom family rituals

## 🏗️ **Project Structure**

```
astro-ai-companion/
├── run_simple.py              # Main entry point
├── requirements_simple.txt     # Dependencies
├── src/
│   ├── telegram_bot/
│   │   └── bot_simple.py      # Main bot logic
│   ├── astrology/
│   │   ├── simple_astrology_engine.py
│   │   └── simple_chart_analyzer.py
│   ├── database/
│   │   ├── database.py        # SQLite database
│   │   └── models.py         # Data models
│   ├── family/
│   │   ├── family_manager.py
│   │   ├── family_recommendations.py
│   │   └── family_telegram_manager.py
│   ├── scheduler/
│   │   └── daily_reminders.py
│   ├── tracking/
│   │   └── progress_tracker.py
│   ├── personalization/
│   │   └── adaptive_system.py
│   ├── goals/
│   │   └── goal_tracker.py
│   ├── notifications/
│   │   └── enhanced_notifications.py
│   └── utils/
│       ├── config_simple.py   # Configuration
│       └── multi_language.py  # Multi-language support
├── config/
│   ├── astrology_rules/
│   └── languages/
├── data/                      # Database files
└── logs/                      # Log files
```

## 🌟 **Personal Family Focus**

This system is designed specifically for **personal family use**:

- ✅ **Private and Secure** - Only for your family
- ✅ **Simple and Reliable** - No complex commercial features
- ✅ **Peace and Harmony** - Focus on family well-being
- ✅ **Health and Wealth** - Practical guidance for daily life
- ✅ **Spiritual Growth** - Support for personal development

## 🎯 **Success Stories**

Your personal family astrology companion will help you:

- **Find peace** in daily challenges
- **Build harmony** in family relationships
- **Improve health** through cosmic guidance
- **Attract wealth** with auspicious timing
- **Discover happiness** through spiritual growth

## 🚀 **Ready to Start?**

**Your personal family astrology companion is ready to bring peace, harmony, health, wealth, and happiness to your family!** ✨

**Deploy to Render and start your cosmic journey today!** 🌟
