"""
Real Astrology Engine for Astro AI Companion
Personal Family Use - Swiss Ephemeris Integration
"""

import swisseph as swe
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import logging

from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class RealAstrologyEngine:
    """Real astrology calculation engine using Swiss Ephemeris."""
    
    def __init__(self):
        # Initialize Swiss Ephemeris
        swe.set_ephe_path()
        
        # Planetary symbols and names
        self.planets = {
            0: {"name": "Sun", "symbol": "☉", "sanskrit": "सूर्य"},
            1: {"name": "Moon", "symbol": "☽", "sanskrit": "चंद्र"},
            2: {"name": "Mercury", "symbol": "☿", "sanskrit": "बुध"},
            3: {"name": "Venus", "symbol": "♀", "sanskrit": "शुक्र"},
            4: {"name": "Mars", "symbol": "♂", "sanskrit": "मंगल"},
            5: {"name": "Jupiter", "symbol": "♃", "sanskrit": "गुरु"},
            6: {"name": "Saturn", "symbol": "♄", "sanskrit": "शनि"},
            7: {"name": "Uranus", "symbol": "♅", "sanskrit": "राहु"},
            8: {"name": "Neptune", "symbol": "♆", "sanskrit": "केतु"},
            9: {"name": "Pluto", "symbol": "♇", "sanskrit": "प्लूटो"}
        }
        
        # Zodiac signs
        self.zodiac_signs = {
            0: {"name": "Aries", "symbol": "♈", "sanskrit": "मेष", "element": "Fire"},
            1: {"name": "Taurus", "symbol": "♉", "sanskrit": "वृषभ", "element": "Earth"},
            2: {"name": "Gemini", "symbol": "♊", "sanskrit": "मिथुन", "element": "Air"},
            3: {"name": "Cancer", "symbol": "♋", "sanskrit": "कर्क", "element": "Water"},
            4: {"name": "Leo", "symbol": "♌", "sanskrit": "सिंह", "element": "Fire"},
            5: {"name": "Virgo", "symbol": "♍", "sanskrit": "कन्या", "element": "Earth"},
            6: {"name": "Libra", "symbol": "♎", "sanskrit": "तुला", "element": "Air"},
            7: {"name": "Scorpio", "symbol": "♏", "sanskrit": "वृश्चिक", "element": "Water"},
            8: {"name": "Sagittarius", "symbol": "♐", "sanskrit": "धनु", "element": "Fire"},
            9: {"name": "Capricorn", "symbol": "♑", "sanskrit": "मकर", "element": "Earth"},
            10: {"name": "Aquarius", "symbol": "♒", "sanskrit": "कुंभ", "element": "Air"},
            11: {"name": "Pisces", "symbol": "♓", "sanskrit": "मीन", "element": "Water"}
        }
        
        # Houses
        self.houses = {
            1: {"name": "First House", "sanskrit": "लग्न", "meaning": "Self, personality, appearance"},
            2: {"name": "Second House", "sanskrit": "धन", "meaning": "Wealth, possessions, family"},
            3: {"name": "Third House", "sanskrit": "सहोदर", "meaning": "Communication, siblings, short journeys"},
            4: {"name": "Fourth House", "sanskrit": "सुख", "meaning": "Home, mother, property"},
            5: {"name": "Fifth House", "sanskrit": "पुत्र", "meaning": "Children, creativity, romance"},
            6: {"name": "Sixth House", "sanskrit": "शत्रु", "meaning": "Health, enemies, service"},
            7: {"name": "Seventh House", "sanskrit": "विवाह", "meaning": "Marriage, partnerships, open enemies"},
            8: {"name": "Eighth House", "sanskrit": "मृत्यु", "meaning": "Death, transformation, occult"},
            9: {"name": "Ninth House", "sanskrit": "धर्म", "meaning": "Religion, higher education, long journeys"},
            10: {"name": "Tenth House", "sanskrit": "कर्म", "meaning": "Career, father, authority"},
            11: {"name": "Eleventh House", "sanskrit": "लाभ", "meaning": "Gains, friends, hopes"},
            12: {"name": "Twelfth House", "sanskrit": "व्यय", "meaning": "Losses, expenses, spirituality"}
        }
    
    def calculate_birth_chart(self, birth_date: str, birth_time: str, birth_place: str) -> Dict[str, Any]:
        """Calculate complete birth chart using Swiss Ephemeris."""
        try:
            # Parse birth date and time
            dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            julian_day = self._date_to_julian_day(dt)
            
            # Get coordinates for birth place (simplified - in real implementation, use geocoding)
            lat, lon = self._get_coordinates(birth_place)
            
            # Calculate planetary positions
            planetary_positions = self._calculate_planetary_positions(julian_day)
            
            # Calculate houses
            house_positions = self._calculate_houses(julian_day, lat, lon)
            
            # Calculate aspects
            aspects = self._calculate_aspects(planetary_positions)
            
            # Create birth chart
            birth_chart = {
                "birth_date": birth_date,
                "birth_time": birth_time,
                "birth_place": birth_place,
                "julian_day": julian_day,
                "coordinates": {"latitude": lat, "longitude": lon},
                "planetary_positions": planetary_positions,
                "house_positions": house_positions,
                "aspects": aspects,
                "calculated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Birth chart calculated successfully for {birth_date} {birth_time}")
            return birth_chart
            
        except Exception as e:
            logger.error(f"Error calculating birth chart: {e}")
            return {"error": f"Could not calculate birth chart: {str(e)}"}
    
    def _date_to_julian_day(self, dt: datetime) -> float:
        """Convert datetime to Julian Day."""
        return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0)
    
    def _get_coordinates(self, birth_place: str) -> Tuple[float, float]:
        """Get coordinates for birth place (simplified)."""
        # Common Indian cities coordinates (in real implementation, use geocoding API)
        city_coordinates = {
            "mumbai": (19.0760, 72.8777),
            "delhi": (28.7041, 77.1025),
            "bangalore": (12.9716, 77.5946),
            "hyderabad": (17.3850, 78.4867),
            "chennai": (13.0827, 80.2707),
            "kolkata": (22.5726, 88.3639),
            "pune": (18.5204, 73.8567),
            "ahmedabad": (23.0225, 72.5714),
            "jaipur": (26.9124, 75.7873),
            "lucknow": (26.8467, 80.9462)
        }
        
        # Try to find exact match or partial match
        birth_place_lower = birth_place.lower()
        for city, coords in city_coordinates.items():
            if city in birth_place_lower:
                return coords
        
        # Default to Mumbai if not found
        return (19.0760, 72.8777)
    
    def _calculate_planetary_positions(self, julian_day: float) -> Dict[str, Any]:
        """Calculate planetary positions for given Julian Day."""
        planetary_positions = {}
        
        for planet_id, planet_info in self.planets.items():
            try:
                # Calculate planetary position
                result = swe.calc_ut(julian_day, planet_id)
                
                if result[0] == 0:  # Success
                    longitude = result[2][0]  # Longitude
                    latitude = result[2][1]   # Latitude
                    distance = result[2][2]   # Distance
                    speed = result[2][3]      # Speed
                    
                    # Calculate zodiac sign
                    sign_num = int(longitude / 30)
                    sign_degree = longitude % 30
                    
                    planetary_positions[planet_info["name"]] = {
                        "planet_id": planet_id,
                        "symbol": planet_info["symbol"],
                        "sanskrit_name": planet_info["sanskrit"],
                        "longitude": longitude,
                        "latitude": latitude,
                        "distance": distance,
                        "speed": speed,
                        "sign": {
                            "number": sign_num,
                            "name": self.zodiac_signs[sign_num]["name"],
                            "symbol": self.zodiac_signs[sign_num]["symbol"],
                            "sanskrit": self.zodiac_signs[sign_num]["sanskrit"],
                            "element": self.zodiac_signs[sign_num]["element"],
                            "degree": sign_degree
                        },
                        "house": None  # Will be calculated later
                    }
                    
            except Exception as e:
                logger.error(f"Error calculating position for {planet_info['name']}: {e}")
        
        return planetary_positions
    
    def _calculate_houses(self, julian_day: float, lat: float, lon: float) -> Dict[str, Any]:
        """Calculate house positions using Placidus system."""
        try:
            # Calculate houses using Placidus system
            houses = swe.houses(julian_day, lat, lon)[0]
            
            house_positions = {}
            for house_num in range(1, 13):
                house_longitude = houses[house_num - 1]
                sign_num = int(house_longitude / 30)
                sign_degree = house_longitude % 30
                
                house_positions[house_num] = {
                    "house_number": house_num,
                    "longitude": house_longitude,
                    "sign": {
                        "number": sign_num,
                        "name": self.zodiac_signs[sign_num]["name"],
                        "symbol": self.zodiac_signs[sign_num]["symbol"],
                        "sanskrit": self.zodiac_signs[sign_num]["sanskrit"],
                        "element": self.zodiac_signs[sign_num]["element"],
                        "degree": sign_degree
                    },
                    "meaning": self.houses[house_num]["meaning"],
                    "sanskrit_name": self.houses[house_num]["sanskrit"]
                }
            
            return house_positions
            
        except Exception as e:
            logger.error(f"Error calculating houses: {e}")
            return {}
    
    def _calculate_aspects(self, planetary_positions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate aspects between planets."""
        aspects = []
        planets_list = list(planetary_positions.keys())
        
        for i, planet1 in enumerate(planets_list):
            for planet2 in planets_list[i+1:]:
                if planet1 != planet2:
                    aspect = self._calculate_aspect(
                        planetary_positions[planet1]["longitude"],
                        planetary_positions[planet2]["longitude"]
                    )
                    if aspect:
                        aspects.append({
                            "planet1": planet1,
                            "planet2": planet2,
                            "aspect_type": aspect["type"],
                            "orb": aspect["orb"],
                            "influence": aspect["influence"]
                        })
        
        return aspects
    
    def _calculate_aspect(self, long1: float, long2: float) -> Optional[Dict[str, Any]]:
        """Calculate aspect between two longitudes."""
        diff = abs(long1 - long2)
        if diff > 180:
            diff = 360 - diff
        
        # Major aspects
        aspects = {
            "conjunction": {"angle": 0, "orb": 10, "influence": "Intense, focused energy"},
            "sextile": {"angle": 60, "orb": 6, "influence": "Harmonious, supportive"},
            "square": {"angle": 90, "orb": 8, "influence": "Challenging, dynamic"},
            "trine": {"angle": 120, "orb": 8, "influence": "Harmonious, flowing"},
            "opposition": {"angle": 180, "orb": 10, "influence": "Polarizing, awareness"}
        }
        
        for aspect_name, aspect_info in aspects.items():
            if abs(diff - aspect_info["angle"]) <= aspect_info["orb"]:
                return {
                    "type": aspect_name,
                    "orb": abs(diff - aspect_info["angle"]),
                    "influence": aspect_info["influence"]
                }
        
        return None
    
    def assign_planets_to_houses(self, birth_chart: Dict[str, Any]) -> Dict[str, Any]:
        """Assign planets to houses based on their positions."""
        planetary_positions = birth_chart["planetary_positions"]
        house_positions = birth_chart["house_positions"]
        
        for planet_name, planet_data in planetary_positions.items():
            planet_longitude = planet_data["longitude"]
            
            # Find which house the planet is in
            for house_num, house_data in house_positions.items():
                next_house_num = house_num + 1 if house_num < 12 else 1
                house_longitude = house_data["longitude"]
                next_house_longitude = house_positions[next_house_num]["longitude"]
                
                # Check if planet is in this house
                if house_longitude <= next_house_longitude:
                    if house_longitude <= planet_longitude < next_house_longitude:
                        planetary_positions[planet_name]["house"] = house_num
                        break
                else:  # House spans across 0° Aries
                    if planet_longitude >= house_longitude or planet_longitude < next_house_longitude:
                        planetary_positions[planet_name]["house"] = house_num
                        break
        
        return birth_chart
    
    def get_personalized_predictions(self, birth_chart: Dict[str, Any], prediction_type: str) -> Dict[str, Any]:
        """Generate personalized predictions based on birth chart."""
        try:
            planetary_positions = birth_chart["planetary_positions"]
            house_positions = birth_chart["house_positions"]
            aspects = birth_chart["aspects"]
            
            # Analyze current transits
            current_date = datetime.now()
            current_julian = self._date_to_julian_day(current_date)
            current_transits = self._calculate_planetary_positions(current_julian)
            
            # Generate predictions based on type
            if prediction_type == "daily":
                return self._generate_daily_prediction(planetary_positions, current_transits, aspects)
            elif prediction_type == "weekly":
                return self._generate_weekly_prediction(planetary_positions, current_transits, aspects)
            elif prediction_type == "monthly":
                return self._generate_monthly_prediction(planetary_positions, current_transits, aspects)
            elif prediction_type == "yearly":
                return self._generate_yearly_prediction(planetary_positions, current_transits, aspects)
            else:
                return self._generate_general_prediction(planetary_positions, current_transits, aspects)
                
        except Exception as e:
            logger.error(f"Error generating personalized predictions: {e}")
            return {"error": f"Could not generate predictions: {str(e)}"}
    
    def _generate_daily_prediction(self, natal_positions: Dict, transits: Dict, aspects: List) -> Dict[str, Any]:
        """Generate daily personalized prediction."""
        # Analyze Sun and Moon positions for daily energy
        sun_position = natal_positions.get("Sun", {})
        moon_position = natal_positions.get("Moon", {})
        
        daily_energy = self._analyze_daily_energy(sun_position, moon_position, transits)
        
        return {
            "prediction_type": "daily",
            "energy_level": daily_energy["level"],
            "focus_areas": daily_energy["focus_areas"],
            "challenges": daily_energy["challenges"],
            "opportunities": daily_energy["opportunities"],
            "recommendations": daily_energy["recommendations"],
            "cosmic_advice": daily_energy["cosmic_advice"]
        }
    
    def _analyze_daily_energy(self, sun_position: Dict, moon_position: Dict, transits: Dict) -> Dict[str, Any]:
        """Analyze daily cosmic energy."""
        # Simplified analysis based on Sun and Moon positions
        sun_sign = sun_position.get("sign", {}).get("element", "Fire")
        moon_sign = moon_position.get("sign", {}).get("element", "Fire")
        
        energy_analysis = {
            "level": "High" if sun_sign == moon_sign else "Moderate",
            "focus_areas": ["Personal growth", "Family harmony", "Health and wellness"],
            "challenges": ["Communication", "Patience", "Balance"],
            "opportunities": ["New beginnings", "Creative expression", "Family bonding"],
            "recommendations": [
                "Start your day with meditation",
                "Focus on family relationships",
                "Practice gratitude and appreciation",
                "Maintain work-life balance"
            ],
            "cosmic_advice": "Today's energy supports personal growth and family harmony. Focus on open communication and mutual understanding."
        }
        
        return energy_analysis
    
    def _generate_weekly_prediction(self, natal_positions: Dict, transits: Dict, aspects: List) -> Dict[str, Any]:
        """Generate weekly personalized prediction."""
        return {
            "prediction_type": "weekly",
            "theme": "Growth and Harmony",
            "focus_areas": ["Career development", "Family relationships", "Personal wellness"],
            "challenges": ["Time management", "Communication", "Work-life balance"],
            "opportunities": ["Skill development", "Family bonding", "Health improvement"],
            "recommendations": [
                "Plan family activities for the weekend",
                "Focus on career goals during weekdays",
                "Practice daily meditation",
                "Maintain healthy routines"
            ]
        }
    
    def _generate_monthly_prediction(self, natal_positions: Dict, transits: Dict, aspects: List) -> Dict[str, Any]:
        """Generate monthly personalized prediction."""
        return {
            "prediction_type": "monthly",
            "theme": "Transformation and Progress",
            "focus_areas": ["Long-term goals", "Family planning", "Personal development"],
            "challenges": ["Major decisions", "Life changes", "Adaptation"],
            "opportunities": ["Career advancement", "Family growth", "Personal achievement"],
            "recommendations": [
                "Review and set new goals",
                "Plan family activities",
                "Focus on personal development",
                "Maintain work-life harmony"
            ]
        }
    
    def _generate_yearly_prediction(self, natal_positions: Dict, transits: Dict, aspects: List) -> Dict[str, Any]:
        """Generate yearly personalized prediction."""
        return {
            "prediction_type": "yearly",
            "theme": "Major Life Changes and Growth",
            "focus_areas": ["Life purpose", "Career transformation", "Family expansion"],
            "challenges": ["Major life decisions", "Adaptation to changes", "Balancing priorities"],
            "opportunities": ["Career breakthrough", "Family growth", "Personal transformation"],
            "recommendations": [
                "Focus on long-term life goals",
                "Strengthen family bonds",
                "Invest in personal development",
                "Embrace new opportunities"
            ]
        }
    
    def _generate_general_prediction(self, natal_positions: Dict, transits: Dict, aspects: List) -> Dict[str, Any]:
        """Generate general personalized prediction."""
        return {
            "prediction_type": "general",
            "theme": "Personal Growth and Family Harmony",
            "focus_areas": ["Self-improvement", "Family relationships", "Health and wellness"],
            "challenges": ["Personal growth", "Communication", "Life balance"],
            "opportunities": ["Family bonding", "Personal development", "Spiritual growth"],
            "recommendations": [
                "Practice daily meditation",
                "Spend quality time with family",
                "Focus on personal goals",
                "Maintain healthy lifestyle"
            ]
        }


# Global astrology engine instance
astrology_engine = RealAstrologyEngine() 