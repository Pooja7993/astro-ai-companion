"""
Festival Calendar Engine for Astro AI Companion
Provides Hindu festivals, auspicious days, and cultural celebrations
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import ephem

@dataclass
class Festival:
    """Festival information."""
    name: str
    date: datetime
    significance: str
    rituals: List[str]
    family_activities: List[str]
    language: str = 'en'

class FestivalCalendar:
    """Engine for festival and auspicious day calculations."""
    
    def __init__(self):
        self.festivals_2024 = {
            'makar_sankranti': {
                'date': '2024-01-15',
                'name_en': 'Makar Sankranti',
                'name_mr': 'मकर संक्रांति',
                'significance_en': 'Sun enters Capricorn, harvest festival, new beginnings',
                'significance_mr': 'सूर्य मकर राशीत प्रवेश करतो, पीक सण, नवीन सुरुवाती',
                'rituals_en': [
                    'Take holy bath in sacred rivers',
                    'Donate sesame seeds and jaggery',
                    'Fly kites to welcome the sun',
                    'Prepare traditional sweets'
                ],
                'rituals_mr': [
                    'पवित्र नद्यांमध्ये स्नान करा',
                    'तीळ आणि गुळ दान करा',
                    'सूर्याचे स्वागत करण्यासाठी पतंग उडवा',
                    'पारंपारिक मिठाई तयार करा'
                ],
                'family_activities_en': [
                    'Family kite flying competition',
                    'Prepare traditional sweets together',
                    'Visit temple as a family',
                    'Share sweets with neighbors'
                ],
                'family_activities_mr': [
                    'कौटुंबिक पतंग उडवण्याची स्पर्धा',
                    'एकत्र पारंपारिक मिठाई तयार करा',
                    'कुटुंब म्हणून मंदिरात जा',
                    'शेजाऱ्यांसोबत मिठाई सामायिक करा'
                ]
            },
            'vasant_panchami': {
                'date': '2024-02-14',
                'name_en': 'Vasant Panchami',
                'name_mr': 'वसंत पंचमी',
                'significance_en': 'Goddess Saraswati worship, spring festival, education',
                'significance_mr': 'सरस्वती देवीची पूजा, वसंत सण, शिक्षण',
                'rituals_en': [
                    'Worship Goddess Saraswati',
                    'Wear yellow clothes',
                    'Start new learning activities',
                    'Offer yellow flowers'
                ],
                'rituals_mr': [
                    'सरस्वती देवीची पूजा करा',
                    'पिवळे कपडे घाला',
                    'नवीन शिकण्याच्या क्रियाकलापांना सुरुवात करा',
                    'पिवळी फुले अर्पण करा'
                ],
                'family_activities_en': [
                    'Children start new educational activities',
                    'Family prayer for wisdom',
                    'Spring cleaning together',
                    'Plant new flowers in garden'
                ],
                'family_activities_mr': [
                    'मुले नवीन शैक्षणिक क्रियाकलाप सुरू करतात',
                    'ज्ञानासाठी कौटुंबिक प्रार्थना',
                    'एकत्र वसंत सफाई',
                    'बागेत नवीन फुले लावा'
                ]
            },
            'maha_shivratri': {
                'date': '2024-03-08',
                'name_en': 'Maha Shivratri',
                'name_mr': 'महा शिवरात्री',
                'significance_en': 'Lord Shiva worship, spiritual awakening, fasting',
                'significance_mr': 'शिव देवाची पूजा, आध्यात्मिक जागृती, उपवास',
                'rituals_en': [
                    'Fast and stay awake all night',
                    'Worship Lord Shiva with bilva leaves',
                    'Chant Om Namah Shivaya',
                    'Visit Shiva temple'
                ],
                'rituals_mr': [
                    'उपवास करा आणि रात्रभर जागे रहा',
                    'बेलपत्रांसह शिव देवाची पूजा करा',
                    'ॐ नमः शिवाय जप करा',
                    'शिव मंदिरात जा'
                ],
                'family_activities_en': [
                    'Family night vigil',
                    'Storytelling about Lord Shiva',
                    'Prepare special prasad together',
                    'Meditation as a family'
                ],
                'family_activities_mr': [
                    'कौटुंबिक रात्र जागरण',
                    'शिव देवाबद्दल कथा सांगणे',
                    'एकत्र विशेष प्रसाद तयार करा',
                    'कुटुंब म्हणून ध्यान'
                ]
            },
            'holi': {
                'date': '2024-03-25',
                'name_en': 'Holi',
                'name_mr': 'होळी',
                'significance_en': 'Festival of colors, victory of good over evil, spring',
                'significance_mr': 'रंगांचा सण, चांगल्यावर वाईटाचा विजय, वसंत',
                'rituals_en': [
                    'Play with natural colors',
                    'Burn Holika bonfire',
                    'Exchange sweets and greetings',
                    'Forgive and forget grudges'
                ],
                'rituals_mr': [
                    'नैसर्गिक रंगांसह खेळा',
                    'होळिका दहन करा',
                    'मिठाई आणि शुभेच्छा विनिमय करा',
                    'क्षमा करा आणि वैर विसरा'
                ],
                'family_activities_en': [
                    'Family color play',
                    'Prepare traditional sweets',
                    'Visit friends and relatives',
                    'Sing and dance together'
                ],
                'family_activities_mr': [
                    'कौटुंबिक रंग खेळ',
                    'पारंपारिक मिठाई तयार करा',
                    'मित्र आणि नातेवाईकांना भेट द्या',
                    'एकत्र गाणे आणि नृत्य करा'
                ]
            },
            'ram_navami': {
                'date': '2024-04-17',
                'name_en': 'Ram Navami',
                'name_mr': 'राम नवमी',
                'significance_en': 'Birth of Lord Rama, dharma, ideal leadership',
                'significance_mr': 'श्री रामाचा जन्म, धर्म, आदर्श नेतृत्व',
                'rituals_en': [
                    'Read Ramayana',
                    'Worship Lord Rama',
                    'Chant Ram mantras',
                    'Practice dharma in daily life'
                ],
                'rituals_mr': [
                    'रामायण वाचा',
                    'श्री रामाची पूजा करा',
                    'राम मंत्र जप करा',
                    'दैनंदिन जीवनात धर्माचा पाठपुरावा करा'
                ],
                'family_activities_en': [
                    'Family Ramayana reading',
                    'Drama or storytelling about Rama',
                    'Practice righteous living',
                    'Help those in need'
                ],
                'family_activities_mr': [
                    'कौटुंबिक रामायण वाचन',
                    'रामाबद्दल नाटक किंवा कथा सांगणे',
                    'धर्माचरणाचा सराव',
                    'गरजूंना मदत करा'
                ]
            },
            'hanuman_jayanti': {
                'date': '2024-04-23',
                'name_en': 'Hanuman Jayanti',
                'name_mr': 'हनुमान जयंती',
                'significance_en': 'Birth of Hanuman, devotion, strength, service',
                'significance_mr': 'हनुमानाचा जन्म, भक्ती, शक्ती, सेवा',
                'rituals_en': [
                    'Visit Hanuman temple',
                    'Chant Hanuman Chalisa',
                    'Offer sindoor and oil',
                    'Practice physical exercise'
                ],
                'rituals_mr': [
                    'हनुमान मंदिरात जा',
                    'हनुमान चालीसा जप करा',
                    'सिंदूर आणि तेल अर्पण करा',
                    'शारीरिक व्यायाम करा'
                ],
                'family_activities_en': [
                    'Family Hanuman Chalisa recitation',
                    'Physical activities together',
                    'Service to community',
                    'Strength building exercises'
                ],
                'family_activities_mr': [
                    'कौटुंबिक हनुमान चालीसा पठण',
                    'एकत्र शारीरिक क्रियाकलाप',
                    'समुदायाला सेवा',
                    'शक्ती वाढवणारे व्यायाम'
                ]
            },
            'krishna_janmashtami': {
                'date': '2024-08-26',
                'name_en': 'Krishna Janmashtami',
                'name_mr': 'कृष्ण जन्माष्टमी',
                'significance_en': 'Birth of Lord Krishna, divine love, wisdom',
                'significance_mr': 'श्री कृष्णाचा जन्म, दैवी प्रेम, ज्ञान',
                'rituals_en': [
                    'Fast until midnight',
                    'Decorate baby Krishna cradle',
                    'Sing bhajans and kirtans',
                    'Read Bhagavad Gita'
                ],
                'rituals_mr': [
                    'मध्यरात्रीपर्यंत उपवास करा',
                    'बाल कृष्णाचे पाळणे सजवा',
                    'भजने आणि कीर्तने गावा',
                    'भगवद्गीता वाचा'
                ],
                'family_activities_en': [
                    'Family bhajan singing',
                    'Dahi handi celebration',
                    'Krishna stories for children',
                    'Spiritual discussions'
                ],
                'family_activities_mr': [
                    'कौटुंबिक भजन गायन',
                    'दही हंडी साजरा',
                    'मुलांसाठी कृष्ण कथा',
                    'आध्यात्मिक चर्चा'
                ]
            },
            'ganesh_chaturthi': {
                'date': '2024-09-07',
                'name_en': 'Ganesh Chaturthi',
                'name_mr': 'गणेश चतुर्थी',
                'significance_en': 'Birth of Lord Ganesha, wisdom, success',
                'significance_mr': 'श्री गणेशाचा जन्म, ज्ञान, यश',
                'rituals_en': [
                    'Install Ganesha idol at home',
                    'Offer modak and durva grass',
                    'Chant Ganesh mantras',
                    'Perform aarti daily'
                ],
                'rituals_mr': [
                    'घरी गणेश मूर्ती स्थापना करा',
                    'मोदक आणि दूर्वा गवत अर्पण करा',
                    'गणेश मंत्र जप करा',
                    'दररोज आरती करा'
                ],
                'family_activities_en': [
                    'Family Ganesha decoration',
                    'Prepare modak together',
                    'Cultural programs',
                    'Community celebrations'
                ],
                'family_activities_mr': [
                    'कौटुंबिक गणेश सजावट',
                    'एकत्र मोदक तयार करा',
                    'सांस्कृतिक कार्यक्रम',
                    'समुदाय साजरे'
                ]
            },
            'navratri': {
                'date': '2024-10-03',
                'name_en': 'Navratri',
                'name_mr': 'नवरात्री',
                'significance_en': 'Nine nights of Goddess worship, spiritual purification',
                'significance_mr': 'देवीची नऊ रात्री पूजा, आध्यात्मिक शुद्धी',
                'rituals_en': [
                    'Fast for nine days',
                    'Worship different forms of Goddess',
                    'Perform garba and dandiya',
                    'Read Durga Saptashati'
                ],
                'rituals_mr': [
                    'नऊ दिवस उपवास करा',
                    'देवीच्या विविध रूपांची पूजा करा',
                    'गरबा आणि डांडिया करा',
                    'दुर्गा सप्तशती वाचा'
                ],
                'family_activities_en': [
                    'Family garba nights',
                    'Traditional fasting together',
                    'Cultural dance performances',
                    'Spiritual family time'
                ],
                'family_activities_mr': [
                    'कौटुंबिक गरबा रात्री',
                    'एकत्र पारंपारिक उपवास',
                    'सांस्कृतिक नृत्य कार्यक्रम',
                    'आध्यात्मिक कौटुंबिक वेळ'
                ]
            },
            'diwali': {
                'date': '2024-11-01',
                'name_en': 'Diwali',
                'name_mr': 'दिवाळी',
                'significance_en': 'Festival of lights, victory of good over evil',
                'significance_mr': 'दिव्यांचा सण, चांगल्यावर वाईटाचा विजय',
                'rituals_en': [
                    'Light diyas and lamps',
                    'Worship Goddess Lakshmi',
                    'Clean and decorate home',
                    'Exchange sweets and gifts'
                ],
                'rituals_mr': [
                    'दिवे आणि दीप लावा',
                    'लक्ष्मी देवीची पूजा करा',
                    'घर साफ करा आणि सजवा',
                    'मिठाई आणि भेटवस्तू विनिमय करा'
                ],
                'family_activities_en': [
                    'Family decoration competition',
                    'Traditional sweets making',
                    'Fireworks and celebrations',
                    'Visit relatives and friends'
                ],
                'family_activities_mr': [
                    'कौटुंबिक सजावट स्पर्धा',
                    'पारंपारिक मिठाई तयार करणे',
                    'आतषबाजी आणि साजरे',
                    'नातेवाईक आणि मित्रांना भेट द्या'
                ]
            }
        }
    
    def get_upcoming_festivals(self, days: int = 30) -> List[Festival]:
        """Get upcoming festivals in the next specified days."""
        upcoming = []
        today = datetime.now()
        
        for festival_id, festival_data in self.festivals_2024.items():
            festival_date = datetime.strptime(festival_data['date'], '%Y-%m-%d')
            
            if today <= festival_date <= today + timedelta(days=days):
                upcoming.append(Festival(
                    name=festival_data['name_en'],
                    date=festival_date,
                    significance=festival_data['significance_en'],
                    rituals=festival_data['rituals_en'],
                    family_activities=festival_data['family_activities_en'],
                    language='en'
                ))
        
        return sorted(upcoming, key=lambda x: x.date)
    
    def get_auspicious_days(self, start_date: datetime, days: int = 30) -> List[Dict[str, Any]]:
        """Get auspicious days based on planetary positions."""
        auspicious_days = []
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            
            # Calculate planetary positions
            sun = ephem.Sun()
            moon = ephem.Moon()
            jupiter = ephem.Jupiter()
            
            sun.compute(date)
            moon.compute(date)
            jupiter.compute(date)
            
            # Check for auspicious combinations
            is_auspicious = False
            reason = ""
            
            # Monday (Moon's day) - Good for new beginnings
            if date.weekday() == 0:
                is_auspicious = True
                reason = "Monday - Moon's day, good for new beginnings and emotional matters"
            
            # Thursday (Jupiter's day) - Good for learning and wisdom
            elif date.weekday() == 3:
                is_auspicious = True
                reason = "Thursday - Jupiter's day, good for learning, wisdom, and spiritual activities"
            
            # Sunday (Sun's day) - Good for leadership and authority
            elif date.weekday() == 6:
                is_auspicious = True
                reason = "Sunday - Sun's day, good for leadership, authority, and important decisions"
            
            # Full Moon - Very auspicious
            if abs(moon.phase - 180) < 5:  # Within 5 degrees of full moon
                is_auspicious = True
                reason += " + Full Moon - Very auspicious for all activities"
            
            # New Moon - Good for new beginnings
            if moon.phase < 10:  # New moon
                is_auspicious = True
                reason += " + New Moon - Good for new beginnings and setting intentions"
            
            if is_auspicious:
                auspicious_days.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'day_name': date.strftime('%A'),
                    'reason': reason,
                    'activities': self._get_auspicious_activities(date.weekday())
                })
        
        return auspicious_days
    
    def _get_auspicious_activities(self, weekday: int) -> List[str]:
        """Get activities for auspicious days."""
        activities = {
            0: [  # Monday
                "Start new projects",
                "Begin learning activities",
                "Emotional healing",
                "Family bonding activities"
            ],
            3: [  # Thursday
                "Study and learning",
                "Spiritual practices",
                "Teaching others",
                "Wisdom sharing"
            ],
            6: [  # Sunday
                "Leadership activities",
                "Important decisions",
                "Authority matters",
                "Career planning"
            ]
        }
        
        return activities.get(weekday, ["General positive activities"])
    
    def get_festival_guidance(self, festival: Festival) -> str:
        """Get detailed guidance for a festival."""
        return f"""🎉 **{festival.name}** - {festival.date.strftime('%B %d, %Y')}

**Significance:**
{festival.significance}

**Recommended Rituals:**
{chr(10).join([f"• {ritual}" for ritual in festival.rituals])}

**Family Activities:**
{chr(10).join([f"• {activity}" for activity in festival.family_activities])}

**Blessings for your family!** 🙏""" 