"""Moon Phase Engine for Astro AI Companion
Personal Family Use - Lunar Phase Calculations and Guidance
"""

import ephem
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import math
import logging
from dataclasses import dataclass

from src.utils.logging_setup import get_logger
from src.utils.multi_language import multi_lang

logger = get_logger(__name__)


@dataclass
class MoonPhaseInfo:
    """Moon phase information."""
    phase_name: str
    illumination: float
    age: float
    moon_sign: str
    next_full_moon: datetime
    next_new_moon: datetime
    rise_time: datetime
    set_time: datetime
    guidance: Dict[str, str]
    activities: Dict[str, List[str]]
    remedies: Dict[str, List[str]]


# Removed duplicate MoonPhaseEngine class definition
        
        # Zodiac signs
        self.zodiac_signs = {
            'en': [
                'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
            ],
            'mr': [
                'मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या',
                'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन'
            ]
        }
        
        # Moon phase guidance
        self.phase_guidance = {
            'New Moon': {
                'en': 'Time for new beginnings and setting intentions. Plant seeds for future growth.',
                'mr': 'नवीन सुरुवात आणि हेतू ठरवण्याची वेळ. भविष्यातील वाढीसाठी बीज पेरा.'
            },
            'Waxing Crescent': {
                'en': 'Time to take action on intentions. Focus on growth and building momentum.',
                'mr': 'हेतूंवर कृती करण्याची वेळ. वाढ आणि गती निर्माण करण्यावर लक्ष केंद्रित करा.'
            },
            'First Quarter': {
                'en': 'Time to overcome challenges. Make decisions and adjustments to your plans.',
                'mr': 'आव्हाने दूर करण्याची वेळ. तुमच्या योजनांमध्ये निर्णय आणि समायोजन करा.'
            },
            'Waxing Gibbous': {
                'en': 'Time for refinement and improvement. Focus on details and perfecting your work.',
                'mr': 'परिष्करण आणि सुधारणेची वेळ. तपशील आणि तुमचे काम परिपूर्ण करण्यावर लक्ष केंद्रित करा.'
            },
            'Full Moon': {
                'en': 'Time for culmination and manifestation. Celebrate achievements and release what no longer serves you.',
                'mr': 'परिणती आणि प्रकटीकरणाची वेळ. यश साजरे करा आणि जे आता उपयोगी नाही ते सोडून द्या.'
            },
            'Waning Gibbous': {
                'en': 'Time for gratitude and sharing. Express thanks and share your wisdom with others.',
                'mr': 'कृतज्ञता आणि सामायिक करण्याची वेळ. आभार व्यक्त करा आणि तुमचे ज्ञान इतरांसह सामायिक करा.'
            },
            'Last Quarter': {
                'en': 'Time for reflection and forgiveness. Let go of what no longer serves you.',
                'mr': 'चिंतन आणि क्षमेची वेळ. जे आता उपयोगी नाही ते सोडून द्या.'
            },
            'Waning Crescent': {
                'en': 'Time for rest and surrender. Prepare for the new cycle by clearing space.',
                'mr': 'विश्रांती आणि समर्पणाची वेळ. जागा साफ करून नवीन चक्रासाठी तयार व्हा.'
            }
        }
        
        # Moon phase activities
        self.phase_activities = {
            'New Moon': {
                'en': [
                    'Set new intentions and goals',
                    'Start new projects',
                    'Plant seeds (literal and metaphorical)',
                    'Meditate on new beginnings',
                    'Create vision boards'
                ],
                'mr': [
                    'नवीन हेतू आणि ध्येय ठरवा',
                    'नवीन प्रकल्प सुरू करा',
                    'बीज पेरा (शाब्दिक आणि प्रतीकात्मक)',
                    'नवीन सुरुवातीवर ध्यान करा',
                    'व्हिजन बोर्ड तयार करा'
                ]
            },
            'Full Moon': {
                'en': [
                    'Celebrate achievements',
                    'Release what no longer serves you',
                    'Charge crystals in moonlight',
                    'Practice gratitude rituals',
                    'Perform family ceremonies'
                ],
                'mr': [
                    'यश साजरे करा',
                    'जे आता उपयोगी नाही ते सोडून द्या',
                    'चंद्रप्रकाशात स्फटिक चार्ज करा',
                    'कृतज्ञता विधी करा',
                    'कौटुंबिक समारंभ करा'
                ]
            }
        }
        
        # Moon phase remedies
        self.phase_remedies = {
            'New Moon': {
                'en': [
                    'Light a white candle',
                    'Write down intentions',
                    'Drink moon-charged water',
                    'Wear silver jewelry',
                    'Offer rice to deities'
                ],
                'mr': [
                    'पांढरी मेणबत्ती लावा',
                    'हेतू लिहून ठेवा',
                    'चंद्र-चार्ज केलेले पाणी प्या',
                    'चांदीचे दागिने घाला',
                    'देवतांना तांदूळ अर्पण करा'
                ]
            },
            'Full Moon': {
                'en': [
                    'Take a ritual bath with salt',
                    'Meditate under the moonlight',
                    'Perform cleansing rituals',
                    'Chant moon mantras',
                    'Offer milk to deities'
                ],
                'mr': [
                    'मिठासह विधी स्नान करा',
                    'चंद्रप्रकाशात ध्यान करा',
                    'शुद्धीकरण विधी करा',
                    'चंद्र मंत्र जपा',
                    'देवतांना दूध अर्पण करा'
                ]
            }
        }
        
    def get_current_moon_phase(self, date: datetime = None, language: str = 'en') -> MoonPhaseInfo:
        """Get current moon phase information."""
        if date is None:
            date = datetime.now()
        
        # Set observer date
        self.observer.date = date
        
        # Calculate moon phase
        moon_phase = MoonPhase.from_date(date)
        
        # Calculate moon rise and set times
        self.moon.compute(self.observer)
        rise_time = self.observer.next_rising(self.moon).datetime()
        set_time = self.observer.next_setting(self.moon).datetime()
        
        # Calculate moon sign
        moon_sign_index = int(math.degrees(self.moon.hlon) / 30) % 12
        moon_sign = self.zodiac_signs[language][moon_sign_index]
        
        # Get guidance for this phase
        guidance = {
            'en': self.phase_guidance.get(moon_phase.phase_name, {}).get('en', ''),
            'mr': self.phase_guidance.get(moon_phase.phase_name, {}).get('mr', '')
        }
        
        # Get activities for this phase
        if moon_phase.phase_name in self.phase_activities:
            activities = self.phase_activities[moon_phase.phase_name]
        elif 'Full Moon' in self.phase_activities and 'Full' in moon_phase.phase_name:
            activities = self.phase_activities['Full Moon']
        elif 'New Moon' in self.phase_activities and 'New' in moon_phase.phase_name:
            activities = self.phase_activities['New Moon']
        else:
            activities = {
                'en': ['Meditate', 'Practice yoga', 'Spend time with family', 'Connect with nature', 'Journal'],
                'mr': ['ध्यान करा', 'योग सराव करा', 'कुटुंबासोबत वेळ घालवा', 'निसर्गाशी जोडा', 'जर्नल लिहा']
            }
        
        # Get remedies for this phase
        if moon_phase.phase_name in self.phase_remedies:
            remedies = self.phase_remedies[moon_phase.phase_name]
        elif 'Full Moon' in self.phase_remedies and 'Full' in moon_phase.phase_name:
            remedies = self.phase_remedies['Full Moon']
        elif 'New Moon' in self.phase_remedies and 'New' in moon_phase.phase_name:
            remedies = self.phase_remedies['New Moon']
        else:
            remedies = {
                'en': ['Drink moon-charged water', 'Wear silver', 'Meditate', 'Chant mantras', 'Offer prayers'],
                'mr': ['चंद्र-चार्ज केलेले पाणी प्या', 'चांदी घाला', 'ध्यान करा', 'मंत्र जपा', 'प्रार्थना अर्पण करा']
            }
        
        # Create and return moon phase info
        return MoonPhaseInfo(
            phase_name=self.phase_names[language][self.phase_names['en'].index(moon_phase.phase_name)],
            illumination=moon_phase.illumination,
            age=moon_phase.age,
            moon_sign=moon_sign,
            next_full_moon=moon_phase.next_full,
            next_new_moon=moon_phase.next_new,
            rise_time=rise_time,
            set_time=set_time,
            guidance=guidance,
            activities=activities,
            remedies=remedies
        )
    
    def set_location(self, latitude: str, longitude: str, elevation: float = 0):
        """Set observer location."""
        try:
            self.observer.lat = latitude
            self.observer.lon = longitude
            self.observer.elevation = elevation
            logger.info(f"Location set to lat: {latitude}, lon: {longitude}, elev: {elevation}")
            return True
        except Exception as e:
            logger.error(f"Error setting location: {e}")
            return False

