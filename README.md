# 🌟 Astro AI Companion - Complete Family Astrology System

A comprehensive family astrology system that combines **Vedic Astrology**, **Numerology**, and **Lal Kitab** to provide unified guidance for each family member through personalized Telegram chats and a modern web interface.

## ✨ Features

### 🎯 **Unified Astrological System**
- **Vedic Astrology**: Planetary positions, Nakshatras, Dashas
- **Numerology**: Life Path, Destiny, and Soul numbers
- **Lal Kitab**: Practical remedies and karmic debt analysis
- **AI-Powered**: OpenRouter integration for natural language guidance

### 👨‍👩‍👧‍👦 **Family-Centric Design**
- Individual profiles for each family member
- Personal Telegram chat for each member
- Family harmony guidance and compatibility
- Unified dashboard for family management

### 💬 **Natural Chat Interface**
- Telegram bot with natural language processing
- No commands needed - just chat naturally
- Personalized responses based on astrological profile
- Real-time guidance and daily insights

### 🌐 **Modern Web UI**
- Beautiful, responsive web interface
- Real-time updates with WebSocket
- Family member management
- Astrological profile visualization

## 🚀 **Render Deployment**

### **Prerequisites**
1. **Render Account**: Sign up at [render.com](https://render.com)
2. **OpenRouter API Key**: Get free API key from [openrouter.ai](https://openrouter.ai)
3. **Telegram Bot**: Create bot with [@BotFather](https://t.me/botfather)

### **One-Click Deploy**
1. Fork this repository
2. Connect to Render
3. Use the `render.yaml` blueprint
4. Set environment variables:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token

### **Manual Setup**

#### **1. Database Setup**
```bash
# Render automatically creates PostgreSQL database
# Connection string is provided via DATABASE_URL
```

#### **2. Web Service**
- **Build Command**: `pip install -r requirements.txt && python -c "from src.config.database import init_database; init_database()"`
- **Start Command**: `python src/web/app.py`
- **Environment**: Python 3.11

#### **3. Telegram Bot Service**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python run_bot.py`
- **Environment**: Python 3.11

#### **4. Environment Variables**
```env
DATABASE_URL=postgresql://... (auto-provided by Render)
OPENROUTER_API_KEY=your_openrouter_key
TELEGRAM_BOT_TOKEN=your_bot_token
SECRET_KEY=auto-generated
ENVIRONMENT=production
```

## 📱 **Usage**

### **Web Interface**
1. Visit your Render app URL
2. Register family members
3. View unified astrological profiles
4. Chat with AI assistant
5. Manage family harmony guidance

### **Telegram Bot**
1. Start chat with your bot
2. Register with: `FirstName|MiddleName|LastName|YYYY-MM-DD|HH:MM|City,Country|relationship`
3. Chat naturally for personalized guidance
4. Each family member gets their own chat experience

### **Example Registration**
```
John|Kumar|Sharma|1990-05-15|14:30|Mumbai,India|head
```

## 🔮 **Astrological Systems**

### **Vedic Astrology**
- Precise planetary calculations using Swiss Ephemeris
- Nakshatra (lunar mansion) analysis
- House positions and aspects
- Dasha (planetary period) calculations

### **Numerology**
- Life Path Number from birth date
- Destiny Number from full name
- Soul Number from vowels in name
- Personal year and cycle analysis

### **Lal Kitab**
- Karmic debt analysis
- Practical remedies and solutions
- House-based predictions
- Simple, actionable guidance

## 🛠 **Technical Architecture**

### **Backend**
- **Flask**: Web framework with WebSocket support
- **SQLAlchemy**: PostgreSQL ORM
- **Swiss Ephemeris**: Astronomical calculations
- **OpenRouter**: Free LLM integration
- **Python Telegram Bot**: Async bot framework

### **Frontend**
- **Bootstrap 5**: Responsive UI framework
- **Socket.IO**: Real-time updates
- **Vanilla JavaScript**: No heavy frameworks
- **Progressive Web App**: Mobile-friendly

### **Database Schema**
- **Users**: Family member profiles
- **Families**: Family groupings
- **BirthCharts**: Astrological data
- **Predictions**: Generated guidance

## 🔧 **Development**

### **Local Setup**
```bash
# Clone repository
git clone <your-repo-url>
cd astro-ai-companion

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your keys

# Initialize database
python -c "from src.config.database import init_database; init_database()"

# Run web app
python src/web/app.py

# Run Telegram bot (separate terminal)
python run_bot.py
```

### **Project Structure**
```
src/
├── config/          # Database configuration
├── models/          # SQLAlchemy models
├── services/        # Business logic services
├── telegram_bot/    # Telegram bot implementation
├── web/            # Flask web application
│   ├── templates/  # HTML templates
│   └── app.py     # Main Flask app
└── utils/          # Utility functions

requirements.txt     # Python dependencies
render.yaml         # Render deployment config
run_bot.py          # Telegram bot runner
```

## 🌟 **Key Features**

### **For Families**
- ✅ Each member gets personalized guidance
- ✅ Individual Telegram chats
- ✅ Family harmony analysis
- ✅ Unified astrological insights
- ✅ Daily guidance and reminders

### **For Developers**
- ✅ Modern Python architecture
- ✅ PostgreSQL database
- ✅ Free LLM integration
- ✅ Render-optimized deployment
- ✅ Scalable and maintainable

### **For Users**
- ✅ Natural chat interface
- ✅ No complex commands
- ✅ Beautiful web dashboard
- ✅ Real-time updates
- ✅ Mobile-friendly design

## 📊 **Cost Optimization**

### **Free Tier Usage**
- **Render**: Free web service + PostgreSQL
- **OpenRouter**: Free LLM API calls
- **Telegram**: Free bot platform
- **Total Monthly Cost**: $0 for moderate usage

### **Scaling Options**
- Render paid plans for higher traffic
- OpenRouter paid models for better AI
- Additional database storage as needed

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 **License**

MIT License - see LICENSE file for details.

## 🆘 **Support**

- **Issues**: GitHub Issues
- **Documentation**: README.md
- **Community**: Discussions tab

---

**Made with ❤️ for families seeking cosmic guidance**

🌟 **Start your family's astrological journey today!** 🌟