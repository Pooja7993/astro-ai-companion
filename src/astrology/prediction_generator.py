"""
Prediction Generator for Astro AI Companion
Generates personalized predictions based on chart analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any
import random
import yaml
from pathlib import Path

from src.utils.config import Config


class PredictionGenerator:
    """Generate personalized astrological predictions."""
    
    def __init__(self):
        self.config = Config()
        
        rules_path = Path("config/astrology_rules/vedic_rules.yaml")
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.vedic_rules = yaml.safe_load(f)
        
        translations_path = Path("config/languages/translations.yaml")
        with open(translations_path, 'r', encoding='utf-8') as f:
            self.translations = yaml.safe_load(f)
    
    def generate_prediction(self, chart_data: Dict[str, Any], prediction_type: str, language: str = 'en') -> str:
        """Generate prediction based on chart analysis."""
        try:
            content = self._generate_content(chart_data, prediction_type, language)
            return content
            
        except Exception as e:
            return f"Error generating prediction: {str(e)}"
    
    def _generate_content(self, chart_data: Dict[str, Any], prediction_type: str, language: str) -> str:
        """Generate prediction content based on type."""
        if prediction_type == 'daily':
            return self._generate_daily_prediction(chart_data, language)
        elif prediction_type == 'weekly':
            return self._generate_weekly_prediction(chart_data, language)
        elif prediction_type == 'monthly':
            return self._generate_monthly_prediction(chart_data, language)
        elif prediction_type == 'quarterly':
            return self._generate_quarterly_prediction(chart_data, language)
        elif prediction_type == 'annual':
            return self._generate_annual_prediction(chart_data, language)
        else:
            return self._generate_daily_prediction(chart_data, language)
    
    def _generate_daily_prediction(self, chart_data: Dict[str, Any], language: str) -> str:
        """Generate daily prediction."""
        lang_key = 'english' if language == 'en' else 'marathi'
        
        planets = chart_data.get('planetary_positions', {})
        strengths = chart_data.get('strengths_weaknesses', {}).get('strengths', [])
        
        dominant_planet = self._get_dominant_planet(planets)
        
        predictions = {
            'en': {
                'sun': "Today brings opportunities for leadership and recognition. Your confidence will shine through in all endeavors. Focus on important decisions and avoid conflicts.",
                'moon': "Emotional clarity and intuitive insights guide you today. Family matters may require attention. Trust your instincts in personal relationships.",
                'mars': "Energy and determination drive your actions today. Physical activities and competitive situations favor you. Channel your passion constructively.",
                'mercury': "Communication and learning are highlighted today. Business dealings and negotiations show promise. Express your ideas clearly.",
                'jupiter': "Wisdom and good fortune accompany you today. Educational pursuits and spiritual activities bring satisfaction. Share your knowledge with others.",
                'venus': "Love, beauty, and creativity flow abundantly today. Artistic endeavors and social connections flourish. Enjoy life's pleasures in moderation.",
                'saturn': "Discipline and hard work pay off today. Long-term projects show progress. Patience and persistence lead to lasting achievements."
            },
            'mr': {
                'sun': "आज नेतृत्व आणि मान्यतेच्या संधी येतील. आपला आत्मविश्वास सर्व कामांमध्ये चमकेल. महत्वाच्या निर्णयांवर लक्ष द्या आणि संघर्ष टाळा.",
                'moon': "आज भावनिक स्पष्टता आणि अंतर्ज्ञान आपले मार्गदर्शन करेल. कौटुंबिक बाबींवर लक्ष देण्याची गरज असू शकते. वैयक्तिक नातेसंबंधांमध्ये आपल्या अंतर्ज्ञानावर विश्वास ठेवा.",
                'mars': "आज ऊर्जा आणि दृढनिश्चय आपल्या कृतींना चालना देईल. शारीरिक क्रियाकलाप आणि स्पर्धात्मक परिस्थिती आपल्या बाजूने असेल. आपल्या उत्कटतेचा रचनात्मक वापर करा.",
                'mercury': "आज संवाद आणि शिक्षणावर भर असेल. व्यावसायिक व्यवहार आणि वाटाघाटी आशादायक दिसतात. आपले विचार स्पष्टपणे मांडा.",
                'jupiter': "आज ज्ञान आणि सुदैव आपल्यासोबत असेल. शैक्षणिक कार्य आणि आध्यात्मिक क्रियाकलाप समाधान देतील. आपले ज्ञान इतरांसोबत सामायिक करा.",
                'venus': "आज प्रेम, सौंदर्य आणि सर्जनशीलता भरपूर प्रमाणात वाहेल. कलात्मक कार्य आणि सामाजिक संपर्क फुलतील. जीवनातील आनंदाचा मर्यादित आस्वाद घ्या.",
                'saturn': "आज शिस्त आणि कठोर परिश्रम फळ देईल. दीर्घकालीन प्रकल्प प्रगती दाखवतील. धैर्य आणि चिकाटी चिरस्थायी यश मिळवून देईल."
            }
        }
        
        base_prediction = predictions.get(language, predictions['en']).get(dominant_planet, predictions[language]['sun'])
        
        additional_insights = self._get_daily_insights(chart_data, language)
        
        return f"{base_prediction}\n\n{additional_insights}"
    
    def _generate_weekly_prediction(self, chart_data: Dict[str, Any], language: str) -> str:
        """Generate weekly prediction."""
        lang_key = 'english' if language == 'en' else 'marathi'
        
        if language == 'en':
            return """This week brings a blend of opportunities and challenges. The first half focuses on professional growth and recognition. Mid-week may present some obstacles that require patience and strategic thinking.