@dataclass
class MoonPhase:
    """Moon phase information."""
    phase_name: str
    illumination: float
    age: float
    angle: float
    next_full: Optional[datetime] = None
    next_new: Optional[datetime] = None
    
    @classmethod
    def from_date(cls, date: datetime = None):
        """Calculate moon phase for a given date."""
        if date is None:
            date = datetime.now()
            
        moon = ephem.Moon(date)
        sun = ephem.Sun(date)
        
        # Calculate moon phase angle
        moon_phase_angle = moon.phase
        
        # Calculate illumination (0-1)
        illumination = moon.phase / 100.0
        
        # Calculate moon age (0-29.53 days)
        previous_new_moon = ephem.previous_new_moon(date)
        moon_age = (date - previous_new_moon.datetime()).total_seconds() / 86400.0
        
        # Calculate next full and new moons
        next_full_moon = ephem.next_full_moon(date)
        next_new_moon = ephem.next_new_moon(date)
        
        # Determine phase name based on angle
        if moon_phase_angle < 1.0:
            phase_name = "New Moon"
        elif moon_phase_angle < 90.0:
            phase_name = "Waxing Crescent"
        elif abs(moon_phase_angle - 90.0) < 1.0:
            phase_name = "First Quarter"
        elif moon_phase_angle < 180.0:
            phase_name = "Waxing Gibbous"
        elif abs(moon_phase_angle - 180.0) < 1.0:
            phase_name = "Full Moon"
        elif moon_phase_angle < 270.0:
            phase_name = "Waning Gibbous"
        elif abs(moon_phase_angle - 270.0) < 1.0:
            phase_name = "Last Quarter"
        else:
            phase_name = "Waning Crescent"
        
        return cls(
            phase_name=phase_name,
            illumination=illumination,
            age=moon_age,
            angle=moon_phase_angle,
            next_full=next_full_moon.datetime(),
            next_new=next_new_moon.datetime()
        )
    
    


