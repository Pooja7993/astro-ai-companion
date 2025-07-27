"""
Simple Astrology Engine for Astro AI Companion
Personal Family Use - Ephem Integration
"""

import ephem
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import json
import logging

from src.utils.logging_setup import get_logger

logger = get_logger(__name__)


class SimpleAstrologyEngine:
    """Simple astrology calculation engine using Ephem."""
    
    def __init__(self):
        # Planetary symbols and names
        self.planets = {
            "Sun": {"symbol": "☉", "sanskrit": "सूर्य", "planet": ephem.Sun()},
            "Moon": {"symbol": "☽", "sanskrit": "चंद्र", "planet": ephem.Moon()},
            "Mercury": {"symbol": "☿", "sanskrit": "बुध", "planet": ephem.Mercury()},
            "Venus": {"symbol": "♀", "sanskrit": "शुक्र", "planet": ephem.Venus()},
            "Mars": {"symbol": "♂", "sanskrit": "मंगल", "planet": ephem.Mars()},
            "Jupiter": {"symbol": "♃", "sanskrit": "गुरु", "planet": ephem.Jupiter()},
            "Saturn": {"symbol": "♄", "sanskrit": "शनि", "planet": ephem.Saturn()}
        }
        
        # Zodiac signs
        self.zodiac_signs = {
            0: {"name": "Aries", "symbol": "♈", "sanskrit": "मेष", "element": "Fire", "start_deg": 0},
            30: {"name": "Taurus", "symbol": "♉", "sanskrit": "वृषभ", "element": "Earth", "start_deg": 30},
            60: {"name": "Gemini", "symbol": "♊", "sanskrit": "मिथुन", "element": "Air", "start_deg": 60},
            90: {"name": "Cancer", "symbol": "♋", "sanskrit": "कर्क", "element": "Water", "start_deg": 90},
            120: {"name": "Leo", "symbol": "♌", "sanskrit": "सिंह", "element": "Fire", "start_deg": 120},
            150: {"name": "Virgo", "symbol": "♍", "sanskrit": "कन्या", "element": "Earth", "start_deg": 150},
            180: {"name": "Libra", "symbol": "♎", "sanskrit": "तुला", "element": "Air", "start_deg": 180},
            210: {"name": "Scorpio", "symbol": "♏", "sanskrit": "वृश्चिक", "element": "Water", "start_deg": 210},
            240: {"name": "Sagittarius", "symbol": "♐", "sanskrit": "धनु", "element": "Fire", "start_deg": 240},
            270: {"name": "Capricorn", "symbol": "♑", "sanskrit": "मकर", "element": "Earth", "start_deg": 270},
            300: {"name": "Aquarius", "symbol": "♒", "sanskrit": "कुंभ", "element": "Air", "start_deg": 300},
            330: {"name": "Pisces", "symbol": "♓", "sanskrit": "मीन", "element": "Water", "start_deg": 330}
        }
    
    def calculate_birth_chart(self, birth_date: str, birth_time: str, birth_place: str) -> Dict[str, Any]:
        """Calculate simplified birth chart using Ephem."""
        try:
            # Parse birth date and time
            dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Get coordinates for birth place (simplified)
            lat, lon = self._get_coordinates(birth_place)
            
            # Calculate planetary positions
            planetary_positions = self._calculate_planetary_positions(dt)
            
            # Create birth chart
            birth_chart = {
                "birth_date": birth_date,
                "birth_time": birth_time,
                "birth_place": birth_place,
                "coordinates": {"latitude": lat, "longitude": lon},
                "planetary_positions": planetary_positions,
                "calculated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Birth chart calculated for {birth_date} {birth_time}")
            return birth_chart
            
        except Exception as e:
            logger.error(f"Error calculating birth chart: {e}")
            return self._get_default_birth_chart(birth_date, birth_time, birth_place)
    
    def _get_coordinates(self, birth_place: str) -> Tuple[float, float]:
        """Get coordinates for birth place (simplified)."""
        # Default coordinates for common places
        place_coordinates = {
            "mumbai": (19.0760, 72.8777),
            "delhi": (28.7041, 77.1025),
            "bangalore": (12.9716, 77.5946),
            "chennai": (13.0827, 80.2707),
            "kolkata": (22.5726, 88.3639),
            "hyderabad": (17.3850, 78.4867),
            "pune": (18.5204, 73.8567),
            "ahmedabad": (23.0225, 72.5714),
            "jaipur": (26.9124, 75.7873),
            "lucknow": (26.8467, 80.9462)
        }
        
        # Try to find coordinates
        place_lower = birth_place.lower()
        for place, coords in place_coordinates.items():
            if place in place_lower:
                return coords
        
        # Default to Mumbai if not found
        return (19.0760, 72.8777)
    
    def _calculate_planetary_positions(self, dt: datetime) -> Dict[str, Any]:
        """Calculate planetary positions using Ephem."""
        positions = {}
        
        for planet_name, planet_info in self.planets.items():
            try:
                planet = planet_info["planet"]
                planet.compute(dt)
                
                # Convert to degrees
                longitude = math.degrees(planet.hlong)
                latitude = math.degrees(planet.hlat)
                
                # Get zodiac sign
                sign = self._get_zodiac_sign(longitude)
                
                positions[planet_name] = {
                    "longitude": longitude,
                    "latitude": latitude,
                    "sign": sign,
                    "symbol": planet_info["symbol"],
                    "sanskrit": planet_info["sanskrit"]
                }
                
            except Exception as e:
                logger.warning(f"Error calculating {planet_name}: {e}")
                positions[planet_name] = {
                    "longitude": 0,
                    "latitude": 0,
                    "sign": "Aries",
                    "symbol": planet_info["symbol"],
                    "sanskrit": planet_info["sanskrit"]
                }
        
        return positions
    
    def _get_zodiac_sign(self, longitude: float) -> str:
        """Get zodiac sign from longitude."""
        # Normalize longitude to 0-360
        longitude = longitude % 360
        
        # Find the sign
        for start_deg, sign_info in self.zodiac_signs.items():
            if longitude >= start_deg and longitude < start_deg + 30:
                return sign_info["name"]
        
        return "Aries"  # Default
    
    def _get_default_birth_chart(self, birth_date: str, birth_time: str, birth_place: str) -> Dict[str, Any]:
        """Get default birth chart when calculation fails."""
        return {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_place": birth_place,
            "coordinates": {"latitude": 19.0760, "longitude": 72.8777},
            "planetary_positions": {
                "Sun": {"longitude": 0, "latitude": 0, "sign": "Aries", "symbol": "☉", "sanskrit": "सूर्य"},
                "Moon": {"longitude": 30, "latitude": 0, "sign": "Taurus", "symbol": "☽", "sanskrit": "चंद्र"},
                "Mercury": {"longitude": 60, "latitude": 0, "sign": "Gemini", "symbol": "☿", "sanskrit": "बुध"},
                "Venus": {"longitude": 90, "latitude": 0, "sign": "Cancer", "symbol": "♀", "sanskrit": "शुक्र"},
                "Mars": {"longitude": 120, "latitude": 0, "sign": "Leo", "symbol": "♂", "sanskrit": "मंगल"},
                "Jupiter": {"longitude": 150, "latitude": 0, "sign": "Virgo", "symbol": "♃", "sanskrit": "गुरु"},
                "Saturn": {"longitude": 180, "latitude": 0, "sign": "Libra", "symbol": "♄", "sanskrit": "शनि"}
            },
            "calculated_at": datetime.now().isoformat()
        }
    
    def get_personalized_predictions(self, birth_chart: Dict[str, Any], prediction_type: str) -> Dict[str, Any]:
        """Get personalized predictions based on birth chart."""
        try:
            planetary_positions = birth_chart.get("planetary_positions", {})
            
            if prediction_type == "daily":
                return self._generate_daily_prediction(planetary_positions)
            elif prediction_type == "weekly":
                return self._generate_weekly_prediction(planetary_positions)
            elif prediction_type == "monthly":
                return self._generate_monthly_prediction(planetary_positions)
            elif prediction_type == "yearly":
                return self._generate_yearly_prediction(planetary_positions)
            else:
                return self._generate_general_prediction(planetary_positions)
                
        except Exception as e:
            logger.error(f"Error generating predictions: {e}")
            return self._get_default_prediction(prediction_type)
    
    def _generate_daily_prediction(self, planetary_positions: Dict) -> Dict[str, Any]:
        """Generate daily prediction."""
        sun_sign = planetary_positions.get("Sun", {}).get("sign", "Aries")
        
        predictions = {
            "Aries": "Today is great for new beginnings and taking action. Your energy is high!",
            "Taurus": "Focus on stability and patience today. Good time for financial planning.",
            "Gemini": "Communication flows well today. Connect with friends and family.",
            "Cancer": "Emotional sensitivity is high. Spend time with loved ones.",
            "Leo": "Your charisma shines today. Lead with confidence and creativity.",
            "Virgo": "Attention to detail serves you well. Organize and plan carefully.",
            "Libra": "Balance and harmony are your focus. Resolve conflicts diplomatically.",
            "Scorpio": "Intuition is strong today. Trust your inner guidance.",
            "Sagittarius": "Adventure calls! Explore new ideas and expand your horizons.",
            "Capricorn": "Discipline and hard work bring rewards. Stay focused on goals.",
            "Aquarius": "Innovation and originality flow. Share your unique perspective.",
            "Pisces": "Creativity and spirituality are highlighted. Trust your dreams."
        }
        
        return {
            "prediction": predictions.get(sun_sign, "Today brings positive energy for growth and harmony."),
            "focus": "Family harmony and personal growth",
            "lucky_color": "Blue",
            "lucky_number": "7"
        }
    
    def _generate_weekly_prediction(self, planetary_positions: Dict) -> Dict[str, Any]:
        """Generate weekly prediction."""
        return {
            "prediction": "This week brings opportunities for family bonding and personal development. Focus on communication and understanding.",
            "focus": "Family relationships and health",
            "lucky_color": "Green",
            "lucky_number": "3"
        }
    
    def _generate_monthly_prediction(self, planetary_positions: Dict) -> Dict[str, Any]:
        """Generate monthly prediction."""
        return {
            "prediction": "This month emphasizes harmony and balance in your family life. Good time for planning and organization.",
            "focus": "Long-term goals and family planning",
            "lucky_color": "Purple",
            "lucky_number": "9"
        }
    
    def _generate_yearly_prediction(self, planetary_positions: Dict) -> Dict[str, Any]:
        """Generate yearly prediction."""
        return {
            "prediction": "This year brings growth, prosperity, and harmony to your family. Focus on health, wealth, and happiness.",
            "focus": "Overall family well-being and success",
            "lucky_color": "Gold",
            "lucky_number": "1"
        }
    
    def _generate_general_prediction(self, planetary_positions: Dict) -> Dict[str, Any]:
        """Generate general prediction."""
        return {
            "prediction": "The stars align for peace, harmony, and prosperity in your family life.",
            "focus": "General well-being and happiness",
            "lucky_color": "White",
            "lucky_number": "5"
        }
    
    def _get_default_prediction(self, prediction_type: str) -> Dict[str, Any]:
        """Get default prediction when calculation fails."""
        return {
            "prediction": "Today brings positive energy for your family. Focus on love, harmony, and peace.",
            "focus": "Family harmony and personal growth",
            "lucky_color": "Blue",
            "lucky_number": "7"
        }


# Global astrology engine instance
astrology_engine = SimpleAstrologyEngine() 