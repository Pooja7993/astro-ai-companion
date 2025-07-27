"""
Remedy Engine for Astro AI Companion
Generates personalized remedies based on astrological analysis
"""

from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path
from datetime import datetime

from src.utils.config_simple import Config


class RemedyEngine:
    """Generate personalized remedies based on astrological analysis."""
    
    def __init__(self):
        self.config = Config()
        
        rules_path = Path("config/astrology_rules/vedic_rules.yaml")
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.vedic_rules = yaml.safe_load(f)
    
    def generate_comprehensive_remedies(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive remedy package for a user."""
        
        remedies_package = {
            'immediate_remedies': self._get_immediate_remedies(chart_data, user_profile),
            'master_remedies': self._get_master_remedies(chart_data, user_profile),
            'planetary_remedies': self._get_planetary_remedies(chart_data, user_profile),
            'lal_kitab_remedies': self._get_lal_kitab_remedies(chart_data, user_profile),
            'lifestyle_remedies': self._get_lifestyle_remedies(chart_data, user_profile),
            'gemstone_recommendations': self._get_gemstone_recommendations(chart_data, user_profile),
            'mantra_recommendations': self._get_mantra_recommendations(chart_data, user_profile),
            'donation_schedule': self._get_donation_schedule(chart_data, user_profile),
            'color_therapy': self._get_color_therapy(chart_data, user_profile),
            'dietary_recommendations': self._get_dietary_recommendations(chart_data, user_profile)
        }
        
        return remedies_package
    
    def _get_immediate_remedies(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get remedies that can be implemented immediately."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            immediate_remedies = [
                {
                    'category': 'Spiritual',
                    'title': 'Morning Prayer',
                    'description': 'Start your day with 5 minutes of prayer or meditation facing east.',
                    'duration': 'Daily',
                    'priority': 'High'
                },
                {
                    'category': 'Lifestyle',
                    'title': 'Water Ritual',
                    'description': 'Drink a glass of water while facing the sun every morning.',
                    'duration': 'Daily',
                    'priority': 'High'
                },
                {
                    'category': 'Charity',
                    'title': 'Daily Giving',
                    'description': 'Give something (food, money, help) to someone in need daily.',
                    'duration': 'Daily',
                    'priority': 'Medium'
                }
            ]
        else:
            immediate_remedies = [
                {
                    'category': 'आध्यात्मिक',
                    'title': 'सकाळची प्रार्थना',
                    'description': 'पूर्वेकडे तोंड करून 5 मिनिटे प्रार्थना किंवा ध्यानाने दिवसाची सुरुवात करा.',
                    'duration': 'दैनिक',
                    'priority': 'उच्च'
                },
                {
                    'category': 'जीवनशैली',
                    'title': 'पाण्याचा विधी',
                    'description': 'दर सकाळी सूर्याकडे तोंड करून एक ग्लास पाणी प्या.',
                    'duration': 'दैनिक',
                    'priority': 'उच्च'
                },
                {
                    'category': 'दानधर्म',
                    'title': 'दैनिक दान',
                    'description': 'दररोज गरजूंना काहीतरी (अन्न, पैसे, मदत) द्या.',
                    'duration': 'दैनिक',
                    'priority': 'मध्यम'
                }
            ]
        
        return immediate_remedies
    
    def _get_master_remedies(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get 5 master remedies that solve 80% of issues."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            master_remedies = [
                {
                    'category': 'Spiritual Foundation',
                    'title': 'Daily Meditation & Prayer',
                    'description': 'Practice 15-20 minutes of meditation and prayer daily at sunrise. This harmonizes all planetary energies and creates a protective spiritual shield.',
                    'effectiveness': '90%',
                    'issues_addressed': ['Mental peace', 'Spiritual growth', 'Overall protection']
                },
                {
                    'category': 'Karmic Cleansing',
                    'title': 'Weekly Service & Donation',
                    'description': 'Serve food to the needy every Saturday and donate according to your capacity. This removes negative karma and attracts divine blessings.',
                    'effectiveness': '85%',
                    'issues_addressed': ['Karmic debts', 'Financial blocks', 'Relationship harmony']
                },
                {
                    'category': 'Planetary Strengthening',
                    'title': 'Primary Gemstone Therapy',
                    'description': 'Wear your ascendant lord gemstone in the appropriate metal and finger. This strengthens your core personality and life force.',
                    'effectiveness': '80%',
                    'issues_addressed': ['Personal power', 'Health', 'Confidence']
                },
                {
                    'category': 'Energy Alignment',
                    'title': 'Sunrise Water Ritual',
                    'description': 'Face east and drink water while chanting your personal mantra every sunrise. This aligns you with cosmic rhythms and solar energy.',
                    'effectiveness': '75%',
                    'issues_addressed': ['Energy levels', 'Mental clarity', 'Spiritual connection']
                },
                {
                    'category': 'Universal Harmony',
                    'title': 'Gayatri Mantra Practice',
                    'description': 'Chant Gayatri Mantra 108 times daily, preferably during sunrise or sunset. This universal mantra purifies all aspects of life.',
                    'effectiveness': '85%',
                    'issues_addressed': ['Wisdom', 'Protection', 'Overall well-being']
                }
            ]
        else:
            master_remedies = [
                {
                    'category': 'आध्यात्मिक पाया',
                    'title': 'दैनिक ध्यान आणि प्रार्थना',
                    'description': 'सूर्योदयाच्या वेळी दररोज 15-20 मिनिटे ध्यान आणि प्रार्थना करा. हे सर्व ग्रहांची ऊर्जा संतुलित करते आणि संरक्षणात्मक आध्यात्मिक ढाल तयार करते.',
                    'effectiveness': '90%',
                    'issues_addressed': ['मानसिक शांती', 'आध्यात्मिक वाढ', 'एकूण संरक्षण']
                },
                {
                    'category': 'कर्म शुद्धीकरण',
                    'title': 'साप्ताहिक सेवा आणि दान',
                    'description': 'दर शनिवारी गरजूंना अन्न परोसा आणि आपल्या क्षमतेनुसार दान करा. हे नकारात्मक कर्म काढून टाकते आणि दैवी आशीर्वाद आकर्षित करते.',
                    'effectiveness': '85%',
                    'issues_addressed': ['कर्म कर्जे', 'आर्थिक अडथळे', 'नातेसंबंध सामंजस्य']
                },
                {
                    'category': 'ग्रह बळकटीकरण',
                    'title': 'प्राथमिक रत्न चिकित्सा',
                    'description': 'आपल्या लग्नेशाचे रत्न योग्य धातू आणि बोटात धारण करा. हे आपले मूळ व्यक्तिमत्व आणि जीवनशक्ती मजबूत करते.',
                    'effectiveness': '80%',
                    'issues_addressed': ['वैयक्तिक शक्ती', 'आरोग्य', 'आत्मविश्वास']
                },
                {
                    'category': 'ऊर्जा संरेखन',
                    'title': 'सूर्योदय पाणी विधी',
                    'description': 'पूर्वेकडे तोंड करून दर सूर्योदयाला आपल्या वैयक्तिक मंत्राचा जप करत पाणी प्या. हे आपल्याला वैश्विक लय आणि सौर ऊर्जेशी जोडते.',
                    'effectiveness': '75%',
                    'issues_addressed': ['ऊर्जा पातळी', 'मानसिक स्पष्टता', 'आध्यात्मिक कनेक्शन']
                },
                {
                    'category': 'सार्वत्रिक सामंजस्य',
                    'title': 'गायत्री मंत्र साधना',
                    'description': 'दररोज गायत्री मंत्राचा 108 वेळा जप करा, शक्यतो सूर्योदय किंवा सूर्यास्ताच्या वेळी. हा सार्वत्रिक मंत्र जीवनाच्या सर्व पैलूंना शुद्ध करतो.',
                    'effectiveness': '85%',
                    'issues_addressed': ['बुद्धी', 'संरक्षण', 'एकूण कल्याण']
                }
            ]
        
        return master_remedies
    
    def _get_planetary_remedies(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Get specific remedies for each planet."""
        language = user_profile.get('preferred_language', 'en')
        planetary_positions = chart_data.get('planetary_positions', {})
        
        planetary_remedies = {}
        
        for planet, data in planetary_positions.items():
            dignity = data.get('dignity', 'neutral')
            
            if dignity in ['debilitated', 'enemy']:
                remedies = self._get_specific_planet_remedies(planet, language)
                if remedies:
                    planetary_remedies[planet] = remedies
        
        return planetary_remedies
    
    def _get_lal_kitab_remedies(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get Lal Kitab specific remedies."""
        language = user_profile.get('preferred_language', 'en')
        lal_kitab_analysis = chart_data.get('lal_kitab_analysis', {})
        
        remedies = []
        
        if lal_kitab_analysis.get('manglik_status') == 'Manglik':
            if language == 'en':
                remedies.extend([
                    {
                        'category': 'Lal Kitab',
                        'title': 'Mars Pacification',
                        'description': 'Donate red lentils and jaggery every Tuesday to reduce Mars malefic effects.',
                        'frequency': 'Weekly'
                    },
                    {
                        'category': 'Lal Kitab',
                        'title': 'Hanuman Worship',
                        'description': 'Visit Hanuman temple every Tuesday and offer sindoor and oil.',
                        'frequency': 'Weekly'
                    }
                ])
            else:
                remedies.extend([
                    {
                        'category': 'लाल किताब',
                        'title': 'मंगळ शांती',
                        'description': 'मंगळाचे दुष्प्रभाव कमी करण्यासाठी दर मंगळवारी लाल डाळ आणि गूळ दान करा.',
                        'frequency': 'साप्ताहिक'
                    },
                    {
                        'category': 'लाल किताब',
                        'title': 'हनुमान पूजा',
                        'description': 'दर मंगळवारी हनुमान मंदिरात जाऊन सिंदूर आणि तेल अर्पण करा.',
                        'frequency': 'साप्ताहिक'
                    }
                ])
        
        return remedies
    
    def _get_lifestyle_remedies(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get lifestyle-based remedies."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            lifestyle_remedies = [
                {
                    'category': 'Daily Routine',
                    'title': 'Early Rising',
                    'description': 'Wake up during Brahma Muhurta (4-6 AM) for maximum cosmic energy absorption.',
                    'benefits': 'Increased vitality, mental clarity, spiritual growth'
                },
                {
                    'category': 'Diet',
                    'title': 'Sattvic Food',
                    'description': 'Consume fresh, vegetarian, and naturally prepared foods. Avoid processed and stale food.',
                    'benefits': 'Better health, mental peace, spiritual progress'
                },
                {
                    'category': 'Exercise',
                    'title': 'Yoga & Pranayama',
                    'description': 'Practice yoga asanas and breathing exercises daily for 30 minutes.',
                    'benefits': 'Physical strength, emotional balance, energy flow'
                }
            ]
        else:
            lifestyle_remedies = [
                {
                    'category': 'दैनिक दिनचर्या',
                    'title': 'लवकर उठणे',
                    'description': 'जास्तीत जास्त वैश्विक ऊर्जा शोषणासाठी ब्रह्म मुहूर्तात (4-6 AM) उठा.',
                    'benefits': 'वाढलेली चैतन्य, मानसिक स्पष्टता, आध्यात्मिक वाढ'
                },
                {
                    'category': 'आहार',
                    'title': 'सात्विक अन्न',
                    'description': 'ताजे, शाकाहारी आणि नैसर्गिकरित्या तयार केलेले अन्न घ्या. प्रक्रिया केलेले आणि शिळे अन्न टाळा.',
                    'benefits': 'चांगले आरोग्य, मानसिक शांती, आध्यात्मिक प्रगती'
                },
                {
                    'category': 'व्यायाम',
                    'title': 'योग आणि प्राणायाम',
                    'description': 'दररोज 30 मिनिटे योगासने आणि श्वासोच्छवासाचे व्यायाम करा.',
                    'benefits': 'शारीरिक शक्ती, भावनिक संतुलन, ऊर्जा प्रवाह'
                }
            ]
        
        return lifestyle_remedies
    
    def _get_gemstone_recommendations(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed gemstone recommendations."""
        language = user_profile.get('preferred_language', 'en')
        basic_info = chart_data.get('basic_info', {})
        
        if language == 'en':
            recommendations = {
                'primary_gemstone': {
                    'name': 'Ruby',
                    'weight': '3-5 carats',
                    'metal': 'Gold',
                    'finger': 'Ring finger',
                    'day_to_wear': 'Sunday',
                    'benefits': 'Strengthens personality, improves health, enhances confidence'
                },
                'alternative_gemstones': [
                    'Red Garnet (Ruby substitute)',
                    'White Sapphire (Diamond substitute)',
                    'Green Tourmaline (Emerald substitute)'
                ]
            }
        else:
            recommendations = {
                'primary_gemstone': {
                    'name': 'माणिक',
                    'weight': '3-5 कॅरेट',
                    'metal': 'सोने',
                    'finger': 'अनामिका',
                    'day_to_wear': 'रविवार',
                    'benefits': 'व्यक्तिमत्व मजबूत करते, आरोग्य सुधारते, आत्मविश्वास वाढवते'
                },
                'alternative_gemstones': [
                    'लाल गार्नेट (माणिकाचा पर्याय)',
                    'पांढरा नीलम (हिऱ्याचा पर्याय)',
                    'हिरवा टूर्मलाइन (पन्न्याचा पर्याय)'
                ]
            }
        
        return recommendations
    
    def _get_mantra_recommendations(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> List[Dict[str, str]]:
        """Get personalized mantra recommendations."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            mantras = [
                {
                    'category': 'Universal',
                    'mantra': 'Om Gam Ganapataye Namaha',
                    'purpose': 'Remove obstacles and bring success',
                    'repetitions': '108 times daily',
                    'best_time': 'Morning'
                },
                {
                    'category': 'Wisdom',
                    'mantra': 'Gayatri Mantra',
                    'purpose': 'Enhance wisdom and spiritual growth',
                    'repetitions': '108 times daily',
                    'best_time': 'Sunrise or Sunset'
                }
            ]
        else:
            mantras = [
                {
                    'category': 'सार्वत्रिक',
                    'mantra': 'ॐ गं गणपतये नमः',
                    'purpose': 'अडथळे दूर करणे आणि यश आणणे',
                    'repetitions': 'दररोज 108 वेळा',
                    'best_time': 'सकाळ'
                },
                {
                    'category': 'बुद्धी',
                    'mantra': 'गायत्री मंत्र',
                    'purpose': 'बुद्धी आणि आध्यात्मिक वाढ वाढवणे',
                    'repetitions': 'दररोज 108 वेळा',
                    'best_time': 'सूर्योदय किंवा सूर्यास्त'
                }
            ]
        
        return mantras
    
    def _get_donation_schedule(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Get weekly donation schedule."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            schedule = {
                'Sunday': [{'item': 'Wheat and Jaggery', 'purpose': 'Strengthen Sun energy', 'quantity': '1 kg each'}],
                'Monday': [{'item': 'Rice and Milk', 'purpose': 'Strengthen Moon energy', 'quantity': '1 kg rice, 1 liter milk'}],
                'Tuesday': [{'item': 'Red Lentils', 'purpose': 'Pacify Mars energy', 'quantity': '1 kg'}],
                'Wednesday': [{'item': 'Green Vegetables', 'purpose': 'Strengthen Mercury energy', 'quantity': 'As per capacity'}],
                'Thursday': [{'item': 'Turmeric and Yellow Items', 'purpose': 'Strengthen Jupiter energy', 'quantity': '500g turmeric'}],
                'Friday': [{'item': 'Sugar and White Items', 'purpose': 'Strengthen Venus energy', 'quantity': '1 kg sugar'}],
                'Saturday': [{'item': 'Mustard Oil and Black Items', 'purpose': 'Pacify Saturn energy', 'quantity': '1 liter oil'}]
            }
        else:
            schedule = {
                'रविवार': [{'item': 'गहू आणि गूळ', 'purpose': 'सूर्य ऊर्जा मजबूत करणे', 'quantity': 'प्रत्येकी 1 किलो'}],
                'सोमवार': [{'item': 'तांदूळ आणि दूध', 'purpose': 'चंद्र ऊर्जा मजबूत करणे', 'quantity': '1 किलो तांदूळ, 1 लिटर दूध'}],
                'मंगळवार': [{'item': 'लाल डाळ', 'purpose': 'मंगळ ऊर्जा शांत करणे', 'quantity': '1 किलो'}],
                'बुधवार': [{'item': 'हिरव्या भाज्या', 'purpose': 'बुध ऊर्जा मजबूत करणे', 'quantity': 'क्षमतेनुसार'}],
                'गुरुवार': [{'item': 'हळद आणि पिवळ्या वस्तू', 'purpose': 'गुरु ऊर्जा मजबूत करणे', 'quantity': '500 ग्रॅम हळद'}],
                'शुक्रवार': [{'item': 'साखर आणि पांढर्या वस्तू', 'purpose': 'शुक्र ऊर्जा मजबूत करणे', 'quantity': '1 किलो साखर'}],
                'शनिवार': [{'item': 'मोहरीचे तेल आणि काळ्या वस्तू', 'purpose': 'शनि ऊर्जा शांत करणे', 'quantity': '1 लिटर तेल'}]
            }
        
        return schedule
    
    def _get_color_therapy(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get color therapy recommendations."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            color_therapy = {
                'primary_colors': ['white', 'yellow', 'red'],
                'avoid_colors': ['black', 'dark_blue'],
                'daily_recommendations': {
                    'clothing': "Wear bright, positive colors for enhanced energy",
                    'home_decor': "Use recommended colors in your living space",
                    'meditation': "Visualize golden light during meditation"
                }
            }
        else:
            color_therapy = {
                'primary_colors': ['पांढरा', 'पिवळा', 'लाल'],
                'avoid_colors': ['काळा', 'गडद निळा'],
                'daily_recommendations': {
                    'clothing': "वाढीव ऊर्जेसाठी चमकदार, सकारात्मक रंगाचे कपडे घाला",
                    'home_decor': "आपल्या राहण्याच्या जागेत शिफारस केलेले रंग वापरा",
                    'meditation': "ध्यानादरम्यान सुवर्ण प्रकाशाची कल्पना करा"
                }
            }
        
        return color_therapy
    
    def _get_dietary_recommendations(self, chart_data: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get dietary recommendations based on astrological analysis."""
        language = user_profile.get('preferred_language', 'en')
        
        if language == 'en':
            dietary_recommendations = {
                'beneficial_foods': ['Fresh fruits and vegetables', 'Whole grains and legumes', 'Dairy products', 'Nuts and seeds', 'Herbal teas'],
                'foods_to_avoid': ['Processed foods', 'Excessive spicy food', 'Stale food', 'Excessive caffeine', 'Non-vegetarian food'],
                'eating_guidelines': ['Eat at regular times', 'Chew slowly', 'Avoid eating during stress', 'Drink water before meals', 'Express gratitude before eating']
            }
        else:
            dietary_recommendations = {
                'beneficial_foods': ['ताजी फळे आणि भाज्या', 'संपूर्ण धान्य आणि डाळी', 'दुग्धजन्य पदार्थ', 'काजू आणि बिया', 'हर्बल चहा'],
                'foods_to_avoid': ['प्रक्रिया केलेले अन्न', 'जास्त तिखट अन्न', 'शिळे अन्न', 'जास्त कॅफिन', 'मांसाहारी अन्न'],
                'eating_guidelines': ['नियमित वेळी जेवा', 'हळूहळू चावा', 'तणावात खाणे टाळा', 'जेवणापूर्वी पाणी प्या', 'खाण्यापूर्वी कृतज्ञता व्यक्त करा']
            }
        
        return dietary_recommendations
    
    def _get_specific_planet_remedies(self, planet: str, language: str) -> List[Dict[str, str]]:
        """Get specific remedies for a planet."""
        if language == 'en':
            remedies_map = {
                'sun': [
                    {'category': 'Worship', 'title': 'Sun Worship', 'description': 'Offer water to Sun every morning while chanting Surya mantras.'},
                    {'category': 'Gemstone', 'title': 'Ruby', 'description': 'Wear ruby in gold ring on ring finger on Sunday morning.'},
                    {'category': 'Donation', 'title': 'Wheat & Jaggery', 'description': 'Donate wheat, jaggery, and copper items on Sundays.'}
                ],
                'moon': [
                    {'category': 'Worship', 'title': 'Moon Worship', 'description': 'Offer milk and white flowers to Moon on Monday evenings.'},
                    {'category': 'Gemstone', 'title': 'Pearl', 'description': 'Wear pearl in silver ring on little finger on Monday morning.'},
                    {'category': 'Donation', 'title': 'Rice & Milk', 'description': 'Donate rice, milk, and silver items on Mondays.'}
                ]
            }
        else:
            remedies_map = {
                'sun': [
                    {'category': 'पूजा', 'title': 'सूर्य पूजा', 'description': 'दर सकाळी सूर्य मंत्र जपत सूर्याला पाणी अर्पण करा.'},
                    {'category': 'रत्न', 'title': 'माणिक', 'description': 'रविवारी सकाळी अनामिकेत सोन्याच्या अंगठीत माणिक धारण करा.'},
                    {'category': 'दान', 'title': 'गहू आणि गूळ', 'description': 'रविवारी गहू, गूळ आणि तांब्याच्या वस्तू दान करा.'}
                ],
                'moon': [
                    {'category': 'पूजा', 'title': 'चंद्र पूजा', 'description': 'सोमवारी संध्याकाळी चंद्राला दूध आणि पांढरी फुले अर्पण करा.'},
                    {'category': 'रत्न', 'title': 'मोती', 'description': 'सोमवारी सकाळी करिंगळीत चांदीच्या अंगठीत मोती धारण करा.'},
                    {'category': 'दान', 'title': 'तांदूळ आणि दूध', 'description': 'सोमवारी तांदूळ, दूध आणि चांदीच्या वस्तू दान करा.'}
                ]
            }
        
        return remedies_map.get(planet, [])