class MoonPhaseEngine:
    """Engine for moon phase calculations and guidance."""
    
    def __init__(self):
        self.moon = ephem.Moon()
        self.sun = ephem.Sun()
        self.observer = ephem.Observer()
        
        # Default location (Mumbai)
        self.observer.lat = '19.0760'  # North
        self.observer.lon = '72.8777'  # East
        self.observer.elevation = 14  # meters
        
        # Moon phase names
        self.phase_names = {
            'en': [
                'New Moon', 'Waxing Crescent', 'First Quarter', 
                'Waxing Gibbous', 'Full Moon', 'Waning Gibbous', 
                'Last Quarter', 'Waning Crescent'
            ],
            'mr': [
                'अमावस्या', 'शुक्ल पक्ष (वाढता चंद्र)', 'शुक्ल पक्ष (प्रथम चतुर्थी)', 
                'शुक्ल पक्ष (वाढता चंद्र)', 'पौर्णिमा', 'कृष्ण पक्ष (कमी होणारा चंद्र)', 
                'कृष्ण पक्ष (अंतिम चतुर्थी)', 'कृष्ण पक्ष (कमी होणारा चंद्र)'
            ]
        }
        
        # Zodiac signs
        self.zodiac_signs = {
            'en': [
                'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
            ],
            'mr': [
                'मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या',
                'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन'
            ]
        }
        
        # Moon phase guidance
        self.phase_guidance = {
            'New Moon': {
                'en': 'Time for new beginnings and setting intentions. Plant seeds for future growth.',
                'mr': 'नवीन सुरुवात आणि हेतू ठरवण्याची वेळ. भविष्यातील वाढीसाठी बीज पेरा.'
            },
            'Waxing Crescent': {
                'en': 'Time to take action on intentions. Focus on growth and building momentum.',
                'mr': 'हेतूंवर कृती करण्याची वेळ. वाढ आणि गती निर्माण करण्यावर लक्ष केंद्रित करा.'
            },
            'First Quarter': {
                'en': 'Time to overcome challenges. Make decisions and adjustments to your plans.',
                'mr': 'आव्हाने दूर करण्याची वेळ. तुमच्या योजनांमध्ये निर्णय आणि समायोजन करा.'
            },
            'Waxing Gibbous': {
                'en': 'Time for refinement and improvement. Focus on details and perfecting your work.',
                'mr': 'परिष्करण आणि सुधारणेची वेळ. तपशील आणि तुमचे काम परिपूर्ण करण्यावर लक्ष केंद्रित करा.'
            },
            'Full Moon': {
                'en': 'Time for culmination and manifestation. Celebrate achievements and release what no longer serves you.',
                'mr': 'परिणती आणि प्रकटीकरणाची वेळ. यश साजरे करा आणि जे आता उपयोगी नाही ते सोडून द्या.'
            },
            'Waning Gibbous': {
                'en': 'Time for gratitude and sharing. Express thanks and share your wisdom with others.',
                'mr': 'कृतज्ञता आणि सामायिक करण्याची वेळ. आभार व्यक्त करा आणि तुमचे ज्ञान इतरांसह सामायिक करा.'
            },
            'Last Quarter': {
                'en': 'Time for reflection and forgiveness. Let go of what no longer serves you.',
                'mr': 'चिंतन आणि क्षमेची वेळ. जे आता उपयोगी नाही ते सोडून द्या.'
            },
            'Waning Crescent': {
                'en': 'Time for rest and surrender. Prepare for the new cycle by clearing space.',
                'mr': 'विश्रांती आणि समर्पणाची वेळ. जागा साफ करून नवीन चक्रासाठी तयार व्हा.'
            }
        }
        
        # Moon phase activities
        self.phase_activities = {
            'New Moon': {
                'en': [
                    'Set new intentions and goals',
                    'Start new projects',
                    'Plant seeds (literal and metaphorical)',
                    'Meditate on new beginnings',
                    'Create vision boards'
                ],
                'mr': [
                    'नवीन हेतू आणि ध्येय ठरवा',
                    'नवीन प्रकल्प सुरू करा',
                    'बीज पेरा (शाब्दिक आणि प्रतीकात्मक)',
                    'नवीन सुरुवातीवर ध्यान करा',
                    'व्हिजन बोर्ड तयार करा'
                ]
            },
            'Full Moon': {
                'en': [
                    'Celebrate achievements',
                    'Release what no longer serves you',
                    'Charge crystals in moonlight',
                    'Practice gratitude rituals',
                    'Perform family ceremonies'
                ],
                'mr': [
                    'यश साजरे करा',
                    'जे आता उपयोगी नाही ते सोडून द्या',
                    'चंद्रप्रकाशात स्फटिक चार्ज करा',
                    'कृतज्ञता विधी करा',
                    'कौटुंबिक समारंभ करा'
                ]
            }
        }
        
        # Moon phase remedies
        self.phase_remedies = {
            'New Moon': {
                'en': [
                    'Light a white candle',
                    'Write down intentions',
                    'Drink moon-charged water',
                    'Wear silver jewelry',
                    'Offer rice to deities'
                ],
                'mr': [
                    'पांढरी मेणबत्ती लावा',
                    'हेतू लिहून ठेवा',
                    'चंद्र-चार्ज केलेले पाणी प्या',
                    'चांदीचे दागिने घाला',
                    'देवतांना तांदूळ अर्पण करा'
                ]
            },
            'Full Moon': {
                'en': [
                    'Take a ritual bath with salt',
                    'Meditate under the moonlight',
                    'Perform cleansing rituals',
                    'Chant moon mantras',
                    'Offer milk to deities'
                ],
                'mr': [
                    'मिठासह विधी स्नान करा',
                    'चंद्रप्रकाशात ध्यान करा',
                    'शुद्धीकरण विधी करा',
                    'चंद्र मंत्र जपा',
                    'देवतांना दूध अर्पण करा'
                ]
            }
        }
    
    def get_current_moon_phase(self, date: datetime = None, language: str = 'en') -> MoonPhaseInfo:
        """Get current moon phase information."""
        if date is None:
            date = datetime.now()
        
        # Set observer date
        self.observer.date = date
        
        # Calculate moon phase
        moon_phase = MoonPhase.from_date(date)
        
        # Calculate moon rise and set times
        self.moon.compute(self.observer)
        try:
            rise_time = self.observer.next_rising(self.moon).datetime()
            set_time = self.observer.next_setting(self.moon).datetime()
        except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
            logger.warning(f"Moon rise/set calculation error: {e}")
            rise_time = datetime.now()
            set_time = datetime.now() + timedelta(hours=12)
        
        # Calculate moon sign
        moon_sign_index = int(math.degrees(self.moon.hlon) / 30) % 12
        moon_sign = self.zodiac_signs[language][moon_sign_index]
        
        # Get guidance for this phase
        guidance = {
            'en': self.phase_guidance.get(moon_phase.phase_name, {}).get('en', ''),
            'mr': self.phase_guidance.get(moon_phase.phase_name, {}).get('mr', '')
        }
        
        # Get activities for this phase
        if moon_phase.phase_name in self.phase_activities:
            activities = self.phase_activities[moon_phase.phase_name]
        elif 'Full Moon' in self.phase_activities and 'Full' in moon_phase.phase_name:
            activities = self.phase_activities['Full Moon']
        elif 'New Moon' in self.phase_activities and 'New' in moon_phase.phase_name:
            activities = self.phase_activities['New Moon']
        else:
            activities = {
                'en': ['Meditate', 'Practice yoga', 'Spend time with family', 'Connect with nature', 'Journal'],
                'mr': ['ध्यान करा', 'योग सराव करा', 'कुटुंबासोबत वेळ घालवा', 'निसर्गाशी जोडा', 'जर्नल लिहा']
            }
        
        # Get remedies for this phase
        if moon_phase.phase_name in self.phase_remedies:
            remedies = self.phase_remedies[moon_phase.phase_name]
        elif 'Full Moon' in self.phase_remedies and 'Full' in moon_phase.phase_name:
            remedies = self.phase_remedies['Full Moon']
        elif 'New Moon' in self.phase_remedies and 'New' in moon_phase.phase_name:
            remedies = self.phase_remedies['New Moon']
        else:
            remedies = {
                'en': ['Drink moon-charged water', 'Wear silver', 'Meditate', 'Chant mantras', 'Offer prayers'],
                'mr': ['चंद्र-चार्ज केलेले पाणी प्या', 'चांदी घाला', 'ध्यान करा', 'मंत्र जपा', 'प्रार्थना अर्पण करा']
            }
        
        # Create and return moon phase info
        return MoonPhaseInfo(
            phase_name=self.phase_names[language][self.phase_names['en'].index(moon_phase.phase_name)],
            illumination=moon_phase.illumination,
            age=moon_phase.age,
            moon_sign=moon_sign,
            next_full_moon=moon_phase.next_full,
            next_new_moon=moon_phase.next_new,
            rise_time=rise_time,
            set_time=set_time,
            guidance=guidance,
            activities=activities,
            remedies=remedies
        )
    
    def _calculate_next_full_and_new_moon(self, date: datetime) -> Tuple[datetime, datetime]:
        """Calculate next full and new moon dates."""
        try:
            # Find next full moon
            next_full = ephem.next_full_moon(date)
            next_full_date = datetime.strptime(str(next_full), '%Y/%m/%d %H:%M:%S')
            
            # Find next new moon
            next_new = ephem.next_new_moon(date)
            next_new_date = datetime.strptime(str(next_new), '%Y/%m/%d %H:%M:%S')
            
            return next_full_date, next_new_date
            
        except Exception as e:
            logger.error(f"Error calculating next full/new moon: {e}")
            # Return default values in case of error
            return datetime.now() + timedelta(days=14), datetime.now() + timedelta(days=14)
    
    def _calculate_illumination(self, phase_angle: float) -> float:
        """Calculate moon illumination percentage."""
        # Simple approximation based on phase angle
        return phase_angle
    
    def _calculate_moon_age(self, phase_angle: float) -> float:
        """Calculate moon age in days."""
        # Moon age based on phase angle (0-29.53 days)
        return phase_angle / 100.0 * 29.53
    
    def get_moon_phase_guidance(self, date: datetime = None, language: str = 'en') -> Dict[str, Any]:
        """Get personalized guidance based on moon phase."""
        try:
            # Get moon phase information
            moon_phase = self.get_current_moon_phase(date)
            
            # Get phase name in requested language
            phase_index = self.phase_names['en'].index(moon_phase.phase)
            phase_name = self.phase_names[language][phase_index] if language in self.phase_names else moon_phase.phase
            
            # Get guidance in requested language
            if language in self.phase_significance and moon_phase.phase in self.phase_significance['en']:
                guidance = self.phase_significance[language][self.phase_names[language][phase_index]]
            else:
                guidance = moon_phase.guidance
            
            # Get remedies in requested language
            if language in self.remedies and moon_phase.phase in self.phase_significance['en']:
                phase_key = 'अमावस्या' if phase_index == 0 else 'पौर्णिमा' if phase_index == 4 else 'अमावस्या'
                remedies = self.remedies[language][phase_key]
            else:
                remedies = moon_phase.remedies
            
            # Format days until next phases
            days_until_full = (moon_phase.next_full - datetime.now()).days
            days_until_new = (moon_phase.next_new - datetime.now()).days
            
            # Create guidance text
            if language == 'en':
                guidance_text = f"The current moon phase is {moon_phase.phase} with {moon_phase.illumination:.1%} illumination. "
                guidance_text += f"This is a time for {guidance.lower()} "
                guidance_text += f"The next full moon is in {days_until_full} days, and the next new moon is in {days_until_new} days."
            else:  # Marathi
                guidance_text = f"सध्याची चंद्र कला {phase_name} आहे, {moon_phase.illumination:.1%} प्रकाशित. "
                guidance_text += f"ही {guidance.lower()} "
                guidance_text += f"पुढील पौर्णिमा {days_until_full} दिवसांत आहे, आणि पुढील अमावस्या {days_until_new} दिवसांत आहे."
            
            return {
                'phase': phase_name,
                'illumination': moon_phase.illumination,
                'age': moon_phase.age,
                'guidance': guidance_text,
                'remedies': remedies,
                'next_full': moon_phase.next_full,
                'next_new': moon_phase.next_new
            }
            
        except Exception as e:
            logger.error(f"Error generating moon phase guidance: {e}")
            if language == 'en':
                return {
                    'phase': 'Unknown',
                    'guidance': "Could not generate moon phase guidance.",
                    'remedies': ["Consult with an astrologer for personalized guidance."]
                }
            else:
                return {
                    'phase': 'अज्ञात',
                    'guidance': "चंद्र कलेचे मार्गदर्शन तयार करू शकत नाही.",
                    'remedies': ["वैयक्तिक मार्गदर्शनासाठी ज्योतिषाचा सल्ला घ्या."]
                }
    
    def get_auspicious_times(self, date: datetime = None, language: str = 'en') -> Dict[str, Any]:
        """Calculate auspicious times based on moon phase."""
        try:
            if date is None:
                date = datetime.now()
            
            # Get current moon phase
            moon_phase = MoonPhase.from_date(date)
            
            # Set observer date
            self.observer.date = date
            
            # Calculate sunrise and sunset
            self.sun.compute(self.observer)
            try:
                sunrise = self.observer.next_rising(self.sun).datetime()
                sunset = self.observer.next_setting(self.sun).datetime()
            except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
                logger.warning(f"Sun rise/set calculation error: {e}")
                # Use default times for polar regions
                sunrise = date.replace(hour=6, minute=0, second=0, microsecond=0)
                sunset = date.replace(hour=18, minute=0, second=0, microsecond=0)
            
            # Calculate moon rise and set
            self.moon.compute(self.observer)
            try:
                moonrise = self.observer.next_rising(self.moon).datetime()
                moonset = self.observer.next_setting(self.moon).datetime()
            except (ephem.AlwaysUpError, ephem.NeverUpError) as e:
                logger.warning(f"Moon rise/set calculation error: {e}")
                # Use default times for polar regions
                moonrise = date.replace(hour=18, minute=0, second=0, microsecond=0)
                moonset = date.replace(hour=6, minute=0, second=0, microsecond=0)
                
            # Get complete moon phase info
            moon_info = self.get_current_moon_phase(date, language)
            phase_index = self.phase_names['en'].index(moon_phase.phase_name)
            
            # Format times
            rise_time_str = moonrise.strftime('%I:%M %p')
            set_time_str = moonset.strftime('%I:%M %p')
            
            # Morning hours are generally good for waxing moon (0-3)
            # Evening hours are generally good for waning moon (4-7)
            if phase_index < 4:  # Waxing moon
                auspicious_start = sunrise.strftime('%I:%M %p')
                auspicious_end = (sunrise + timedelta(hours=4)).strftime('%I:%M %p')
                activity = "Starting new projects" if language == 'en' else "नवीन प्रकल्प सुरू करणे"
            else:  # Waning moon
                auspicious_start = (sunset - timedelta(hours=2)).strftime('%I:%M %p')
                auspicious_end = sunset.strftime('%I:%M %p')
                activity = "Reflection and meditation" if language == 'en' else "चिंतन आणि ध्यान"
            
            return {
                'moonrise': rise_time_str,
                'moonset': set_time_str,
                'auspicious_start': auspicious_start,
                'auspicious_end': auspicious_end,
                'activity': activity,
                'best_time': f"{auspicious_start} - {auspicious_end}",
                'activities': moon_info.activities[language][:3] if language in moon_info.activities else [],
                'avoid_time': "4:00 PM - 8:00 PM" if phase_index < 4 else "6:00 AM - 10:00 AM"
            }
                
        except Exception as e:
            logger.error(f"Error calculating auspicious times: {e}")
            if language == 'en':
                return {
                    'moonrise': "Not available",
                    'moonset': "Not available",
                    'auspicious_start': "Not available",
                    'auspicious_end': "Not available",
                    'activity': "Consult with an astrologer",
                    'best_time': "Not available",
                    'activities': ["Consult with an astrologer for personalized guidance."],
                    'avoid_time': "Not available"
                }
            else:
                return {
                    'moonrise': "उपलब्ध नाही",
                    'moonset': "उपलब्ध नाही",
                    'auspicious_start': "उपलब्ध नाही",
                    'auspicious_end': "उपलब्ध नाही",
                    'activity': "ज्योतिषाचा सल्ला घ्या",
                    'best_time': "उपलब्ध नाही",
                    'activities': ["वैयक्तिक मार्गदर्शनासाठी ज्योतिषाचा सल्ला घ्या."],
                    'avoid_time': "उपलब्ध नाही"
                }


# Create a singleton instance
moon_phase_engine = MoonPhaseEngine()