Key Areas:
• Career: Advancement opportunities emerge
• Relationships: Communication improves significantly  
• Health: Maintain balance between work and rest
• Finance: Conservative approach recommended

The weekend promises relaxation and quality time with loved ones."""
        else:
            return """या आठवड्यात संधी आणि आव्हाने यांचे मिश्रण असेल. पहिला अर्धा भाग व्यावसायिक वाढ आणि मान्यतेवर केंद्रित असेल. आठवड्याच्या मध्यात काही अडथळे येऊ शकतात ज्यासाठी धैर्य आणि रणनीतिक विचारांची गरज असेल.

मुख्य क्षेत्रे:
• करिअर: प्रगतीच्या संधी उदयास येतील
• नातेसंबंध: संवाद लक्षणीयरीत्या सुधारेल
• आरोग्य: काम आणि विश्रांती यांच्यात संतुलन राखा
• अर्थकारण: पुराणमतवादी दृष्टिकोन शिफारसीय

आठवड्याच्या शेवटी विश्रांती आणि प्रियजनांसोबत दर्जेदार वेळ घालवण्याचे वचन आहे."""
    
    def _generate_monthly_prediction(self, chart_data: Dict[str, Any], language: str) -> str:
        """Generate monthly prediction."""
        if language == 'en':
            return """This month marks a significant period of transformation and growth. The planetary alignments suggest major developments in your personal and professional life.

First Week: New beginnings and fresh opportunities
Second Week: Consolidation and building foundations  
Third Week: Challenges that test your resolve
Fourth Week: Rewards and recognition for your efforts

Focus Areas:
• Embrace change with confidence
• Strengthen important relationships
• Invest in long-term goals
• Practice patience during difficult phases

Overall, this month sets the stage for future success."""
        else:
            return """हा महिना परिवर्तन आणि वाढीचा महत्त्वपूर्ण काळ आहे. ग्रहांची स्थिती आपल्या वैयक्तिक आणि व्यावसायिक जीवनात मोठे बदल सूचित करते.

पहिला आठवडा: नवीन सुरुवात आणि ताज्या संधी
दुसरा आठवडा: एकत्रीकरण आणि पाया बांधणे
तिसरा आठवडा: आपल्या दृढतेची परीक्षा घेणारी आव्हाने
चौथा आठवडा: आपल्या प्रयत्नांसाठी बक्षिसे आणि मान्यता

लक्ष केंद्रित करण्याची क्षेत्रे:
• आत्मविश्वासाने बदल स्वीकारा
• महत्त्वाचे नातेसंबंध मजबूत करा
• दीर्घकालीन उद्दिष्टांमध्ये गुंतवणूक करा
• कठीण टप्प्यांमध्ये धैर्य पाळा

एकूणच, हा महिना भविष्यातील यशासाठी पायाभरणी करतो."""
    
    def _generate_quarterly_prediction(self, chart_data: Dict[str, Any], language: str) -> str:
        """Generate quarterly prediction."""
        if language == 'en':
            return """The next three months present a powerful cycle of growth and achievement. Major planetary transits indicate significant life changes and opportunities for advancement.

Month 1: Foundation building and planning
Month 2: Active implementation and progress
Month 3: Completion and new beginnings

Key Themes:
• Professional recognition and career advancement
• Strengthening of personal relationships
• Financial stability and growth
• Health and vitality improvements
• Spiritual and personal development

