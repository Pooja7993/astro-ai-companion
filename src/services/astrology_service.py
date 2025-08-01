"""
Unified Astrology Service combining Vedic, Numerology, and Lal Kitab
"""

import json
from datetime import datetime, date
from typing import Dict, Any, Optional, List
import swisseph as swe
from loguru import logger
from src.services.openrouter_service import openrouter_service

class UnifiedAstrologyService:
    """Unified astrology service combining multiple systems."""
    
    def __init__(self):
        # Initialize Swiss Ephemeris
        swe.set_ephe_path('/usr/share/swisseph')  # Render path
        
        # Zodiac signs
        self.zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # Nakshatras
        self.nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
    
    def calculate_birth_chart(self, birth_date: str, birth_time: str, 
                            birth_place: str, latitude: float, longitude: float) -> Dict[str, Any]:
        """Calculate comprehensive birth chart."""
        try:
            # Parse birth date and time
            birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Calculate Julian day
            jd = swe.julday(birth_dt.year, birth_dt.month, birth_dt.day, 
                           birth_dt.hour + birth_dt.minute/60.0)
            
            # Calculate planetary positions
            planets = self._calculate_planetary_positions(jd)
            
            # Calculate houses
            houses = self._calculate_houses(jd, latitude, longitude)
            
            # Calculate Nakshatra
            moon_longitude = planets.get('Moon', {}).get('longitude', 0)
            nakshatra = self._calculate_nakshatra(moon_longitude)
            
            # Calculate aspects
            aspects = self._calculate_aspects(planets)
            
            return {
                'planets': planets,
                'houses': houses,
                'nakshatra': nakshatra,
                'aspects': aspects,
                'ascendant': houses.get('1', {}).get('sign', 'Aries')
            }
            
        except Exception as e:
            logger.error(f"Error calculating birth chart: {e}")
            return {}
    
    def _calculate_planetary_positions(self, jd: float) -> Dict[str, Any]:
        """Calculate planetary positions."""
        planets = {}
        planet_ids = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mercury': swe.MERCURY,
            'Venus': swe.VENUS,
            'Mars': swe.MARS,
            'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE,
            'Ketu': swe.MEAN_NODE  # Ketu is 180° opposite to Rahu
        }
        
        for planet_name, planet_id in planet_ids.items():
            try:
                result = swe.calc_ut(jd, planet_id)
                longitude = result[0][0]
                
                if planet_name == 'Ketu':
                    longitude = (longitude + 180) % 360
                
                sign_num = int(longitude / 30)
                sign = self.zodiac_signs[sign_num]
                degree = longitude % 30
                
                planets[planet_name] = {
                    'longitude': longitude,
                    'sign': sign,
                    'degree': degree,
                    'sign_num': sign_num
                }
                
            except Exception as e:
                logger.error(f"Error calculating {planet_name}: {e}")
        
        return planets
    
    def _calculate_houses(self, jd: float, latitude: float, longitude: float) -> Dict[str, Any]:
        """Calculate house positions."""
        try:
            # Calculate houses using Placidus system
            houses_data = swe.houses(jd, latitude, longitude, b'P')  # P for Placidus
            cusps = houses_data[0]
            
            houses = {}
            for i in range(12):
                cusp_longitude = cusps[i + 1]  # cusps[0] is not used
                sign_num = int(cusp_longitude / 30)
                sign = self.zodiac_signs[sign_num]
                degree = cusp_longitude % 30
                
                houses[str(i + 1)] = {
                    'cusp': cusp_longitude,
                    'sign': sign,
                    'degree': degree,
                    'sign_num': sign_num
                }
            
            return houses
            
        except Exception as e:
            logger.error(f"Error calculating houses: {e}")
            return {}
    
    def _calculate_nakshatra(self, moon_longitude: float) -> Dict[str, Any]:
        """Calculate Nakshatra from Moon's longitude."""
        try:
            # Each nakshatra is 13°20' (13.333...)
            nakshatra_length = 360 / 27
            nakshatra_num = int(moon_longitude / nakshatra_length)
            nakshatra_name = self.nakshatras[nakshatra_num]
            
            # Calculate pada (quarter)
            pada_length = nakshatra_length / 4
            pada_num = int((moon_longitude % nakshatra_length) / pada_length) + 1
            
            return {
                'name': nakshatra_name,
                'number': nakshatra_num + 1,
                'pada': pada_num,
                'longitude': moon_longitude
            }
            
        except Exception as e:
            logger.error(f"Error calculating nakshatra: {e}")
            return {'name': 'Unknown', 'number': 1, 'pada': 1}
    
    def _calculate_aspects(self, planets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate planetary aspects."""
        aspects = []
        planet_names = list(planets.keys())
        
        for i, planet1 in enumerate(planet_names):
            for planet2 in planet_names[i+1:]:
                try:
                    long1 = planets[planet1]['longitude']
                    long2 = planets[planet2]['longitude']
                    
                    # Calculate angular difference
                    diff = abs(long1 - long2)
                    if diff > 180:
                        diff = 360 - diff
                    
                    # Check for major aspects (with 8° orb)
                    aspect_type = None
                    if abs(diff - 0) <= 8:
                        aspect_type = "Conjunction"
                    elif abs(diff - 60) <= 8:
                        aspect_type = "Sextile"
                    elif abs(diff - 90) <= 8:
                        aspect_type = "Square"
                    elif abs(diff - 120) <= 8:
                        aspect_type = "Trine"
                    elif abs(diff - 180) <= 8:
                        aspect_type = "Opposition"
                    
                    if aspect_type:
                        aspects.append({
                            'planet1': planet1,
                            'planet2': planet2,
                            'aspect': aspect_type,
                            'orb': diff
                        })
                        
                except Exception as e:
                    logger.error(f"Error calculating aspect between {planet1} and {planet2}: {e}")
        
        return aspects
    
    def calculate_numerology(self, birth_date: str, full_name: str) -> Dict[str, Any]:
        """Calculate numerology numbers."""
        try:
            # Parse birth date
            birth_dt = datetime.strptime(birth_date, "%Y-%m-%d")
            
            # Life Path Number
            life_path = self._calculate_life_path_number(birth_dt)
            
            # Destiny Number (from full name)
            destiny = self._calculate_destiny_number(full_name)
            
            # Soul Number (from vowels in name)
            soul = self._calculate_soul_number(full_name)
            
            return {
                'life_path_number': life_path,
                'destiny_number': destiny,
                'soul_number': soul,
                'birth_date': birth_date,
                'full_name': full_name
            }
            
        except Exception as e:
            logger.error(f"Error calculating numerology: {e}")
            return {}
    
    def _calculate_life_path_number(self, birth_dt: datetime) -> int:
        """Calculate life path number from birth date."""
        # Sum all digits in birth date
        date_str = birth_dt.strftime("%d%m%Y")
        total = sum(int(digit) for digit in date_str)
        
        # Reduce to single digit (except master numbers 11, 22, 33)
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(digit) for digit in str(total))
        
        return total
    
    def _calculate_destiny_number(self, full_name: str) -> int:
        """Calculate destiny number from full name."""
        # Letter to number mapping
        letter_values = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
            'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
        }
        
        total = sum(letter_values.get(char.upper(), 0) for char in full_name if char.isalpha())
        
        # Reduce to single digit
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(digit) for digit in str(total))
        
        return total
    
    def _calculate_soul_number(self, full_name: str) -> int:
        """Calculate soul number from vowels in name."""
        vowel_values = {'A': 1, 'E': 5, 'I': 9, 'O': 6, 'U': 3}
        
        total = sum(vowel_values.get(char.upper(), 0) for char in full_name if char.upper() in vowel_values)
        
        # Reduce to single digit
        while total > 9 and total not in [11, 22, 33]:
            total = sum(int(digit) for digit in str(total))
        
        return total
    
    def generate_lal_kitab_analysis(self, birth_chart: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Lal Kitab analysis."""
        try:
            planets = birth_chart.get('planets', {})
            houses = birth_chart.get('houses', {})
            
            # Simplified Lal Kitab analysis
            analysis = {
                'debts': [],
                'remedies': [],
                'favorable_periods': [],
                'challenging_periods': []
            }
            
            # Check for planetary debts (simplified)
            if 'Sun' in planets and planets['Sun']['sign_num'] == 6:  # Sun in Libra
                analysis['debts'].append("Pitru Rin (Ancestral debt)")
                analysis['remedies'].append("Offer water to Sun daily")
            
            if 'Moon' in planets and planets['Moon']['sign_num'] == 7:  # Moon in Scorpio
                analysis['debts'].append("Matru Rin (Mother's debt)")
                analysis['remedies'].append("Donate milk and rice")
            
            # Add general Lal Kitab remedies
            analysis['remedies'].extend([
                "Keep a piece of silver with you",
                "Feed crows regularly",
                "Donate to the needy on Saturdays"
            ])
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error generating Lal Kitab analysis: {e}")
            return {}
    
    async def generate_unified_guidance(self, user_data: Dict[str, Any], 
                                      birth_chart: Dict[str, Any],
                                      numerology: Dict[str, Any],
                                      lal_kitab: Dict[str, Any],
                                      prediction_type: str = "daily") -> str:
        """Generate unified guidance combining all systems."""
        try:
            # Prepare context for AI
            context = f"""
            User: {user_data.get('full_name', 'User')}
            Birth Date: {user_data.get('birth_date')}
            Birth Time: {user_data.get('birth_time')}
            Birth Place: {user_data.get('birth_place')}
            
            Vedic Astrology:
            - Sun Sign: {birth_chart.get('planets', {}).get('Sun', {}).get('sign', 'Unknown')}
            - Moon Sign: {birth_chart.get('planets', {}).get('Moon', {}).get('sign', 'Unknown')}
            - Ascendant: {birth_chart.get('ascendant', 'Unknown')}
            - Nakshatra: {birth_chart.get('nakshatra', {}).get('name', 'Unknown')}
            
            Numerology:
            - Life Path Number: {numerology.get('life_path_number', 'Unknown')}
            - Destiny Number: {numerology.get('destiny_number', 'Unknown')}
            - Soul Number: {numerology.get('soul_number', 'Unknown')}
            
            Lal Kitab:
            - Debts: {', '.join(lal_kitab.get('debts', []))}
            - Remedies: {', '.join(lal_kitab.get('remedies', [])[:3])}
            """
            
            system_prompt = """You are an expert astrologer who combines Vedic astrology, numerology, and Lal Kitab to provide unified guidance. 
            Provide practical, positive, and actionable advice that integrates insights from all three systems. 
            Focus on personal growth, relationships, career, health, and spiritual development.
            Keep the response concise but comprehensive, around 200-300 words."""
            
            prompt = f"""Based on the astrological data provided, generate a {prediction_type} guidance that combines:
            1. Vedic astrological insights
            2. Numerological influences  
            3. Lal Kitab remedies and advice
            
            Provide unified guidance that helps the person navigate their day/week/month with practical advice.
            
            Context: {context}"""
            
            response = await openrouter_service.generate_response(prompt, system_prompt)
            return response
            
        except Exception as e:
            logger.error(f"Error generating unified guidance: {e}")
            return "Unable to generate guidance at this time. Please try again later."

# Global instance
astrology_service = UnifiedAstrologyService()