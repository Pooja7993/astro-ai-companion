"""
Health & Wellness Engine for Astro AI Companion
Provides Ayurvedic recommendations, seasonal health tips, and wellness guidance
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import ephem

@dataclass
class HealthRecommendation:
    """Health recommendation information."""
    category: str
    title: str
    description: str
    benefits: List[str]
    timing: str
    language: str = 'en'

class HealthWellnessEngine:
    """Engine for health and wellness recommendations based on astrology."""
    
    def __init__(self):
        self.seasons = {
            'spring': {'start': 3, 'end': 5, 'dosha': 'kapha'},
            'summer': {'start': 6, 'end': 8, 'dosha': 'pitta'},
            'autumn': {'start': 9, 'end': 11, 'dosha': 'vata'},
            'winter': {'start': 12, 'end': 2, 'dosha': 'vata'}
        }
        
        self.planetary_health = {
            'sun': {
                'dosha': 'pitta',
                'body_part': 'heart, spine, right eye (men), left eye (women)',
                'health_issues': ['heart problems', 'fever', 'headaches', 'eye issues'],
                'remedies': ['surya namaskar', 'sun gazing', 'red foods', 'golden milk']
            },
            'moon': {
                'dosha': 'kapha',
                'body_part': 'stomach, left eye (men), right eye (women), mind',
                'health_issues': ['digestive problems', 'mental health', 'sleep issues', 'water retention'],
                'remedies': ['moon gazing', 'silver water', 'white foods', 'meditation']
            },
            'mars': {
                'dosha': 'pitta',
                'body_part': 'muscles, blood, reproductive organs, left ear',
                'health_issues': ['inflammation', 'fever', 'blood disorders', 'anger issues'],
                'remedies': ['physical exercise', 'red foods', 'copper water', 'anger management']
            },
            'mercury': {
                'dosha': 'vata',
                'body_part': 'nervous system, skin, respiratory system',
                'health_issues': ['nervous disorders', 'skin problems', 'speech issues', 'anxiety'],
                'remedies': ['green foods', 'pranayama', 'nervine herbs', 'communication therapy']
            },
            'jupiter': {
                'dosha': 'kapha',
                'body_part': 'liver, fat, right ear, thighs',
                'health_issues': ['liver problems', 'obesity', 'diabetes', 'wisdom issues'],
                'remedies': ['yellow foods', 'turmeric', 'wisdom practices', 'teaching others']
            },
            'venus': {
                'dosha': 'kapha',
                'body_part': 'reproductive organs, face, kidneys, throat',
                'health_issues': ['reproductive issues', 'kidney problems', 'beauty concerns', 'love life'],
                'remedies': ['white foods', 'diamond water', 'beauty rituals', 'relationship healing']
            },
            'saturn': {
                'dosha': 'vata',
                'body_part': 'bones, teeth, skin, nervous system',
                'health_issues': ['bone problems', 'skin disorders', 'chronic diseases', 'depression'],
                'remedies': ['oil massage', 'black foods', 'patience practices', 'karma yoga']
            }
        }
    
    def get_seasonal_health_tips(self, date: datetime = None) -> Dict[str, Any]:
        """Get seasonal health recommendations."""
        if date is None:
            date = datetime.now()
        
        month = date.month
        
        # Determine season
        current_season = None
        for season, info in self.seasons.items():
            if info['start'] <= month <= info['end']:
                current_season = season
                break
        
        if not current_season:
            current_season = 'winter'  # December to February
        
        return self._get_season_health_guide(current_season)
    
    def _get_season_health_guide(self, season: str) -> Dict[str, Any]:
        """Get health guide for specific season."""
        guides = {
            'spring': {
                'en': {
                    'name': 'Spring (Vasant)',
                    'dosha': 'Kapha',
                    'description': 'Spring is the season of renewal and growth. Kapha dosha is naturally high.',
                    'diet': [
                        'Light, dry, and warm foods',
                        'Bitter, astringent, and pungent tastes',
                        'Honey, ginger, turmeric',
                        'Avoid heavy, oily, and sweet foods'
                    ],
                    'lifestyle': [
                        'Early morning exercise',
                        'Dry massage with warm oil',
                        'Nasal cleansing (neti)',
                        'Sun exposure in moderation'
                    ],
                    'herbs': ['Ginger', 'Turmeric', 'Black pepper', 'Honey'],
                    'activities': ['Yoga', 'Pranayama', 'Walking', 'Gardening']
                },
                'mr': {
                    'name': 'वसंत',
                    'dosha': 'कफ',
                    'description': 'वसंत हा नूतनीकरण आणि वाढीचा काळ आहे. कफ दोष नैसर्गिकरित्या जास्त असतो.',
                    'diet': [
                        'हलके, कोरडे आणि उबदार अन्न',
                        'कडू, तुरट आणि तिखट चवी',
                        'मध, आले, हळद',
                        'जड, तैलयुक्त आणि गोड अन्न टाळा'
                    ],
                    'lifestyle': [
                        'सकाळी लवकर व्यायाम',
                        'उबदार तेलाने कोरडी मालिश',
                        'नाक साफ करणे (नेती)',
                        'मर्यादित प्रमाणात सूर्यप्रकाश'
                    ],
                    'herbs': ['आले', 'हळद', 'मिरी', 'मध'],
                    'activities': ['योग', 'प्राणायाम', 'चालणे', 'बागकाम']
                }
            },
            'summer': {
                'en': {
                    'name': 'Summer (Grishma)',
                    'dosha': 'Pitta',
                    'description': 'Summer is hot and intense. Pitta dosha is naturally high.',
                    'diet': [
                        'Cool, sweet, and bitter foods',
                        'Coconut water, cucumber, mint',
                        'Avoid hot, spicy, and sour foods',
                        'Stay hydrated with cool drinks'
                    ],
                    'lifestyle': [
                        'Cool baths and showers',
                        'Moonlight exposure',
                        'Gentle exercise in cool hours',
                        'Avoid midday sun'
                    ],
                    'herbs': ['Coconut', 'Mint', 'Coriander', 'Rose'],
                    'activities': ['Swimming', 'Moon gazing', 'Gentle yoga', 'Cool walks']
                },
                'mr': {
                    'name': 'उन्हाळा',
                    'dosha': 'पित्त',
                    'description': 'उन्हाळा गरम आणि तीव्र असतो. पित्त दोष नैसर्गिकरित्या जास्त असतो.',
                    'diet': [
                        'थंड, गोड आणि कडू अन्न',
                        'नारळ पाणी, काकडी, पुदीना',
                        'गरम, तिखट आणि आंबट अन्न टाळा',
                        'थंड पेयांसह जलयोजन राखा'
                    ],
                    'lifestyle': [
                        'थंड स्नान',
                        'चंद्रप्रकाश',
                        'थंड तासांमध्ये सौम्य व्यायाम',
                        'दुपारचे सूर्य टाळा'
                    ],
                    'herbs': ['नारळ', 'पुदीना', 'कोथिंबीर', 'गुलाब'],
                    'activities': ['पोहणे', 'चंद्र पाहणे', 'सौम्य योग', 'थंड चालणे']
                }
            },
            'autumn': {
                'en': {
                    'name': 'Autumn (Sharad)',
                    'dosha': 'Vata',
                    'description': 'Autumn is dry and windy. Vata dosha is naturally high.',
                    'diet': [
                        'Warm, moist, and sweet foods',
                        'Ghee, sesame oil, warm milk',
                        'Avoid cold, dry, and bitter foods',
                        'Regular meal times'
                    ],
                    'lifestyle': [
                        'Warm oil massage (abhyanga)',
                        'Warm baths',
                        'Gentle, grounding exercise',
                        'Regular sleep schedule'
                    ],
                    'herbs': ['Sesame', 'Ghee', 'Warm spices', 'Nuts'],
                    'activities': ['Grounding yoga', 'Warm baths', 'Gentle walks', 'Meditation']
                },
                'mr': {
                    'name': 'शरद',
                    'dosha': 'वात',
                    'description': 'शरद कोरडा आणि वाऱ्याचा असतो. वात दोष नैसर्गिकरित्या जास्त असतो.',
                    'diet': [
                        'उबदार, ओलसर आणि गोड अन्न',
                        'तूप, तिळाचे तेल, उबदार दूध',
                        'थंड, कोरडे आणि कडू अन्न टाळा',
                        'नियमित जेवणाचे वेळ'
                    ],
                    'lifestyle': [
                        'उबदार तेल मालिश (अभ्यंग)',
                        'उबदार स्नान',
                        'सौम्य, जमिनीवरचे व्यायाम',
                        'नियमित झोपेचे वेळ'
                    ],
                    'herbs': ['तिळ', 'तूप', 'उबदार मसाले', 'काजू'],
                    'activities': ['जमिनीवरचा योग', 'उबदार स्नान', 'सौम्य चालणे', 'ध्यान']
                }
            },
            'winter': {
                'en': {
                    'name': 'Winter (Hemant/Shishir)',
                    'dosha': 'Vata',
                    'description': 'Winter is cold and dry. Vata dosha is naturally high.',
                    'diet': [
                        'Warm, heavy, and sweet foods',
                        'Hot soups, stews, and warm drinks',
                        'Ghee, nuts, and warming spices',
                        'Avoid cold, light, and dry foods'
                    ],
                    'lifestyle': [
                        'Warm oil massage daily',
                        'Warm baths and steam',
                        'Moderate exercise to generate heat',
                        'Early bedtime and late rising'
                    ],
                    'herbs': ['Ginger', 'Cinnamon', 'Cardamom', 'Black pepper'],
                    'activities': ['Warm yoga', 'Steam therapy', 'Warm walks', 'Rest']
                },
                'mr': {
                    'name': 'हिवाळा',
                    'dosha': 'वात',
                    'description': 'हिवाळा थंड आणि कोरडा असतो. वात दोष नैसर्गिकरित्या जास्त असतो.',
                    'diet': [
                        'उबदार, जड आणि गोड अन्न',
                        'गरम सूप, स्टू आणि उबदार पेय',
                        'तूप, काजू आणि उबदार मसाले',
                        'थंड, हलके आणि कोरडे अन्न टाळा'
                    ],
                    'lifestyle': [
                        'दररोज उबदार तेल मालिश',
                        'उबदार स्नान आणि वाफ',
                        'उष्णता निर्माण करण्यासाठी मध्यम व्यायाम',
                        'लवकर झोपणे आणि उशीरा उठणे'
                    ],
                    'herbs': ['आले', 'दालचिनी', 'वेलची', 'मिरी'],
                    'activities': ['उबदार योग', 'वाफ चिकित्सा', 'उबदार चालणे', 'विश्रांती']
                }
            }
        }
        
        return guides.get(season, guides['spring'])
    
    def get_planetary_health_guidance(self, dominant_planet: str, language: str = 'en') -> HealthRecommendation:
        """Get health guidance based on dominant planet."""
        planet_info = self.planetary_health.get(dominant_planet, self.planetary_health['sun'])
        
        if language == 'en':
            return HealthRecommendation(
                category='Planetary Health',
                title=f'{dominant_planet.title()} Health Guidance',
                description=f'Your dominant planet {dominant_planet} affects {planet_info["body_part"]}. Focus on balancing {planet_info["dosha"]} dosha.',
                benefits=[
                    f'Strengthens {planet_info["body_part"]}',
                    f'Balances {planet_info["dosha"]} dosha',
                    'Improves overall vitality',
                    'Prevents health issues'
                ],
                timing='Best practiced during planetary hours',
                language='en'
            )
        else:
            return HealthRecommendation(
                category='ग्रह आरोग्य',
                title=f'{dominant_planet.title()} आरोग्य मार्गदर्शन',
                description=f'आपला प्रमुख ग्रह {dominant_planet} {planet_info["body_part"]} ला प्रभावित करतो. {planet_info["dosha"]} दोष संतुलित करण्यावर लक्ष केंद्रित करा.',
                benefits=[
                    f'{planet_info["body_part"]} मजबूत करते',
                    f'{planet_info["dosha"]} दोष संतुलित करते',
                    'एकूण चैतन्य सुधारते',
                    'आरोग्य समस्या टाळते'
                ],
                timing='ग्रहीय तासांमध्ये सर्वोत्तम सराव',
                language='mr'
            )
    
    def get_exercise_timing(self, birth_time: str, language: str = 'en') -> Dict[str, Any]:
        """Get optimal exercise timing based on birth time."""
        try:
            birth_hour = int(birth_time.split(':')[0])
            
            # Determine dosha based on birth time
            if 6 <= birth_hour <= 10:
                dominant_dosha = 'kapha'
                best_time = '6:00 AM - 10:00 AM'
                exercise_type = 'Vigorous exercise, sun salutations'
            elif 10 <= birth_hour <= 14:
                dominant_dosha = 'pitta'
                best_time = '6:00 AM - 8:00 AM or 6:00 PM - 8:00 PM'
                exercise_type = 'Moderate exercise, cooling practices'
            else:
                dominant_dosha = 'vata'
                best_time = '6:00 AM - 8:00 AM'
                exercise_type = 'Gentle exercise, grounding practices'
            
            if language == 'en':
                return {
                    'best_time': best_time,
                    'exercise_type': exercise_type,
                    'dosha': dominant_dosha,
                    'recommendations': [
                        'Exercise during your optimal time',
                        'Stay consistent with timing',
                        'Listen to your body',
                        'Include warm-up and cool-down'
                    ]
                }
            else:
                return {
                    'best_time': best_time,
                    'exercise_type': exercise_type,
                    'dosha': dominant_dosha,
                    'recommendations': [
                        'आपल्या सर्वोत्तम वेळेत व्यायाम करा',
                        'वेळेसह सातत्य राखा',
                        'आपल्या शरीराकडे लक्ष द्या',
                        'वॉर्म-अप आणि कूल-डाउन समाविष्ट करा'
                    ]
                }
        except:
            # Default recommendations
            if language == 'en':
                return {
                    'best_time': '6:00 AM - 8:00 AM',
                    'exercise_type': 'Moderate exercise',
                    'dosha': 'balanced',
                    'recommendations': [
                        'Exercise in the morning',
                        'Stay consistent',
                        'Listen to your body',
                        'Include warm-up and cool-down'
                    ]
                }
            else:
                return {
                    'best_time': '6:00 AM - 8:00 AM',
                    'exercise_type': 'मध्यम व्यायाम',
                    'dosha': 'संतुलित',
                    'recommendations': [
                        'सकाळी व्यायाम करा',
                        'सातत्य राखा',
                        'आपल्या शरीराकडे लक्ष द्या',
                        'वॉर्म-अप आणि कूल-डाउन समाविष्ट करा'
                    ]
                }
    
    def get_daily_health_routine(self, language: str = 'en') -> Dict[str, Any]:
        """Get daily health routine recommendations."""
        if language == 'en':
            return {
                'morning': [
                    'Wake up before sunrise (Brahma Muhurta)',
                    'Drink warm water with lemon and honey',
                    'Practice sun salutations (Surya Namaskar)',
                    'Oil pulling for oral health',
                    'Meditation for mental clarity'
                ],
                'afternoon': [
                    'Eat lunch at peak digestive time (12-2 PM)',
                    'Take a short walk after meals',
                    'Stay hydrated with room temperature water',
                    'Practice deep breathing exercises'
                ],
                'evening': [
                    'Light dinner before sunset',
                    'Gentle evening walk',
                    'Family time and relaxation',
                    'Prepare for restful sleep'
                ],
                'night': [
                    'Early bedtime (10 PM)',
                    'Avoid screens 1 hour before sleep',
                    'Light reading or meditation',
                    'Gratitude practice before sleep'
                ]
            }
        else:
            return {
                'morning': [
                    'सूर्योदयापूर्वी उठा (ब्रह्म मुहूर्त)',
                    'लिंबू आणि मधासह उबदार पाणी प्या',
                    'सूर्य नमस्कार सराव करा',
                    'तोंडाच्या आरोग्यासाठी तेल कुल्ला',
                    'मानसिक स्पष्टतेसाठी ध्यान'
                ],
                'afternoon': [
                    'पचनाच्या शिखर वेळेत दुपारचे जेवण (12-2 PM)',
                    'जेवणानंतर थोडी चालणे',
                    'खोलीच्या तापमानाच्या पाण्याने जलयोजन राखा',
                    'खोल श्वासोच्छवासाचे व्यायाम'
                ],
                'evening': [
                    'सूर्यास्तापूर्वी हलके रात्रीचे जेवण',
                    'सौम्य संध्याकाळी चालणे',
                    'कौटुंबिक वेळ आणि विश्रांती',
                    'चांगल्या झोपेसाठी तयारी'
                ],
                'night': [
                    'लवकर झोपणे (10 PM)',
                    'झोपण्यापूर्वी 1 तास स्क्रीन टाळा',
                    'हलके वाचन किंवा ध्यान',
                    'झोपण्यापूर्वी कृतज्ञता सराव'
                ]
            } 