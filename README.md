# 🌟 Astro AI Companion - Personal Family Edition

**Your advanced personal family astrology companion with AI-powered insights, deep analytics, and adaptive learning!**

## ✨ **Features**

### **🎯 Core Astrology Features:**
- **Birth Chart Analysis** - Personalized planetary positions and zodiac signs
- **Advanced Analytics** - Dasha, transits, yogas, and comprehensive chart analysis
- **Daily Predictions** - Cosmic insights with advanced astrology calculations
- **Family Recommendations** - Simple remedies and warnings for family harmony
- **Multi-language Support** - English and Marathi
- **Personal Guidance** - Health, relationships, spiritual growth, life purpose

### **🤖 AI-Powered Features:**
- **Local LLM Chat** - Natural, context-aware conversations via Ollama
- **Model Selection** - Use Llama 3, Mistral, CodeLlama, and other models
- **Adaptive Learning** - Learns from your feedback to personalize recommendations
- **Smart Predictions** - AI-enhanced daily predictions based on your preferences

### **🖼️ Voice & Visualization:**
- **Birth Chart Images** - Beautiful visual birth charts
- **Prediction Images** - Styled prediction graphics
- **Voice Predictions** - Text-to-speech ready for future
- **Chart Visualization** - Professional astrology charts

### **👨‍👩‍👧‍👦 Family Features:**
- **Family Member Management** - Add and manage family members
- **Individual Telegram Access** - Each family member gets personal guidance
- **Family Compatibility** - Analyze relationships and harmony
- **Simple Recommendations** - One remedy and warnings for peace
- **Language Preferences** - Each member can choose English or Marathi

### **🚀 Advanced Features:**
- **Daily Reminders** - Automated morning and evening guidance
- **Progress Tracking** - Track mood, harmony, health, spiritual growth
- **Goal Setting** - Set and track personal and family goals
- **Advanced Personalization** - Learns from your feedback and adapts
- **Enhanced Notifications** - Smart alerts for important events
- **Stateful Registration** - Edit profiles with first/middle/last name support

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

## 🤖 **Ollama Setup (For AI Chat)**

### **1. Install Ollama**
- **Windows:** Download from [ollama.ai](https://ollama.ai)
- **Mac/Linux:** `curl -fsSL https://ollama.ai/install.sh | sh`

### **2. Download Models**
```bash
ollama pull llama3
ollama pull mistral
ollama pull codellama
```

### **3. Start Ollama**
```bash
ollama serve
```

### **4. Test AI Chat**
In your bot, use:
- `/ai What is my astrological forecast today?`
- `/ai mistral:Give me a prediction for next week`

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

## 📱 **Complete Bot Commands**

### **🎯 Basic Commands:**
- `/start` - Welcome message and introduction
- `/register` - Create your personal profile
- `/edit_profile` - Update your profile details
- `/profile` - View your personal details
- `/commands` - Complete list of all commands
- `/help` - Show help guide

### **📅 Prediction Commands:**
- `/daily` - Today's cosmic guidance (with advanced analytics & adaptive learning)
- `/weekly` - This week's forecast
- `/monthly` - Monthly overview
- `/yearly` - Annual predictions

### **🔮 Advanced Analytics:**
- `/analytics` - Comprehensive astrology analysis
- `/dasha` - Current dasha period information
- `/transits` - Current planetary transits
- `/yogas` - Active yogas in your chart

### **🖼️ Voice & Chart Features:**
- `/chart` - Generate your birth chart image
- `/prediction_image` - Get prediction as beautiful image
- `/voice_prediction` - Voice prediction (coming soon)

### **🤖 AI-Powered Chat:**
- `/ai` - Advanced AI chat (requires Ollama)
- `/ai model:prompt` - Use specific LLM model (llama3, mistral, codellama)

### **💫 Personal Guidance:**
- `/personal` - Personal life guidance
- `/family` - Family and relationship insights
- `/health` - Health and wellness guidance
- `/relationships` - Love and relationship advice
- `/spiritual` - Spiritual growth guidance
- `/life_purpose` - Life purpose and career guidance

### **👨‍👩‍👧‍👦 Family Commands:**
- `/family_recommendations` - Family peace, harmony, health, wealth & happiness
- `/family_members` - View registered family members

### **🔮 Consultation Commands:**
- `/ask [question]` - Ask specific questions
- `/remedies` - Personalized remedies

### **📊 Optional Enhancements:**
- `/progress` - Track your progress and achievements
- `/goals` - View and manage your goals
- `/set_goal` - Set new family or personal goals
- `/timing` - Get personalized timing recommendations
- `/rituals` - View custom family rituals

### **🤖 AI & Learning:**
- `/adaptive` - Get personalized adaptive recommendations

## 💡 **Usage Examples**

### **Registration:**
```
/register
Enter: First Name|Middle Name|Last Name|Date of Birth|Time of Birth|Place of Birth|Language
Example: John|A.|Doe|1990-01-15|14:30|Mumbai, India|en
```

### **AI Chat:**
```
/ai What should I focus on today?
/ai mistral:Give me a health prediction
/ai codellama:How can I improve my relationships?
```

### **Advanced Analytics:**
```
/analytics - Get comprehensive chart analysis
/dasha - Check your current dasha period
/transits - See current planetary positions
/yogas - Discover active yogas in your chart
```

### **Natural Conversation:**
Just type anything naturally! The bot will provide personalized guidance based on your birth chart and preferences.

## 🌟 **Advanced Features**

### **Adaptive Learning:**
- Rate predictions with 👍 or 👎
- Bot learns your preferences
- Personalized recommendations improve over time
- Family-specific guidance for each member

### **Privacy & Security:**
- All data stored locally or on your server
- No third-party AI services (unless you choose)
- Family data is private and secure
- No cloud dependencies for core features

### **Multi-language Support:**
- English (en) - Default language
- Marathi (mr) - Full support
- Each family member can choose their preferred language

## 🚀 **Deployment Status**

✅ **Ready for Production**
- All features implemented and tested
- Render deployment guide included
- Error handling and graceful fallbacks
- Family-focused and privacy-first

**Your personal family astrology companion is ready to bring peace, harmony, health, wealth, and happiness to your family!** ✨
