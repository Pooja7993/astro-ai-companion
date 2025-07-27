"""
Multi-Language Support for Astro AI Companion
Personal Family Use - English and Marathi
"""

from typing import Dict, Any, Optional, List
from enum import Enum

from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class Language(Enum):
    """Supported languages."""
    ENGLISH = "en"
    MARATHI = "mr"


class MultiLanguageSupport:
    """Multi-language support system for English and Marathi."""
    
    def __init__(self):
        self.translations = self._load_translations()
        self.current_language = Language.ENGLISH
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """Load translations for English and Marathi."""
        return {
            "en": {
                # Basic commands
                "start_welcome": """🌟 **Welcome to Your Personal Astro AI Companion!**

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

Ready to explore your cosmic journey? Start with `/register` or just chat with me! ✨""",
                
                "register_guide": """🌟 Welcome! Let's create your personal astrological profile.

Please provide your birth details in this format:
**Name|Date of Birth|Time of Birth|Place of Birth**

Example:
`John Doe|1990-01-15|14:30|Mumbai, India`

This will help me provide personalized guidance for you and your family.""",
                
                "registration_success": """✅ **Welcome to your personal astrology companion!**

Your profile has been created successfully. I can now provide you with:

• **Personal daily guidance** based on your birth chart
• **Family insights** and relationship analysis
• **Health and wellness** cosmic guidance
• **Spiritual growth** and life purpose insights

Try asking me anything naturally, or use commands like:
• `/daily` - Today's guidance
• `/family` - Family insights
• `/health` - Wellness guidance
• `/personal` - Personal life guidance

What would you like to know about your cosmic journey? ✨""",
                
                "help_message": """🌟 **Astro AI Companion - Help Guide**

**📋 Available Commands:**

**🎯 Basic Commands:**
• `/start` - Welcome message and introduction
• `/register` - Create your personal profile
• `/help` - Show this help message
• `/profile` - View your personal details

**📅 Prediction Commands:**
• `/daily` - Today's cosmic guidance
• `/weekly` - This week's forecast
• `/monthly` - Monthly overview
• `/yearly` - Annual predictions

**💫 Personal Guidance:**
• `/personal` - Personal life guidance
• `/family` - Family and relationship insights
• `/health` - Health and wellness guidance
• `/relationships` - Love and relationship advice
• `/spiritual` - Spiritual growth guidance
• `/life_purpose` - Life purpose and career guidance

**🔮 Consultation Commands:**
• `/ask [question]` - Ask specific questions
• `/remedies` - Personalized remedies

**💬 Natural Conversation:**
You can also chat with me naturally! Just type your questions or thoughts, and I'll provide personalized guidance based on your birth chart.

**👨‍👩‍👧‍👦 Family Features:**
• Personal birth chart analysis
• Family compatibility insights
• Individual guidance for each family member
• Private and secure for your family only

**💎 Example Questions:**
• "How's my day looking?"
• "What should I focus on today?"
• "How can I improve my relationships?"
• "What's my life purpose?"
• "How can I grow spiritually?"

**🌟 Your Personal Astrology Guide:**
I'm designed specifically for you and your family, providing personalized cosmic guidance for your personal growth and family harmony.

Need help with anything specific? Just ask! ✨""",
                
                # Daily predictions
                "daily_prediction": """🌟 **Daily Cosmic Guidance**

**📅 Today's Energy:**
• **Morning:** Perfect for new beginnings and important decisions
• **Afternoon:** Focus on creative activities and learning
• **Evening:** Family time and relaxation
• **Night:** Reflection and planning for tomorrow

**💫 Today's Focus:**
• **Personal growth:** Time for self-improvement
• **Family harmony:** Strengthen family bonds
• **Health:** Focus on wellness and vitality
• **Spiritual:** Connect with higher consciousness

**🎯 Today's Opportunities:**
• **Morning meditation:** Start day with intention
• **Family bonding:** Quality time with loved ones
• **Health activities:** Exercise and healthy eating
• **Spiritual practice:** Prayer and meditation

**💎 Today's Remedies:**
• **Morning:** Light a diya for positive energy
• **Afternoon:** Drink water from copper vessel
• **Evening:** Family prayer and gratitude
• **Night:** Reflect on the day's blessings

Have a wonderful day filled with cosmic blessings! ✨""",
                
                # Family guidance
                "family_guidance": """👨‍👩‍👧‍👦 **Family & Relationship Guidance**

**💝 FAMILY ENERGY ANALYSIS:**

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

Want more specific guidance? Ask me: "How can I improve family relationships?" or "What's best for my family?" 👨‍👩‍👧‍👦""",
                
                # Health guidance
                "health_guidance": """🏥 **Health & Wellness Guidance**

**💪 HEALTH ENERGY ANALYSIS:**

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

Want more specific guidance? Ask me: "How can I improve my health?" or "What's best for my wellness?" 🏥""",
                
                # Error messages
                "error_registration": "❌ Please provide all details in the correct format:\n**Name|Date of Birth|Time of Birth|Place of Birth**",
                "error_general": "❌ Sorry, I couldn't process your request right now. Please try again.",
                "error_not_registered": "❌ Please register first using `/register` to create your profile.",
                "error_prediction": "❌ Error generating prediction. Please try again.",
                
                # Success messages
                "profile_created": "✅ Profile created successfully!",
                "user_updated": "✅ User information updated successfully!",
                "family_member_added": "✅ Family member added successfully!",
                
                # Natural conversation responses
                "greeting_response": "🌟 Hello! How can I help you with your cosmic journey today?",
                "daily_question": "📅 **Today's Guidance**\n\nToday is perfect for new beginnings and important decisions. Focus on your personal growth and family harmony. The cosmic energy supports your spiritual journey and inner peace.",
                "family_question": "👨‍👩‍👧‍👦 **Family Guidance**\n\nYour family bonds are strong and supportive. Focus on open communication and quality time together. The cosmic energy favors family harmony and emotional connections.",
                "health_question": "🏥 **Health Guidance**\n\nFocus on physical and mental wellness. Practice morning meditation and maintain a balanced diet. The cosmic energy supports your vitality and inner peace.",
                "spiritual_question": "🙏 **Spiritual Guidance**\n\nYour spiritual path is clear and purposeful. Focus on meditation, prayer, and service to others. The cosmic energy supports your spiritual growth and wisdom.",
                "career_question": "💼 **Career Guidance**\n\nYour professional path involves helping others through meaningful work. Focus on service, teaching, and guidance. The cosmic energy supports your leadership and wisdom.",
                "general_guidance": "🌟 **Personal Guidance**\n\nI sense you're seeking guidance. Based on your cosmic energy, focus on personal growth, family harmony, and spiritual development. Trust your intuition and follow your heart's calling."
            },
            
            "mr": {
                # Basic commands
                "start_welcome": """🌟 **तुमच्या वैयक्तिक ज्योतिष साथीदाराला स्वागत आहे!**

मी तुमचा वैयक्तिक ज्योतिष मार्गदर्शक आहे, तुमच्या आणि तुमच्या कुटुंबासाठी विशेषतः तयार केलेला. मी पुरवतो:

**✨ वैयक्तिक मार्गदर्शन:**
• दैनिक कॉस्मिक अंतर्दृष्टी आणि भविष्यवाणी
• कुटुंबातील नातेसंबंधांचे विश्लेषण
• आरोग्य आणि कल्याण मार्गदर्शन
• आध्यात्मिक विकास समर्थन
• जीवनाच्या उद्देशाची शोध

**🎯 कसे वापरावे:**
• **नैसर्गिक संवाद:** फक्त तुमच्या मनातील गोष्टी टाइप करा
• **आदेश:** /daily, /weekly, /family, /health इत्यादी वापरा
• **प्रश्न:** तुमच्या जीवनाबद्दल मला काहीही विचारा

**👨‍👩‍👧‍👦 कुटुंब वैशिष्ट्ये:**
• वैयक्तिक जन्मकुंडली विश्लेषण
• कुटुंब सुसंगतता अंतर्दृष्टी
• प्रत्येक कुटुंब सदस्यासाठी वैयक्तिक मार्गदर्शन
• तुमच्या कुटुंबासाठी खाजगी आणि सुरक्षित

**🚀 त्वरित सुरुवात:**
1. तुमचे प्रोफाइल तयार करण्यासाठी `/register` वापरा
2. मला नैसर्गिकरित्या काहीही विचारा
3. विशिष्ट मार्गदर्शनासाठी आदेश वापरा

तुमच्या कॉस्मिक प्रवासाचा शोध घेण्यास तयार आहात? `/register` सह सुरुवात करा किंवा फक्त माझ्याशी संवाद साधा! ✨""",
                
                "register_guide": """🌟 स्वागत आहे! चला तुमचे वैयक्तिक ज्योतिष प्रोफाइल तयार करूया.

कृपया या स्वरूपात तुमचे जन्म तपशील द्या:
**नाव|जन्म तारीख|जन्म वेळ|जन्म ठिकाण**

उदाहरण:
`राजेश कुमार|1990-01-15|14:30|मुंबई, भारत`

हे मला तुमच्या आणि तुमच्या कुटुंबासाठी वैयक्तिकृत मार्गदर्शन पुरवण्यास मदत करेल.""",
                
                "registration_success": """✅ **तुमच्या वैयक्तिक ज्योतिष साथीदाराला स्वागत आहे!**

तुमचे प्रोफाइल यशस्वीरित्या तयार केले गेले आहे. आता मी तुम्हाला पुरवू शकतो:

• तुमच्या जन्मकुंडलीवर आधारित **वैयक्तिक दैनिक मार्गदर्शन**
• **कुटुंब अंतर्दृष्टी** आणि नातेसंबंध विश्लेषण
• **आरोग्य आणि कल्याण** कॉस्मिक मार्गदर्शन
• **आध्यात्मिक विकास** आणि जीवनाच्या उद्देशाची अंतर्दृष्टी

मला नैसर्गिकरित्या काहीही विचारण्याचा प्रयत्न करा, किंवा यासारखे आदेश वापरा:
• `/daily` - आजचे मार्गदर्शन
• `/family` - कुटुंब अंतर्दृष्टी
• `/health` - कल्याण मार्गदर्शन
• `/personal` - वैयक्तिक जीवन मार्गदर्शन

तुमच्या कॉस्मिक प्रवासाबद्दल तुम्हाला काय जाणून घ्यायचे आहे? ✨""",
                
                "help_message": """🌟 **ज्योतिष साथीदार - मदत मार्गदर्शन**

**📋 उपलब्ध आदेश:**

**🎯 मूलभूत आदेश:**
• `/start` - स्वागत संदेश आणि परिचय
• `/register` - तुमचे वैयक्तिक प्रोफाइल तयार करा
• `/help` - हे मदत संदेश दाखवा
• `/profile` - तुमचे वैयक्तिक तपशील पहा

**📅 भविष्यवाणी आदेश:**
• `/daily` - आजचे कॉस्मिक मार्गदर्शन
• `/weekly` - या आठवड्याचा अंदाज
• `/monthly` - मासिक आढावा
• `/yearly` - वार्षिक भविष्यवाणी

**💫 वैयक्तिक मार्गदर्शन:**
• `/personal` - वैयक्तिक जीवन मार्गदर्शन
• `/family` - कुटुंब आणि नातेसंबंध अंतर्दृष्टी
• `/health` - आरोग्य आणि कल्याण मार्गदर्शन
• `/relationships` - प्रेम आणि नातेसंबंध सल्ला
• `/spiritual` - आध्यात्मिक विकास मार्गदर्शन
• `/life_purpose` - जीवनाचा उद्देश आणि करिअर मार्गदर्शन

**🔮 सल्लागार आदेश:**
• `/ask [प्रश्न]` - विशिष्ट प्रश्न विचारा
• `/remedies` - वैयक्तिकृत उपाय

**💬 नैसर्गिक संवाद:**
तुम्ही माझ्याशी नैसर्गिकरित्या संवाद साधू शकता! फक्त तुमचे प्रश्न किंवा विचार टाइप करा, आणि मी तुमच्या जन्मकुंडलीवर आधारित वैयक्तिकृत मार्गदर्शन पुरवेन.

**👨‍👩‍👧‍👦 कुटुंब वैशिष्ट्ये:**
• वैयक्तिक जन्मकुंडली विश्लेषण
• कुटुंब सुसंगतता अंतर्दृष्टी
• प्रत्येक कुटुंब सदस्यासाठी वैयक्तिक मार्गदर्शन
• तुमच्या कुटुंबासाठी खाजगी आणि सुरक्षित

**💎 उदाहरण प्रश्न:**
• "माझा दिवस कसा दिसत आहे?"
• "आज मी कशावर लक्ष केंद्रित करावे?"
• "मी माझे नातेसंबंध कसे सुधारू शकतो?"
• "माझा जीवनाचा उद्देश काय आहे?"
• "मी आध्यात्मिकरित्या कसे वाढू शकतो?"

**🌟 तुमचा वैयक्तिक ज्योतिष मार्गदर्शक:**
मी तुमच्या आणि तुमच्या कुटुंबासाठी विशेषतः तयार केलेला आहे, तुमच्या वैयक्तिक विकास आणि कुटुंब सुसंवादासाठी वैयक्तिकृत कॉस्मिक मार्गदर्शन पुरवतो.

काही विशिष्ट मदत हवी आहे? फक्त विचारा! ✨""",
                
                # Daily predictions
                "daily_prediction": """🌟 **दैनिक कॉस्मिक मार्गदर्शन**

**📅 आजची ऊर्जा:**
• **सकाळ:** नवीन सुरुवात आणि महत्वाचे निर्णय घेण्यासाठी परिपूर्ण
• **दुपार:** सर्जनशील क्रियाकलाप आणि शिकण्यावर लक्ष केंद्रित करा
• **संध्याकाळ:** कुटुंब वेळ आणि विश्रांती
• **रात्र:** उद्यासाठी चिंतन आणि नियोजन

**💫 आजचे लक्ष केंद्र:**
• **वैयक्तिक विकास:** स्वतःच्या सुधारणेसाठी वेळ
• **कुटुंब सुसंवाद:** कुटुंबातील बंध मजबूत करा
• **आरोग्य:** कल्याण आणि जीवनशक्तीवर लक्ष केंद्रित करा
• **आध्यात्मिक:** उच्च चेतनेशी जोडणी

**🎯 आजची संधी:**
• **सकाळचे ध्यान:** हेतूने दिवस सुरु करा
• **कुटुंब बंध:** प्रियजनांसोबत गुणवत्तापूर्ण वेळ
• **आरोग्य क्रियाकलाप:** व्यायाम आणि निरोगी खाणे
• **आध्यात्मिक सराव:** प्रार्थना आणि ध्यान

**💎 आजचे उपाय:**
• **सकाळ:** सकारात्मक ऊर्जेसाठी दिवा लावा
• **दुपार:** तांब्याच्या भांड्यातून पाणी प्या
• **संध्याकाळ:** कुटुंब प्रार्थना आणि कृतज्ञता
• **रात्र:** दिवसाच्या आशीर्वादांवर चिंतन करा

कॉस्मिक आशीर्वादांनी भरलेला एक चांगला दिवस घ्या! ✨""",
                
                # Family guidance
                "family_guidance": """👨‍👩‍👧‍👦 **कुटुंब आणि नातेसंबंध मार्गदर्शन**

**💝 कुटुंब ऊर्जा विश्लेषण:**

**🏠 कुटुंब गतिशीलता:**
• **कुटुंब सुसंवाद:** समर्थनकारक वातावरणासह मजबूत बंध
• **संवाद शैली:** खुला आणि उबदार कुटुंब संवाद
• **कुटुंब शक्ती:** भावनिक समर्थन आणि परस्पर समज

**💑 नातेसंबंध अंतर्दृष्टी:**
• **प्रेम सुसंगतता:** काळजी घेणाऱ्या जोडीदारांसह उच्च सुसंगतता
• **लग्न वेळ:** शुक्र मजबूत कालावधी नातेसंबंध संधी आणतात
• **नातेसंबंध आव्हाने:** बुध मागे जात असताना संवाद

**👶 कुटुंब नियोजन:**
• **मुले वेळ:** गुरू कालावधी कुटुंब विस्तारास अनुकूल
• **पालक-मूल बंध:** मजबूत भावनिक जोडणी
• **कुटुंब विकास:** स्थिर कुटुंब विकास आणि सुसंवाद

**🎯 कुटुंब यशस्वी सूत्र:**
1. **सकाळची कुटुंब वेळ:** कुटुंब बंधाने दिवस सुरु करा
2. **संवाद तास:** 6-8 PM कुटुंब चर्चेसाठी सर्वोत्तम
3. **शनिवार क्रियाकलाप:** शुक्र मजबूत कालावधीत कुटुंब क्रियाकलाप नियोजन करा
4. **कुटुंब विधी:** अर्थपूर्ण कुटुंब परंपरा तयार करा

**💎 कुटुंब उपाय:**
• **दैनिक सराव:** कुटुंब सुसंवादासाठी दिवा लावा
• **सोमवार विधी:** कुटुंब शक्तीसाठी सूर्याला पाणी अर्पण करा
• **शुक्रवार अर्पण:** शुक्राच्या प्रेम आशीर्वादासाठी पांढरे फूल
• **कुटुंब संरक्षण:** कुटुंब क्षेत्रात लहान गणेश मूर्ती ठेवा

अधिक विशिष्ट मार्गदर्शन हवे आहे? मला विचारा: "मी कुटुंब नातेसंबंध कसे सुधारू शकतो?" किंवा "माझ्या कुटुंबासाठी काय चांगले आहे?" 👨‍👩‍👧‍👦""",
                
                # Health guidance
                "health_guidance": """🏥 **आरोग्य आणि कल्याण मार्गदर्शन**

**💪 आरोग्य ऊर्जा विश्लेषण:**

**🌿 कल्याण लक्ष केंद्र:**
• **शारीरिक आरोग्य:** चांगल्या जीवनशक्तीसह मजबूत शरीर
• **मानसिक कल्याण:** संतुलित भावनिक आणि मानसिक स्थिती
• **ऊर्जा पातळी:** सूर्य मजबूत कालावधीत उच्च ऊर्जा

**🏃‍♂️ फिटनेस मार्गदर्शन:**
• **सर्वोत्तम व्यायाम वेळ:** जास्तीत जास्त ऊर्जेसाठी 6-8 AM
• **व्यायाम प्रकार:** मानसिक शांतीसाठी योग आणि ध्यान
• **पुनर्प्राप्ती कालावधी:** चंद्र कमकुवत कालावधीत विश्रांती

**🍎 पोषण सल्ला:**
• **आहार लक्ष केंद्र:** ताजे फळे आणि भाज्या
• **जलयोजन:** तांब्याच्या भांड्याचे फायदे असलेले पाणी प्या
• **उपवास:** आरोग्य शुद्धीकरणासाठी मंगळवार उपवास

**😴 झोप आणि विश्रांती:**
• **झोप वेळ:** उत्तम विश्रांतीसाठी 10 PM ते 6 AM
• **झोप गुणवत्ता:** चंद्र मजबूत कालावधीत खोल झोप
• **विश्रांती:** शांतीसाठी संध्याकाळचे ध्यान

**💎 आरोग्य उपाय:**
• **दैनिक सराव:** सकाळचे सूर्य नमस्कार
• **मंगळवार विधी:** आरोग्य शुद्धीकरणासाठी उपवास
• **बुधवार अर्पण:** आरोग्यासाठी हिरव्या भाज्या
• **आरोग्य संरक्षण:** कल्याणासाठी तुळस झाड ठेवा

अधिक विशिष्ट मार्गदर्शन हवे आहे? मला विचारा: "मी माझे आरोग्य कसे सुधारू शकतो?" किंवा "माझ्या कल्याणासाठी काय चांगले आहे?" 🏥""",
                
                # Error messages
                "error_registration": "❌ कृपया योग्य स्वरूपात सर्व तपशील द्या:\n**नाव|जन्म तारीख|जन्म वेळ|जन्म ठिकाण**",
                "error_general": "❌ माफ करा, मी आता तुमची विनंती प्रक्रिया करू शकत नाही. कृपया पुन्हा प्रयत्न करा.",
                "error_not_registered": "❌ कृपया प्रथम तुमचे प्रोफाइल तयार करण्यासाठी `/register` वापरा.",
                "error_prediction": "❌ भविष्यवाणी तयार करताना त्रुटी. कृपया पुन्हा प्रयत्न करा.",
                
                # Success messages
                "profile_created": "✅ प्रोफाइल यशस्वीरित्या तयार केले!",
                "user_updated": "✅ वापरकर्ता माहिती यशस्वीरित्या अपडेट केली!",
                "family_member_added": "✅ कुटुंब सदस्य यशस्वीरित्या जोडला!",
                
                # Natural conversation responses
                "greeting_response": "🌟 नमस्कार! मी तुमच्या कॉस्मिक प्रवासात कसे मदत करू शकतो?",
                "daily_question": "📅 **आजचे मार्गदर्शन**\n\nआज नवीन सुरुवात आणि महत्वाचे निर्णय घेण्यासाठी परिपूर्ण आहे. तुमच्या वैयक्तिक विकास आणि कुटुंब सुसंवादावर लक्ष केंद्रित करा. कॉस्मिक ऊर्जा तुमच्या आध्यात्मिक प्रवास आणि अंतर्गत शांतीला समर्थन देते.",
                "family_question": "👨‍👩‍👧‍👦 **कुटुंब मार्गदर्शन**\n\nतुमचे कुटुंब बंध मजबूत आणि समर्थनकारक आहेत. खुला संवाद आणि गुणवत्तापूर्ण वेळ एकत्र घालवण्यावर लक्ष केंद्रित करा. कॉस्मिक ऊर्जा कुटुंब सुसंवाद आणि भावनिक जोडणींना अनुकूल आहे.",
                "health_question": "🏥 **आरोग्य मार्गदर्शन**\n\nशारीरिक आणि मानसिक कल्याणावर लक्ष केंद्रित करा. सकाळचे ध्यान सराव करा आणि संतुलित आहार राखा. कॉस्मिक ऊर्जा तुमच्या जीवनशक्ती आणि अंतर्गत शांतीला समर्थन देते.",
                "spiritual_question": "🙏 **आध्यात्मिक मार्गदर्शन**\n\nतुमचा आध्यात्मिक मार्ग स्पष्ट आणि उद्देशपूर्ण आहे. ध्यान, प्रार्थना आणि इतरांची सेवा यावर लक्ष केंद्रित करा. कॉस्मिक ऊर्जा तुमच्या आध्यात्मिक विकास आणि ज्ञानाला समर्थन देते.",
                "career_question": "💼 **करिअर मार्गदर्शन**\n\nतुमचा व्यावसायिक मार्ग अर्थपूर्ण कामाद्वारे इतरांची मदत करण्यावर आहे. सेवा, शिक्षण आणि मार्गदर्शनावर लक्ष केंद्रित करा. कॉस्मिक ऊर्जा तुमच्या नेतृत्व आणि ज्ञानाला समर्थन देते.",
                "general_guidance": "🌟 **वैयक्तिक मार्गदर्शन**\n\nमला वाटते तुम्ही मार्गदर्शन शोधत आहात. तुमच्या कॉस्मिक ऊर्जेवर आधारित, वैयक्तिक विकास, कुटुंब सुसंवाद आणि आध्यात्मिक विकासावर लक्ष केंद्रित करा. तुमच्या अंतर्ज्ञानावर विश्वास ठेवा आणि तुमच्या हृदयाच्या आवाहनाला अनुसरा."
            }
        }
    
    def set_language(self, language: str) -> bool:
        """Set the current language."""
        try:
            if language in ["en", "mr"]:
                self.current_language = Language(language)
                logger.info(f"Language set to {language}")
                return True
            else:
                logger.warning(f"Unsupported language: {language}")
                return False
        except Exception as e:
            logger.error(f"Error setting language: {e}")
            return False
    
    def get_text(self, key: str, language: Optional[str] = None) -> str:
        """Get translated text for given key."""
        try:
            lang = language or self.current_language.value
            if lang in self.translations and key in self.translations[lang]:
                return self.translations[lang][key]
            else:
                # Fallback to English
                return self.translations["en"].get(key, f"Missing translation: {key}")
        except Exception as e:
            logger.error(f"Error getting translation for key {key}: {e}")
            return f"Translation error: {key}"
    
    def get_current_language(self) -> str:
        """Get current language code."""
        return self.current_language.value
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return [lang.value for lang in Language]
    
    def format_message(self, key: str, **kwargs) -> str:
        """Format message with parameters."""
        try:
            message = self.get_text(key)
            return message.format(**kwargs)
        except Exception as e:
            logger.error(f"Error formatting message for key {key}: {e}")
            return self.get_text(key)


# Global multi-language support instance
multi_lang = MultiLanguageSupport() 