# 🔧 Environment Setup Guide

## 📋 **YOUR .env FILE SHOULD CONTAIN:**

```bash
# Environment Configuration for Personal Family Astro AI Companion
# Personal Family Use - Clean and Simple

# Telegram Configuration (REQUIRED)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=5929651379

# Database Configuration
DB_DATABASE_URL=sqlite:///./data/astro_companion.db

# Logging Configuration
LOG_LOG_LEVEL=INFO
LOG_LOG_FILE=logs/astro_ai.log

# Astrology Configuration
ASTRO_DEFAULT_LANGUAGE=en
ASTRO_SUPPORTED_LANGUAGES=en,mr

# Environment Settings
ENVIRONMENT=production
DEBUG=false

# File Paths
DATA_DIR=./data
LOGS_DIR=./logs
CONFIG_DIR=./config
```

## 🎯 **WHAT YOU NEED TO DO:**

### **1. Create .env file:**
```bash
cp env.example .env
```

### **2. Edit .env file:**
- Replace `your_telegram_bot_token_here` with your actual bot token
- Your chat ID `5929651379` is already set correctly

### **3. For Render Deployment:**
Add these environment variables in Render:

| Key | Value | Description |
|-----|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `your_bot_token_here` | Your Telegram bot token |
| `TELEGRAM_CHAT_ID` | `5929651379` | Your chat ID (already set) |
| `ENVIRONMENT` | `production` | Environment setting |
| `DEBUG` | `false` | Debug mode off |

## ✅ **VERIFICATION:**

Your setup is now:
- ✅ **Clean** - No unnecessary commercial features
- ✅ **Personal** - Your chat ID included
- ✅ **Simple** - Only essential variables
- ✅ **Ready** - For both local and Render deployment

## 🚀 **NEXT STEPS:**

1. **Get your Telegram bot token** from @BotFather
2. **Update .env file** with your bot token
3. **Deploy to Render** with the environment variables above
4. **Test your bot** - It will now send messages directly to you!

**Your personal family astrology companion is ready!** 🌟✨ 