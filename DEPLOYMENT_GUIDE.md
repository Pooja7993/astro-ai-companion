# 🚀 **Complete Deployment Guide - Astro AI Companion**

## 📋 **Table of Contents**
1. [Local Development Setup](#local-development-setup)
2. [Ollama AI Setup](#ollama-ai-setup)
3. [Telegram Bot Setup](#telegram-bot-setup)
4. [Render Deployment](#render-deployment)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Configuration](#advanced-configuration)

---

## 🏠 **Local Development Setup**

### **Step 1: Clone Repository**
```bash
git clone https://github.com/Pooja7993/astro-ai-companion.git
cd astro-ai-companion
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements_simple.txt
```

### **Step 4: Environment Variables**
Create `.env` file:
```env
telegram_bot_token=your_bot_token_here
telegram_chat_id=5929651379
```

### **Step 5: Test Locally**
```bash
python run_simple.py
```

**Expected Output:**
```
🌟 Starting Simple Astro AI Companion...
🌐 Web server started on port 8080
✅ Bot started successfully!
📱 Your personal astrology companion is now running...
💬 Chat with your bot on Telegram!
```

---

## 🤖 **Ollama AI Setup (Optional)**

### **Step 1: Install Ollama**
- **Windows:** Download from [ollama.ai](https://ollama.ai)
- **Mac:** `curl -fsSL https://ollama.ai/install.sh | sh`
- **Linux:** `curl -fsSL https://ollama.ai/install.sh | sh`

### **Step 2: Start Ollama Server**
```bash
ollama serve
```

### **Step 3: Download Models**
```bash
# Download popular models
ollama pull llama3
ollama pull mistral
ollama pull codellama
ollama pull phi3
ollama pull gemma
```

### **Step 4: Test Ollama**
```bash
# Test if Ollama is working
ollama run llama3 "Hello, how are you?"
```

### **Step 5: Test AI Chat in Bot**
In your Telegram bot:
```
/ai What is my astrological forecast today?
/ai mistral:Give me a prediction for next week
```

---

## 📱 **Telegram Bot Setup**

### **Step 1: Create Bot**
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot`
3. Choose bot name (e.g., "My Astro AI Companion")
4. Choose username (e.g., "my_astro_bot")
5. Save the bot token

### **Step 2: Get Chat ID**
1. Message your bot: `/start`
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find your `chat_id` in the response
4. Add to `.env`: `telegram_chat_id=your_chat_id`

### **Step 3: Test Bot**
1. Start your bot locally
2. Message your bot on Telegram
3. Try commands: `/start`, `/register`, `/help`

---

## ☁️ **Render Deployment**

### **Step 1: Prepare Repository**
```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### **Step 2: Create Render Account**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render access

### **Step 3: Create Web Service**
1. Click **"New +"** → **"Web Service"**
2. Connect to your GitHub repository
3. Configure settings:
   - **Name:** `astro-ai-companion`
   - **Environment:** `Python 3`
   - **Region:** Choose closest to you
   - **Branch:** `main`

### **Step 4: Build Configuration**
- **Build Command:** `pip install -r requirements_simple.txt`
- **Start Command:** `python run_simple.py`

### **Step 5: Environment Variables**
In Render dashboard, add:
```
telegram_bot_token=your_bot_token_here
telegram_chat_id=your_chat_id_here
```

### **Step 6: Deploy**
1. Click **"Create Web Service"**
2. Monitor build logs
3. Wait for deployment to complete
4. Test your bot on Telegram

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Bot Not Responding**
**Symptoms:** Bot doesn't reply to messages
**Solutions:**
- Check if bot token is correct
- Verify chat ID is correct
- Check Render logs for errors
- Ensure bot is not blocked

#### **2. Ollama Connection Error**
**Symptoms:** `/ai` command fails
**Solutions:**
- Install Ollama: [ollama.ai](https://ollama.ai)
- Start server: `ollama serve`
- Download model: `ollama pull llama3`
- Check firewall settings

#### **3. Database Errors**
**Symptoms:** Registration/profile errors
**Solutions:**
- Check database file permissions
- Ensure `data/` directory exists
- Restart the application

#### **4. Render Deployment Fails**
**Symptoms:** Build fails or service won't start
**Solutions:**
- Check build logs in Render dashboard
- Verify all dependencies in `requirements_simple.txt`
- Ensure `run_simple.py` exists and is executable
- Check environment variables

#### **5. Chart Generation Fails**
**Symptoms:** `/chart` command doesn't work
**Solutions:**
- Ensure matplotlib is installed
- Check if user has birth details registered
- Verify image generation permissions

### **Debug Commands**
```bash
# Check if bot is running
curl https://your-service-name.onrender.com/

# Check Ollama status
curl http://localhost:11434/api/tags

# Test database
python -c "from src.database.database import DatabaseManager; db = DatabaseManager(); print('Database OK')"
```

---

## ⚙️ **Advanced Configuration**

### **Custom Environment Variables**
```env
# Core Settings
telegram_bot_token=your_bot_token
telegram_chat_id=your_chat_id

# Database
DB_DATABASE_URL=sqlite:///./data/astro_companion.db

# Logging
LOG_LOG_LEVEL=INFO
LOG_LOG_FILE=logs/simple_astro.log

# Astrology
ASTRO_DEFAULT_LANGUAGE=en
ASTRO_SUPPORTED_LANGUAGES=en,mr

# Environment
ENVIRONMENT=production
DEBUG=false
```

### **Ollama Configuration**
```bash
# Custom model configuration
ollama create my-astro-model -f Modelfile

# Modelfile content:
FROM llama3
SYSTEM "You are a helpful astrology assistant. Provide guidance for peace, harmony, health, wealth, and happiness."
```

### **Performance Optimization**
- **Database:** Use PostgreSQL for production (optional)
- **Caching:** Add Redis for session management (optional)
- **Monitoring:** Add health check endpoints
- **Scaling:** Configure auto-scaling in Render

---

## 📊 **Monitoring & Maintenance**

### **Health Checks**
- **Bot Status:** Message `/start` to test
- **Database:** Check if registration works
- **AI Chat:** Test `/ai` command
- **Charts:** Test `/chart` command

### **Logs**
- **Render Logs:** Available in Render dashboard
- **Application Logs:** `logs/simple_astro.log`
- **Error Tracking:** Check for exceptions in logs

### **Updates**
```bash
# Update from GitHub
git pull origin main

# Restart service
# In Render: Manual Deploy → Clear build cache & deploy
```

---

## 🎯 **Success Checklist**

✅ **Local Setup**
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Environment variables set
- [ ] Bot responds to `/start`

✅ **Ollama Setup (Optional)**
- [ ] Ollama installed
- [ ] Server running (`ollama serve`)
- [ ] Models downloaded
- [ ] `/ai` command works

✅ **Telegram Setup**
- [ ] Bot created with BotFather
- [ ] Chat ID obtained
- [ ] Bot token configured
- [ ] Bot responds to commands

✅ **Render Deployment**
- [ ] Web service created
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Bot works on Render

✅ **Feature Testing**
- [ ] Registration works (`/register`)
- [ ] Daily predictions work (`/daily`)
- [ ] Advanced analytics work (`/analytics`)
- [ ] Chart generation works (`/chart`)
- [ ] AI chat works (`/ai`)

---

## 🚀 **Ready to Launch!**

Your Astro AI Companion is now ready to bring peace, harmony, health, wealth, and happiness to your family!

**Next Steps:**
1. Test all features thoroughly
2. Add family members
3. Customize preferences
4. Enjoy your personal astrology companion!

**Need Help?**
- Check the troubleshooting section
- Review Render logs
- Test commands one by one
- Contact support if needed

**Happy Astrology Journey!** ✨🌟 