This quarter emphasizes the importance of balance between ambition and wisdom."""
        else:
            return """पुढील तीन महिने वाढ आणि यशाचे शक्तिशाली चक्र सादर करतात. मुख्य ग्रह संक्रमणे जीवनातील महत्त्वपूर्ण बदल आणि प्रगतीच्या संधी दर्शवितात.

महिना 1: पायाभरणी आणि नियोजन
महिना 2: सक्रिय अंमलबजावणी आणि प्रगती
महिना 3: पूर्णता आणि नवीन सुरुवात

मुख्य विषय:
• व्यावसायिक मान्यता आणि करिअर प्रगती
• वैयक्तिक नातेसंबंधांचे बळकटीकरण
• आर्थिक स्थिरता आणि वाढ
• आरोग्य आणि चैतन्य सुधारणा
• आध्यात्मिक आणि वैयक्तिक विकास

या तिमाहीत महत्त्वाकांक्षा आणि शहाणपण यांच्यातील संतुलनाचे महत्त्व अधोरेखित केले आहे."""
    
    def _generate_annual_prediction(self, chart_data: Dict[str, Any], language: str) -> str:
        """Generate annual prediction."""
        if language == 'en':
            return """This year promises to be transformative with significant achievements and personal growth. The annual chart reveals multiple opportunities for advancement across all life areas.

First Quarter: New ventures and fresh starts
Second Quarter: Steady progress and relationship building
Third Quarter: Challenges that strengthen character
Fourth Quarter: Harvest time with rewards and recognition

Major Themes:
• Career reaches new heights with leadership opportunities
• Personal relationships deepen and mature
• Financial growth through wise investments
• Health improvements through lifestyle changes
• Spiritual awakening and inner wisdom development

This year marks a turning point toward greater fulfillment and success."""
        else:
            return """हे वर्ष महत्त्वपूर्ण यश आणि वैयक्तिक वाढीसह परिवर्तनकारी असण्याचे वचन देते. वार्षिक कुंडली जीवनाच्या सर्व क्षेत्रांमध्ये प्रगतीच्या अनेक संधी प्रकट करते.

पहिली तिमाही: नवीन उपक्रम आणि ताजी सुरुवात
दुसरी तिमाही: स्थिर प्रगती आणि नातेसंबंध निर्माण
तिसरी तिमाही: चारित्र्य मजबूत करणारी आव्हाने
चौथी तिमाही: बक्षिसे आणि मान्यतेसह कापणीचा काळ

मुख्य विषय:
• नेतृत्वाच्या संधींसह करिअर नवीन उंची गाठते
• वैयक्तिक नातेसंबंध खोल आणि परिपक्व होतात
• शहाणपणाच्या गुंतवणुकीद्वारे आर्थिक वाढ
• जीवनशैलीतील बदलांद्वारे आरोग्य सुधारणा
• आध्यात्मिक जागृती आणि अंतर्ज्ञान विकास

