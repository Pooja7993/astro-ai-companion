# 🧪 LOCAL TESTING GUIDE

## **Step 1: Create Test Environment File**

Create a `.env` file in your project root with:

```env
# Test Environment Variables for Local Testing

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_test_bot_token_here
TELEGRAM_CHAT_ID=5929651379

# Environment
ENVIRONMENT=development
DEBUG=true

# Database
DB_DATABASE_URL=sqlite:///data/test_astro_companion.db

# Logging
LOG_LOG_LEVEL=DEBUG
LOG_LOG_FILE=logs/test_simple_astro.log

# Astrology
ASTRO_DEFAULT_LANGUAGE=en
ASTRO_SUPPORTED_LANGUAGES=en,mr

# Scheduler
SCHEDULER_ENABLE_DAILY_REMINDERS=true
SCHEDULER_MORNING_TIME=07:00
SCHEDULER_EVENING_TIME=18:00
SCHEDULER_NIGHT_TIME=21:30
```

## **Step 2: Get Your Bot Token**

1. **Message @BotFather** on Telegram
2. **Send `/mybots`** to see your bots
3. **Select your bot** and get the token
4. **Replace `your_test_bot_token_here`** with your actual token

## **Step 3: Test Dependencies**

```bash
# Install all dependencies
pip install -r requirements_simple.txt

# Test imports
python -c "from telegram import Update; print('✅ Telegram import works')"
python -c "from loguru import logger; print('✅ Loguru import works')"
python -c "import ephem; print('✅ Ephem import works')"
```

## **Step 4: Test Configuration**

```bash
# Test config loading
python -c "from src.utils.config_simple import get_config; config = get_config(); print('✅ Config loaded successfully')"
```

## **Step 5: Test Bot Startup**

```bash
# Test bot startup (will show error if token missing)
python run_simple.py
```

## **Step 6: Test Individual Components**

```bash
# Test database
python -c "from src.database.database import DatabaseManager; db = DatabaseManager(); print('✅ Database works')"

# Test astrology engine
python -c "from src.astrology.simple_chart_analyzer import chart_analyzer; print('✅ Astrology engine works')"

# Test family recommendations
python -c "from src.family.family_recommendations import family_recommendations; print('✅ Family recommendations work')"
```

## **Step 7: Full Integration Test**

Once you have your bot token in `.env`:

```bash
# Start the bot
python run_simple.py
```

**Expected Output:**
```
🌟 Starting Simple Astro AI Companion...
✅ Bot started successfully!
📱 Your personal astrology companion is now running...
💬 Chat with your bot on Telegram!
```

## **Step 8: Test Bot Commands**

Message your bot on Telegram:
- `/start` - Should welcome you
- `/help` - Should show all commands
- `/register` - Should ask for birth details
- `/daily` - Should give daily prediction
- `/family` - Should give family recommendations

## **✅ SUCCESS CRITERIA:**

- ✅ **All imports work** - No ModuleNotFoundError
- ✅ **Config loads** - No Pydantic validation errors
- ✅ **Bot starts** - No startup errors
- ✅ **Commands work** - Bot responds to messages
- ✅ **Database works** - Can save/retrieve data
- ✅ **Astrology works** - Can generate predictions

## **🚨 COMMON ISSUES & FIXES:**

### **Missing Bot Token:**
```
❌ Error: TELEGRAM_BOT_TOKEN not found
✅ Fix: Add your bot token to .env file
```

### **Import Errors:**
```
❌ Error: No module named 'telegram'
✅ Fix: pip install python-telegram-bot>=20.7
```

### **Config Errors:**
```
❌ Error: Pydantic validation error
✅ Fix: Check .env file format and values
```

## **🎯 READY FOR RENDER:**

Once local testing passes:
1. **All tests green** ✅
2. **Bot responds correctly** ✅
3. **No errors in logs** ✅
4. **Ready to deploy to Render** 🚀

**Let's start testing!** 🧪 