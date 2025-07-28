"""
Advanced Astrology Analytics for Personal/Family Companion
Includes Dasha, Transits, Yogas, and detailed chart analysis
"""

import ephem
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from loguru import logger

class AdvancedAstrologyAnalytics:
    """Advanced astrology calculations for personal/family use."""
    
    def __init__(self):
        self.planets = {
            'Sun': ephem.Sun,
            'Moon': ephem.Moon,
            'Mercury': ephem.Mercury,
            'Venus': ephem.Venus,
            'Mars': ephem.Mars,
            'Jupiter': ephem.Jupiter,
            'Saturn': ephem.Saturn,
            'Rahu': None,  # Will be calculated
            'Ketu': None    # Will be calculated
        }
    
    def calculate_dasha(self, birth_date: str, birth_time: str) -> Dict[str, Any]:
        """Calculate Vimshottari Dasha periods."""
        try:
            # Parse birth date and time
            birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Calculate Moon's longitude at birth
            birth_place = ephem.Observer()
            birth_place.date = birth_dt
            moon = ephem.Moon()
            moon.compute(birth_place)
            
            # Calculate dasha periods (simplified Vimshottari)
            dasha_periods = {
                'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
                'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
            }
            
            # Calculate current dasha
            current_date = datetime.now()
            years_since_birth = (current_date - birth_dt).days / 365.25
            
            # Determine current dasha lord and period
            total_years = sum(dasha_periods.values())
            current_cycle = years_since_birth % total_years
            
            current_dasha = None
            accumulated_years = 0
            
            for planet, years in dasha_periods.items():
                if accumulated_years <= current_cycle < accumulated_years + years:
                    current_dasha = planet
                    break
                accumulated_years += years
            
            return {
                'current_dasha': current_dasha,
                'dasha_start': accumulated_years,
                'dasha_end': accumulated_years + dasha_periods.get(current_dasha, 0),
                'years_remaining': (accumulated_years + dasha_periods.get(current_dasha, 0)) - current_cycle
            }
            
        except Exception as e:
            logger.error(f"Error calculating dasha: {e}")
            return {'error': str(e)}
    
    def calculate_transits(self, birth_date: str, birth_time: str, birth_place: str) -> Dict[str, Any]:
        """Calculate current planetary transits and their effects."""
        try:
            # Parse birth details
            birth_dt = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
            
            # Set up observer for birth place
            observer = ephem.Observer()
            observer.lat = '19.0760'  # Default to Mumbai if place not parsed
            observer.lon = '72.8777'
            observer.date = datetime.now()
            
            transits = {}
            
            # Calculate current positions of planets
            for planet_name, planet_class in self.planets.items():
                if planet_class:
                    planet = planet_class()
                    planet.compute(observer)
                    transits[planet_name] = {
                        'longitude': float(planet.hlong),
                        'latitude': float(planet.hlat),
                        'distance': float(planet.earth_distance),
                        'phase': float(planet.phase) if hasattr(planet, 'phase') else 0
                    }
            
            return transits
            
        except Exception as e:
            logger.error(f"Error calculating transits: {e}")
            return {'error': str(e)}
    
    def detect_yogas(self, birth_chart: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect important yogas in the birth chart."""
        yogas = []
        
        try:
            # Check for common yogas
            sun_pos = birth_chart.get('Sun', {}).get('longitude', 0)
            moon_pos = birth_chart.get('Moon', {}).get('longitude', 0)
            
            # Gajakesari Yoga (Jupiter-Moon conjunction)
            jupiter_pos = birth_chart.get('Jupiter', {}).get('longitude', 0)
            if abs(jupiter_pos - moon_pos) < 30:  # Within 30 degrees
                yogas.append({
                    'name': 'Gajakesari Yoga',
                    'description': 'Jupiter-Moon conjunction brings wisdom and prosperity',
                    'strength': 'Strong' if abs(jupiter_pos - moon_pos) < 10 else 'Moderate'
                })
            
            # Budh-Aditya Yoga (Mercury-Sun conjunction)
            mercury_pos = birth_chart.get('Mercury', {}).get('longitude', 0)
            if abs(mercury_pos - sun_pos) < 15:  # Within 15 degrees
                yogas.append({
                    'name': 'Budh-Aditya Yoga',
                    'description': 'Mercury-Sun conjunction brings intelligence and communication skills',
                    'strength': 'Strong' if abs(mercury_pos - sun_pos) < 5 else 'Moderate'
                })
            
            # Shasha Yoga (Saturn-Moon conjunction)
            saturn_pos = birth_chart.get('Saturn', {}).get('longitude', 0)
            if abs(saturn_pos - moon_pos) < 30:
                yogas.append({
                    'name': 'Shasha Yoga',
                    'description': 'Saturn-Moon conjunction brings discipline and patience',
                    'strength': 'Strong' if abs(saturn_pos - moon_pos) < 10 else 'Moderate'
                })
            
            return yogas
            
        except Exception as e:
            logger.error(f"Error detecting yogas: {e}")
            return []
    
    def get_advanced_prediction(self, user_data: Dict[str, Any], prediction_type: str = 'daily') -> Dict[str, Any]:
        """Generate advanced prediction using dasha, transits, and yogas."""
        try:
            birth_date = user_data.get('birth_date')
            birth_time = user_data.get('birth_time')
            birth_place = user_data.get('birth_place', 'Mumbai, India')
            
            # Calculate advanced analytics
            dasha_info = self.calculate_dasha(birth_date, birth_time)
            transits = self.calculate_transits(birth_date, birth_time, birth_place)
            yogas = self.detect_yogas(transits)
            
            # Generate prediction based on analytics
            prediction = self._generate_advanced_prediction_text(
                dasha_info, transits, yogas, prediction_type, user_data.get('name', 'User')
            )
            
            return {
                'prediction': prediction,
                'dasha': dasha_info,
                'transits': transits,
                'yogas': yogas,
                'type': prediction_type
            }
            
        except Exception as e:
            logger.error(f"Error generating advanced prediction: {e}")
            return {'error': str(e)}
    
    def _generate_advanced_prediction_text(self, dasha: Dict, transits: Dict, yogas: List, 
                                         prediction_type: str, user_name: str) -> str:
        """Generate human-readable prediction text."""
        
        prediction_text = f"🌟 **Advanced {prediction_type.title()} Prediction for {user_name}**\n\n"
        
        # Dasha information
        if 'current_dasha' in dasha and not 'error' in dasha:
            prediction_text += f"**🕉️ Current Dasha:** {dasha['current_dasha']}\n"
            prediction_text += f"**⏰ Years Remaining:** {dasha.get('years_remaining', 0):.1f} years\n\n"
        
        # Transit information
        if 'Sun' in transits and not 'error' in transits:
            prediction_text += "**🌞 Current Transits:**\n"
            for planet, data in transits.items():
                if isinstance(data, dict) and 'longitude' in data:
                    prediction_text += f"• {planet}: {data['longitude']:.1f}°\n"
            prediction_text += "\n"
        
        # Yogas
        if yogas:
            prediction_text += "**✨ Active Yogas:**\n"
            for yoga in yogas:
                prediction_text += f"• {yoga['name']} ({yoga['strength']}): {yoga['description']}\n"
            prediction_text += "\n"
        
        # Personalized guidance
        prediction_text += "**💫 Cosmic Guidance:**\n"
        prediction_text += "Based on your advanced chart analysis, focus on:\n"
        prediction_text += "• Personal growth and spiritual development\n"
        prediction_text += "• Family harmony and relationships\n"
        prediction_text += "• Health and wellness practices\n"
        prediction_text += "• Career and life purpose alignment\n\n"
        
        prediction_text += "**🎯 Today's Focus:** Trust your intuition and follow your heart's calling! ✨"
        
        return prediction_text

# Global instance
advanced_analytics = AdvancedAstrologyAnalytics() 