हे वर्ष अधिक समाधान आणि यशाच्या दिशेने एक वळणाचा मुद्दा आहे."""
    
    def _generate_remedies(self, chart_data: Dict[str, Any], language: str) -> List[Dict[str, str]]:
        """Generate personalized remedies."""
        remedies = []
        
        weaknesses = chart_data.get('strengths_weaknesses', {}).get('weaknesses', [])
        planets = chart_data.get('planetary_positions', {})
        
        for planet, data in planets.items():
            if data.get('dignity') in ['debilitated', 'enemy']:
                planet_remedies = self._get_planet_remedies(planet, language)
                remedies.extend(planet_remedies[:2])  # Max 2 remedies per planet
        
        if not remedies:
            remedies = self._get_general_remedies(language)
        
        return remedies[:5]  # Max 5 remedies total
    
    def _generate_master_remedies(self, chart_data: Dict[str, Any], language: str) -> List[Dict[str, str]]:
        """Generate 5 master remedies that solve 80% of issues."""
        if language == 'en':
            master_remedies = [
                {
                    'category': 'Spiritual',
                    'title': 'Daily Meditation',
                    'description': 'Practice 15 minutes of meditation daily at sunrise. This harmonizes all planetary energies and brings mental peace.'
                },
                {
                    'category': 'Gemstone',
                    'title': 'Primary Gemstone',
                    'description': 'Wear your ascendant lord gemstone on the appropriate finger. This strengthens your overall personality and life force.'
                },
                {
                    'category': 'Charity',
                    'title': 'Weekly Donation',
                    'description': 'Donate food to the needy every Saturday. This removes negative karma and attracts positive energy.'
                },
                {
                    'category': 'Mantra',
                    'title': 'Gayatri Mantra',
                    'description': 'Chant Gayatri Mantra 108 times daily. This universal mantra purifies the mind and enhances wisdom.'
                },
                {
                    'category': 'Lifestyle',
                    'title': 'Sunrise Routine',
                    'description': 'Wake up before sunrise and face east while drinking water. This aligns you with cosmic rhythms and solar energy.'
                }
            ]
        else:
            master_remedies = [
                {
                    'category': 'आध्यात्मिक',
                    'title': 'दैनिक ध्यान',
                    'description': 'सूर्योदयाच्या वेळी दररोज 15 मिनिटे ध्यान करा. हे सर्व ग्रहांची ऊर्जा संतुलित करते आणि मानसिक शांती आणते.'
                },
                {
                    'category': 'रत्न',
                    'title': 'मुख्य रत्न',
                    'description': 'आपल्या लग्नेशाचे रत्न योग्य बोटात धारण करा. हे आपले एकूण व्यक्तिमत्व आणि जीवनशक्ती मजबूत करते.'
                },
                {
                    'category': 'दानधर्म',
                    'title': 'साप्ताहिक दान',
                    'description': 'दर शनिवारी गरजूंना अन्न दान करा. हे नकारात्मक कर्म काढून टाकते आणि सकारात्मक ऊर्जा आकर्षित करते.'
                },
                {
                    'category': 'मंत्र',
                    'title': 'गायत्री मंत्र',
                    'description': 'दररोज गायत्री मंत्राचा 108 वेळा जप करा. हा सार्वत्रिक मंत्र मन शुद्ध करतो आणि बुद्धी वाढवतो.'
                },
                {
                    'category': 'जीवनशैली',
                    'title': 'सूर्योदय दिनचर्या',
                    'description': 'सूर्योदयापूर्वी उठा आणि पूर्वेकडे तोंड करून पाणी प्या. हे आपल्याला वैश्विक लय आणि सौर ऊर्जेशी जोडते.'
                }
            ]
        
        return master_remedies
    
    def _generate_lucky_elements(self, chart_data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Generate lucky elements for the user."""
        planets = chart_data.get('planetary_positions', {})
        dominant_planet = self._get_dominant_planet(planets)
        
        lucky_elements = {
            'en': {
                'colors': self.vedic_rules['remedies']['colors'].get(dominant_planet, ['white', 'yellow']),
                'numbers': [1, 3, 5, 8, 9],
                'days': ['Sunday', 'Tuesday', 'Thursday'],
                'gemstones': self.vedic_rules['remedies']['gemstones'].get(dominant_planet, ['pearl']),
                'directions': ['East', 'North']
            },
            'mr': {
                'colors': self.vedic_rules['remedies']['colors'].get(dominant_planet, ['पांढरा', 'पिवळा']),
                'numbers': [1, 3, 5, 8, 9],
                'days': ['रविवार', 'मंगळवार', 'गुरुवार'],
                'gemstones': self.vedic_rules['remedies']['gemstones'].get(dominant_planet, ['मोती']),
                'directions': ['पूर्व', 'उत्तर']
            }
        }
        
        return lucky_elements.get(language, lucky_elements['en'])
    
    def _get_dominant_planet(self, planets: Dict[str, Any]) -> str:
        """Determine the most influential planet in the chart."""
        best_planet = 'sun'
        best_score = 0
        
        dignity_scores = {
            'exalted': 5,
            'own_sign': 4,
            'friendly': 3,
            'neutral': 2,
            'enemy': 1,
            'debilitated': 0
        }
        
        for planet, data in planets.items():
            dignity = data.get('dignity', 'neutral')
            score = dignity_scores.get(dignity, 2)
            
            if score > best_score:
                best_score = score
                best_planet = planet
        
        return best_planet
    
    def _get_daily_insights(self, chart_data: Dict[str, Any], language: str) -> str:
        """Get additional daily insights."""
        numerology = chart_data.get('numerology', {})
        life_path = numerology.get('life_path_number', 1)
        
        insights = {
            'en': {
                1: "Your leadership qualities are highlighted today. Take initiative in important matters.",
                2: "Cooperation and partnerships bring success today. Avoid conflicts and seek harmony.",
                3: "Creative expression and communication flow freely today. Share your ideas with confidence.",
                4: "Focus on building solid foundations today. Practical matters require attention.",
                5: "Adventure and learning opportunities present themselves. Embrace new experiences.",
                6: "Service to others brings fulfillment today. Focus on helping and healing.",
                7: "Spiritual insights and inner wisdom guide your decisions today.",
                8: "Material success and recognition are within reach. Stay focused on your goals.",
                9: "Completion and new beginnings mark this day. Trust the natural cycles of life."
            },
            'mr': {
                1: "आज आपले नेतृत्व गुण अधोरेखित आहेत. महत्त्वाच्या बाबींमध्ये पुढाकार घ्या.",
                2: "आज सहकार्य आणि भागीदारी यश आणते. संघर्ष टाळा आणि सामंजस्य शोधा.",
                3: "आज सर्जनशील अभिव्यक्ती आणि संवाद मुक्तपणे वाहतो. आत्मविश्वासाने आपले विचार सामायिक करा.",
                4: "आज भक्कम पाया बांधण्यावर लक्ष केंद्रित करा. व्यावहारिक बाबींवर लक्ष देण्याची गरज आहे.",
                5: "साहस आणि शिकण्याच्या संधी स्वतःला सादर करतात. नवीन अनुभव स्वीकारा.",
                6: "आज इतरांची सेवा करणे समाधान आणते. मदत आणि उपचार यावर लक्ष केंद्रित करा.",
                7: "आध्यात्मिक अंतर्दृष्टी आणि अंतर्ज्ञान आज आपल्या निर्णयांचे मार्गदर्शन करते.",
                8: "भौतिक यश आणि मान्यता आवाक्यात आहे. आपल्या उद्दिष्टांवर लक्ष केंद्रित करा.",
                9: "पूर्णता आणि नवीन सुरुवात या दिवसाची वैशिष्ट्ये आहेत. जीवनाच्या नैसर्गिक चक्रांवर विश्वास ठेवा."
            }
        }
        
        return insights.get(language, insights['en']).get(life_path, insights[language][1])
    
    def _get_planet_remedies(self, planet: str, language: str) -> List[Dict[str, str]]:
        """Get remedies for a specific planet."""
        if language == 'en':
            planet_remedies = {
                'sun': [
                    {'category': 'Gemstone', 'title': 'Ruby', 'description': 'Wear ruby in gold ring on Sunday morning to strengthen Sun energy.'},
                    {'category': 'Donation', 'title': 'Wheat Donation', 'description': 'Donate wheat and jaggery to needy people on Sundays.'}
                ],
                'moon': [
                    {'category': 'Gemstone', 'title': 'Pearl', 'description': 'Wear pearl in silver ring on Monday to strengthen Moon energy.'},
                    {'category': 'Donation', 'title': 'Rice Donation', 'description': 'Donate rice and milk to poor people on Mondays.'}
                ],
                'mars': [
                    {'category': 'Gemstone', 'title': 'Red Coral', 'description': 'Wear red coral in copper ring on Tuesday to strengthen Mars energy.'},
                    {'category': 'Donation', 'title': 'Red Lentils', 'description': 'Donate red lentils and jaggery on Tuesdays.'}
                ],
                'mercury': [
                    {'category': 'Gemstone', 'title': 'Emerald', 'description': 'Wear emerald in gold ring on Wednesday to strengthen Mercury energy.'},
                    {'category': 'Donation', 'title': 'Green Items', 'description': 'Donate green vegetables and books on Wednesdays.'}
                ],
                'jupiter': [
                    {'category': 'Gemstone', 'title': 'Yellow Sapphire', 'description': 'Wear yellow sapphire in gold ring on Thursday to strengthen Jupiter energy.'},
                    {'category': 'Donation', 'title': 'Turmeric Donation', 'description': 'Donate turmeric and yellow items on Thursdays.'}
                ],
                'venus': [
                    {'category': 'Gemstone', 'title': 'Diamond', 'description': 'Wear diamond in silver ring on Friday to strengthen Venus energy.'},
                    {'category': 'Donation', 'title': 'Sugar Donation', 'description': 'Donate sugar and white items on Fridays.'}
                ],
                'saturn': [
                    {'category': 'Gemstone', 'title': 'Blue Sapphire', 'description': 'Wear blue sapphire in silver ring on Saturday to strengthen Saturn energy.'},
                    {'category': 'Donation', 'title': 'Oil Donation', 'description': 'Donate mustard oil and black items on Saturdays.'}
                ]
            }
        else:
            planet_remedies = {
                'sun': [
                    {'category': 'रत्न', 'title': 'माणिक', 'description': 'रविवारी सकाळी सोन्याच्या अंगठीत माणिक धारण करा सूर्य ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'गहू दान', 'description': 'रविवारी गरजूंना गहू आणि गूळ दान करा.'}
                ],
                'moon': [
                    {'category': 'रत्न', 'title': 'मोती', 'description': 'सोमवारी चांदीच्या अंगठीत मोती धारण करा चंद्र ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'तांदूळ दान', 'description': 'सोमवारी गरिबांना तांदूळ आणि दूध दान करा.'}
                ],
                'mars': [
                    {'category': 'रत्न', 'title': 'लाल प्रवाळ', 'description': 'मंगळवारी तांब्याच्या अंगठीत लाल प्रवाळ धारण करा मंगळ ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'लाल डाळ', 'description': 'मंगळवारी लाल डाळ आणि गूळ दान करा.'}
                ],
                'mercury': [
                    {'category': 'रत्न', 'title': 'पन्ना', 'description': 'बुधवारी सोन्याच्या अंगठीत पन्ना धारण करा बुध ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'हिरव्या वस्तू', 'description': 'बुधवारी हिरव्या भाज्या आणि पुस्तके दान करा.'}
                ],
                'jupiter': [
                    {'category': 'रत्न', 'title': 'पुष्पराग', 'description': 'गुरुवारी सोन्याच्या अंगठीत पुष्पराग धारण करा गुरु ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'हळद दान', 'description': 'गुरुवारी हळद आणि पिवळ्या वस्तू दान करा.'}
                ],
                'venus': [
                    {'category': 'रत्न', 'title': 'हिरा', 'description': 'शुक्रवारी चांदीच्या अंगठीत हिरा धारण करा शुक्र ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'साखर दान', 'description': 'शुक्रवारी साखर आणि पांढर्या वस्तू दान करा.'}
                ],
                'saturn': [
                    {'category': 'रत्न', 'title': 'नीलम', 'description': 'शनिवारी चांदीच्या अंगठीत नीलम धारण करा शनि ऊर्जा मजबूत करण्यासाठी.'},
                    {'category': 'दान', 'title': 'तेल दान', 'description': 'शनिवारी मोहरीचे तेल आणि काळ्या वस्तू दान करा.'}
                ]
            }
        
        return planet_remedies.get(planet, [])
    
    def _get_general_remedies(self, language: str) -> List[Dict[str, str]]:
        """Get general remedies when no specific planetary remedies are needed."""
        if language == 'en':
            return [
                {'category': 'Spiritual', 'title': 'Daily Prayer', 'description': 'Offer prayers to your chosen deity every morning for divine blessings.'},
                {'category': 'Charity', 'title': 'Food Donation', 'description': 'Feed the hungry and donate food regularly to accumulate positive karma.'},
                {'category': 'Lifestyle', 'title': 'Early Rising', 'description': 'Wake up before sunrise to align with natural cosmic rhythms.'},
                {'category': 'Mantra', 'title': 'Om Chanting', 'description': 'Chant Om 108 times daily to purify mind and enhance spiritual energy.'},
                {'category': 'Service', 'title': 'Help Others', 'description': 'Serve others selflessly to remove negative karma and attract blessings.'}
            ]
        else:
            return [
                {'category': 'आध्यात्मिक', 'title': 'दैनिक प्रार्थना', 'description': 'दैवी आशीर्वादासाठी दर सकाळी आपल्या इष्ट देवतेची प्रार्थना करा.'},
                {'category': 'दानधर्म', 'title': 'अन्न दान', 'description': 'सकारात्मक कर्म जमा करण्यासाठी भुकेल्यांना खायला द्या आणि नियमित अन्न दान करा.'},
                {'category': 'जीवनशैली', 'title': 'लवकर उठणे', 'description': 'नैसर्गिक वैश्विक लयशी जुळवून घेण्यासाठी सूर्योदयापूर्वी उठा.'},
                {'category': 'मंत्र', 'title': 'ॐ जप', 'description': 'मन शुद्ध करण्यासाठी आणि आध्यात्मिक ऊर्जा वाढवण्यासाठी दररोज ॐ चा 108 वेळा जप करा.'},
                {'category': 'सेवा', 'title': 'इतरांची मदत', 'description': 'नकारात्मक कर्म काढून टाकण्यासाठी आणि आशीर्वाद आकर्षित करण्यासाठी निःस्वार्थपणे इतरांची सेवा करा.'}
            ]
