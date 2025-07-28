"""
Simple Chart Analyzer for Astro AI Companion
Personal Family Use - Ephem Integration
"""

import ephem
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import yaml
from pathlib import Path

from src.utils.config_simple import get_config


class SimpleChartAnalyzer:
    """Simple chart analyzer using Ephem."""
    
    def __init__(self):
        try:
            self.config = get_config()
        except Exception:
            # Use default config if environment variables are missing
            self.config = None
        
        self.city_coordinates = self._load_city_coordinates()
        
        # Vedic rules file was removed - use empty dict
        self.vedic_rules = {}
    
    def _load_city_coordinates(self) -> Dict[str, tuple]:
        """Load offline city coordinates database."""
        return {
            "mumbai, india": (19.0760, 72.8777),
            "delhi, india": (28.7041, 77.1025),
            "bangalore, india": (12.9716, 77.5946),
            "hyderabad, india": (17.3850, 78.4867),
            "ahmedabad, india": (23.0225, 72.5714),
            "chennai, india": (13.0827, 80.2707),
            "kolkata, india": (22.5726, 88.3639),
            "pune, india": (18.5204, 73.8567),
            "jaipur, india": (26.9124, 75.7873),
            "lucknow, india": (26.8467, 80.9462),
            "new york, usa": (40.7128, -74.0060),
            "london, uk": (51.5074, -0.1278),
            "tokyo, japan": (35.6762, 139.6503),
            "paris, france": (48.8566, 2.3522),
            "sydney, australia": (-33.8688, 151.2093),
            "toronto, canada": (43.6532, -79.3832),
            "dubai, uae": (25.2048, 55.2708),
            "singapore": (1.3521, 103.8198),
            "hong kong": (22.3193, 114.1694),
            "los angeles, usa": (34.0522, -118.2437),
            "chicago, usa": (41.8781, -87.6298),
            "berlin, germany": (52.5200, 13.4050),
            "madrid, spain": (40.4168, -3.7038),
            "rome, italy": (41.9028, 12.4964),
            "moscow, russia": (55.7558, 37.6176),
            "beijing, china": (39.9042, 116.4074),
            "shanghai, china": (31.2304, 121.4737),
            "seoul, south korea": (37.5665, 126.9780),
            "bangkok, thailand": (13.7563, 100.5018),
            "kuala lumpur, malaysia": (3.1390, 101.6869),
            "jakarta, indonesia": (-6.2088, 106.8456),
            "manila, philippines": (14.5995, 120.9842),
            "cairo, egypt": (30.0444, 31.2357),
            "johannesburg, south africa": (-26.2041, 28.0473),
            "lagos, nigeria": (6.5244, 3.3792),
            "nairobi, kenya": (-1.2921, 36.8219),
            "buenos aires, argentina": (-34.6118, -58.3960),
            "sao paulo, brazil": (-23.5558, -46.6396),
            "mexico city, mexico": (19.4326, -99.1332),
            "lima, peru": (-12.0464, -77.0428),
            "bogota, colombia": (4.7110, -74.0721),
            "santiago, chile": (-33.4489, -70.6693),
            "caracas, venezuela": (10.4806, -66.9036),
            "montevideo, uruguay": (-34.9011, -56.1645),
            "quito, ecuador": (-0.1807, -78.4678),
            "la paz, bolivia": (-16.5000, -68.1193),
            "asuncion, paraguay": (-25.2637, -57.5759),
            "georgetown, guyana": (6.8013, -58.1551),
            "paramaribo, suriname": (5.8520, -55.2038),
            "cayenne, french guiana": (4.9333, -52.3333),
        }
    
    def get_coordinates(self, location: str) -> tuple:
        """Get latitude and longitude for a location using offline database."""
        location_lower = location.lower()
        
        # Try exact match first
        if location_lower in self.city_coordinates:
            return self.city_coordinates[location_lower]
        
        # Try partial match
        for city, coords in self.city_coordinates.items():
            if location_lower in city or city in location_lower:
                return coords
        
        # Default to Mumbai if not found
        return (19.0760, 72.8777)
    
    def analyze_chart(self, user) -> Dict[str, Any]:
        """Analyze birth chart for a user."""
        try:
            # Parse birth date and time
            birth_date = user.birth_date
            birth_time = user.birth_time
            birth_place = user.birth_place
            
            dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Get coordinates
            lat, lon = self.get_coordinates(birth_place)
            
            # Calculate planetary positions
            planetary_positions = self._calculate_planetary_positions(dt)
            
            # Get basic analysis
            basic_info = self._get_basic_info(planetary_positions, user)
            
            # Create analysis result
            analysis = {
                "user_info": {
                    "name": user.name,
                    "birth_date": birth_date,
                    "birth_time": birth_time,
                    "birth_place": birth_place,
                    "coordinates": {"latitude": lat, "longitude": lon}
                },
                "planetary_positions": planetary_positions,
                "basic_info": basic_info,
                "analysis_date": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            return self._get_default_analysis(user)
    
    def _calculate_planetary_positions(self, dt: datetime) -> Dict[str, Dict]:
        """Calculate planetary positions using Ephem."""
        positions = {}
        
        planets = {
            "Sun": ephem.Sun(),
            "Moon": ephem.Moon(),
            "Mercury": ephem.Mercury(),
            "Venus": ephem.Venus(),
            "Mars": ephem.Mars(),
            "Jupiter": ephem.Jupiter(),
            "Saturn": ephem.Saturn()
        }
        
        for planet_name, planet in planets.items():
            try:
                planet.compute(dt)
                
                # Convert to degrees
                longitude = float(planet.hlong) * 180 / ephem.pi
                latitude = float(planet.hlat) * 180 / ephem.pi
                
                # Get zodiac sign
                sign = self._get_zodiac_sign(longitude)
                
                positions[planet_name] = {
                    "longitude": longitude,
                    "latitude": latitude,
                    "sign": sign,
                    "symbol": self._get_planet_symbol(planet_name),
                    "sanskrit": self._get_planet_sanskrit(planet_name)
                }
                
            except Exception as e:
                positions[planet_name] = {
                    "longitude": 0,
                    "latitude": 0,
                    "sign": "Aries",
                    "symbol": self._get_planet_symbol(planet_name),
                    "sanskrit": self._get_planet_sanskrit(planet_name)
                }
        
        return positions
    
    def _get_zodiac_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude."""
        # Normalize longitude to 0-360
        longitude = longitude % 360
        
        # Zodiac signs with their starting degrees
        signs = [
            (0, "Aries"), (30, "Taurus"), (60, "Gemini"), (90, "Cancer"),
            (120, "Leo"), (150, "Virgo"), (180, "Libra"), (210, "Scorpio"),
            (240, "Sagittarius"), (270, "Capricorn"), (300, "Aquarius"), (330, "Pisces")
        ]
        
        for start_deg, sign in signs:
            if longitude >= start_deg and longitude < start_deg + 30:
                return sign
        
        return "Aries"  # Default
    
    def _get_planet_symbol(self, planet_name: str) -> str:
        """Get planet symbol."""
        symbols = {
            "Sun": "☉", "Moon": "☽", "Mercury": "☿", "Venus": "♀",
            "Mars": "♂", "Jupiter": "♃", "Saturn": "♄"
        }
        return symbols.get(planet_name, "☉")
    
    def _get_planet_sanskrit(self, planet_name: str) -> str:
        """Get planet Sanskrit name."""
        sanskrit = {
            "Sun": "सूर्य", "Moon": "चंद्र", "Mercury": "बुध", "Venus": "शुक्र",
            "Mars": "मंगल", "Jupiter": "गुरु", "Saturn": "शनि"
        }
        return sanskrit.get(planet_name, "सूर्य")
    
    def _get_basic_info(self, planetary_positions: Dict, user) -> Dict[str, Any]:
        """Get basic chart information."""
        sun_sign = planetary_positions.get("Sun", {}).get("sign", "Aries")
        moon_sign = planetary_positions.get("Moon", {}).get("sign", "Taurus")
        
        return {
            "sun_sign": sun_sign,
            "moon_sign": moon_sign,
            "ascendant": "Aries",  # Simplified
            "birth_star": self._get_birth_star(planetary_positions),
            "personality": self._get_personality_traits(sun_sign),
            "strengths": self._get_strengths(sun_sign),
            "challenges": self._get_challenges(sun_sign)
        }
    
    def _get_birth_star(self, planetary_positions: Dict) -> str:
        """Get birth star (simplified)."""
        moon_longitude = planetary_positions.get("Moon", {}).get("longitude", 0)
        
        # Simplified nakshatra calculation
        nakshatra_num = int(moon_longitude / 13.333333) % 27
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        return nakshatras[nakshatra_num] if 0 <= nakshatra_num < 27 else "Ashwini"
    
    def _get_personality_traits(self, sun_sign: str) -> List[str]:
        """Get personality traits based on sun sign."""
        traits = {
            "Aries": ["Courageous", "Energetic", "Willful", "Pioneering", "Independent"],
            "Taurus": ["Patient", "Reliable", "Warmhearted", "Loving", "Persistent"],
            "Gemini": ["Adaptable", "Versatile", "Communicative", "Witty", "Intellectual"],
            "Cancer": ["Emotional", "Loving", "Intuitive", "Imaginative", "Shrewd"],
            "Leo": ["Generous", "Warmhearted", "Creative", "Enthusiastic", "Broad-minded"],
            "Virgo": ["Modest", "Shy", "Meticulous", "Reliable", "Practical"],
            "Libra": ["Diplomatic", "Gracious", "Fair-minded", "Social", "Peace-loving"],
            "Scorpio": ["Determined", "Forceful", "Emotional", "Intuitive", "Powerful"],
            "Sagittarius": ["Optimistic", "Loves freedom", "Jovial", "Good-humored", "Honest"],
            "Capricorn": ["Responsible", "Disciplined", "Self-controlled", "Good managers"],
            "Aquarius": ["Progressive", "Original", "Independent", "Humanitarian"],
            "Pisces": ["Compassionate", "Artistic", "Intuitive", "Gentle", "Wise"]
        }
        return traits.get(sun_sign, ["Unique", "Special", "Wonderful"])
    
    def _get_strengths(self, sun_sign: str) -> List[str]:
        """Get strengths based on sun sign."""
        strengths = {
            "Aries": ["Leadership", "Courage", "Energy", "Pioneering spirit"],
            "Taurus": ["Patience", "Reliability", "Loyalty", "Practicality"],
            "Gemini": ["Communication", "Adaptability", "Intelligence", "Versatility"],
            "Cancer": ["Emotional intelligence", "Intuition", "Nurturing", "Protectiveness"],
            "Leo": ["Charisma", "Creativity", "Generosity", "Leadership"],
            "Virgo": ["Attention to detail", "Reliability", "Analytical thinking", "Practicality"],
            "Libra": ["Diplomacy", "Fairness", "Social skills", "Harmony"],
            "Scorpio": ["Determination", "Intuition", "Passion", "Transformation"],
            "Sagittarius": ["Optimism", "Adventure", "Honesty", "Philosophy"],
            "Capricorn": ["Responsibility", "Discipline", "Ambition", "Practicality"],
            "Aquarius": ["Innovation", "Humanitarianism", "Originality", "Independence"],
            "Pisces": ["Compassion", "Creativity", "Intuition", "Spirituality"]
        }
        return strengths.get(sun_sign, ["Unique talents", "Special abilities"])
    
    def _get_challenges(self, sun_sign: str) -> List[str]:
        """Get challenges based on sun sign."""
        challenges = {
            "Aries": ["Impatience", "Impulsiveness", "Aggressiveness"],
            "Taurus": ["Stubbornness", "Possessiveness", "Resistance to change"],
            "Gemini": ["Restlessness", "Inconsistency", "Scattered energy"],
            "Cancer": ["Moodiness", "Over-sensitivity", "Clinginess"],
            "Leo": ["Pride", "Stubbornness", "Need for attention"],
            "Virgo": ["Perfectionism", "Over-criticism", "Worry"],
            "Libra": ["Indecisiveness", "People-pleasing", "Avoidance of conflict"],
            "Scorpio": ["Jealousy", "Secretiveness", "Intensity"],
            "Sagittarius": ["Impatience", "Bluntness", "Restlessness"],
            "Capricorn": ["Pessimism", "Rigidity", "Workaholism"],
            "Aquarius": ["Detachment", "Rebelliousness", "Unpredictability"],
            "Pisces": ["Escapism", "Over-sensitivity", "Indecisiveness"]
        }
        return challenges.get(sun_sign, ["Personal growth areas", "Learning opportunities"])
    
    def _get_default_analysis(self, user) -> Dict[str, Any]:
        """Get default analysis when calculation fails."""
        return {
            "user_info": {
                "name": user.name,
                "birth_date": user.birth_date,
                "birth_time": user.birth_time,
                "birth_place": user.birth_place,
                "coordinates": {"latitude": 19.0760, "longitude": 72.8777}
            },
            "planetary_positions": {
                "Sun": {"longitude": 0, "latitude": 0, "sign": "Aries", "symbol": "☉", "sanskrit": "सूर्य"},
                "Moon": {"longitude": 30, "latitude": 0, "sign": "Taurus", "symbol": "☽", "sanskrit": "चंद्र"},
                "Mercury": {"longitude": 60, "latitude": 0, "sign": "Gemini", "symbol": "☿", "sanskrit": "बुध"},
                "Venus": {"longitude": 90, "latitude": 0, "sign": "Cancer", "symbol": "♀", "sanskrit": "शुक्र"},
                "Mars": {"longitude": 120, "latitude": 0, "sign": "Leo", "symbol": "♂", "sanskrit": "मंगल"},
                "Jupiter": {"longitude": 150, "latitude": 0, "sign": "Virgo", "symbol": "♃", "sanskrit": "गुरु"},
                "Saturn": {"longitude": 180, "latitude": 0, "sign": "Libra", "symbol": "♄", "sanskrit": "शनि"}
            },
            "basic_info": {
                "sun_sign": "Aries",
                "moon_sign": "Taurus",
                "ascendant": "Aries",
                "birth_star": "Ashwini",
                "personality": ["Courageous", "Energetic", "Willful", "Pioneering", "Independent"],
                "strengths": ["Leadership", "Courage", "Energy", "Pioneering spirit"],
                "challenges": ["Impatience", "Impulsiveness", "Aggressiveness"]
            },
            "analysis_date": datetime.now().isoformat()
        }


# Global chart analyzer instance
chart_analyzer = SimpleChartAnalyzer() 