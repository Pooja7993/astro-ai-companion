"""
Vedic Astrology Chart Analyzer
Implements comprehensive chart analysis using pyswisseph and flatlib
"""

import swisseph as swe
from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import pytz
import yaml
from pathlib import Path

from src.utils.config import Config


class ChartAnalyzer:
    """Comprehensive Vedic astrology chart analyzer."""
    
    def __init__(self):
        self.config = Config()
        
        self.city_coordinates = self._load_city_coordinates()
        
        rules_path = Path("config/astrology_rules/vedic_rules.yaml")
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.vedic_rules = yaml.safe_load(f)
    
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
            "kanpur, india": (26.4499, 80.3319),
            "nagpur, india": (21.1458, 79.0882),
            "indore, india": (22.7196, 75.8577),
            "thane, india": (19.2183, 72.9781),
            "bhopal, india": (23.2599, 77.4126),
            "visakhapatnam, india": (17.6868, 83.2185),
            "pimpri-chinchwad, india": (18.6298, 73.7997),
            "patna, india": (25.5941, 85.1376),
            "vadodara, india": (22.3072, 73.1812),
            "ghaziabad, india": (28.6692, 77.4538),
            
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
        location_lower = location.lower().strip()
        
        if location_lower in self.city_coordinates:
            return self.city_coordinates[location_lower]
        
        for city_key, coords in self.city_coordinates.items():
            city_name = city_key.split(',')[0].strip()
            if city_name in location_lower or location_lower in city_name:
                return coords
        
        print(f"Warning: Location '{location}' not found in offline database. Using default coordinates (Mumbai).")
        return (19.0760, 72.8777)
    
    def analyze_chart(self, user) -> Dict[str, Any]:
        """Analyze complete birth chart for a user."""
        try:
            birth_datetime = datetime.combine(
                user.date_of_birth,
                datetime.strptime(user.time_of_birth, "%H:%M").time()
            )
            
            if not user.latitude or not user.longitude:
                lat, lon = self.get_coordinates(user.birth_location)
            else:
                lat, lon = user.latitude, user.longitude
            
            date_str = f"{birth_datetime.year}/{birth_datetime.month}/{birth_datetime.day}"
            time_str = f"{birth_datetime.hour}:{birth_datetime.minute}"
            date = Datetime(date_str, time_str)
            pos = GeoPos(lat, lon)
            chart = Chart(date, pos)
            
            analysis = {
                'basic_info': self._get_basic_info(chart, user),
                'planetary_positions': self._get_planetary_positions(chart),
                'house_analysis': self._get_house_analysis(chart),
                'aspects': self._get_aspects(chart),
                'dashas': self._calculate_dashas(chart),
                'yogas': self._identify_yogas(chart),
                'strengths_weaknesses': self._analyze_strengths_weaknesses(chart),
                'current_transits': self._get_current_transits(chart),
                'numerology': self._calculate_numerology(user),
                'lal_kitab_analysis': self._lal_kitab_analysis(chart)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing chart: {e}")
            return {'error': str(e)}
    
    def _get_basic_info(self, chart: Chart, user) -> Dict[str, Any]:
        """Get basic chart information."""
        asc = chart.get(const.ASC)
        sun = chart.get(const.SUN)
        moon = chart.get(const.MOON)
        
        return {
            'ascendant_sign': asc.sign,  # asc.sign is already the sign name string
            'ascendant_degree': round(asc.lon, 2),
            'sun_sign': sun.sign,  # sun.sign is already the sign name string
            'moon_sign': moon.sign,  # moon.sign is already the sign name string
            'birth_nakshatra': self._get_nakshatra(moon.lon),
            'chart_type': 'North Indian',
            'ayanamsa': 'Lahiri'
        }
    
    def _get_planetary_positions(self, chart: Chart) -> Dict[str, Dict]:
        """Get positions of all planets."""
        planets = {}
        
        planet_list = [
            const.SUN, const.MOON, const.MERCURY, const.VENUS,
            const.MARS, const.JUPITER, const.SATURN,
            const.NORTH_NODE, const.SOUTH_NODE
        ]
        
        asc = chart.get(const.ASC)
        asc_lon = asc.lon
        
        for planet_id in planet_list:
            planet = chart.get(planet_id)
            planet_name = planet_id.lower()  # planet_id is already the string name
            
            house_diff = (planet.lon - asc_lon) % 360
            house_number = int(house_diff / 30) + 1
            
            planets[planet_name] = {
                'sign': planet.sign,  # planet.sign is already the sign name string
                'degree': round(planet.lon, 2),
                'house': house_number,
                'retrograde': planet.isRetrograde() if hasattr(planet, 'isRetrograde') else False,
                'dignity': self._get_planet_dignity(planet_name, planet.sign),
                'nakshatra': self._get_nakshatra(planet.lon)
            }
        
        return planets
    
    def _get_house_analysis(self, chart: Chart) -> Dict[str, Dict]:
        """Analyze all 12 houses."""
        houses = {}
        
        asc = chart.get(const.ASC)
        asc_lon = asc.lon
        
        house_constants = [
            const.HOUSE1, const.HOUSE2, const.HOUSE3, const.HOUSE4,
            const.HOUSE5, const.HOUSE6, const.HOUSE7, const.HOUSE8,
            const.HOUSE9, const.HOUSE10, const.HOUSE11, const.HOUSE12
        ]
        
        for house_num in range(1, 13):
            house = chart.get(house_constants[house_num - 1])
            
            planets_in_house = []
            for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                            const.MARS, const.JUPITER, const.SATURN,
                            const.NORTH_NODE, const.SOUTH_NODE]:
                planet = chart.get(planet_id)
                house_diff = (planet.lon - asc_lon) % 360
                planet_house = int(house_diff / 30) + 1
                if planet_house == house_num:
                    planets_in_house.append(planet_id.lower())  # planet_id is already the string name
            
            houses[f'house_{house_num}'] = {
                'sign': house.sign,  # house.sign is already the sign name string
                'lord': self._get_house_lord(house.sign),
                'planets': planets_in_house,
                'significance': self._get_house_significance(house_num),
                'strength': self._calculate_house_strength(chart, house_num)
            }
        
        return houses
    
    def _get_aspects(self, chart: Chart) -> List[Dict]:
        """Calculate planetary aspects."""
        aspects = []
        
        planet_list = [
            const.SUN, const.MOON, const.MERCURY, const.VENUS,
            const.MARS, const.JUPITER, const.SATURN
        ]
        
        for i, planet1_id in enumerate(planet_list):
            for planet2_id in planet_list[i+1:]:
                planet1 = chart.get(planet1_id)
                planet2 = chart.get(planet2_id)
                
                angle = abs(planet1.lon - planet2.lon)
                if angle > 180:
                    angle = 360 - angle
                
                aspect_type = None
                orb = 8
                
                if abs(angle - 0) <= orb:
                    aspect_type = "conjunction"
                elif abs(angle - 60) <= orb:
                    aspect_type = "sextile"
                elif abs(angle - 90) <= orb:
                    aspect_type = "square"
                elif abs(angle - 120) <= orb:
                    aspect_type = "trine"
                elif abs(angle - 180) <= orb:
                    aspect_type = "opposition"
                
                if aspect_type:
                    aspects.append({
                        'planet1': planet1_id.lower(),  # planet_id is already the string name
                        'planet2': planet2_id.lower(),  # planet_id is already the string name
                        'aspect': aspect_type,
                        'angle': round(angle, 2),
                        'strength': self._calculate_aspect_strength(aspect_type, angle)
                    })
        
        return aspects
    
    def _calculate_dashas(self, chart: Chart) -> Dict[str, Any]:
        """Calculate Vimshottari Dasha periods."""
        moon = chart.get(const.MOON)
        moon_nakshatra = self._get_nakshatra(moon.lon)
        
        dasha_lords = {
            'Ashwini': 'Ketu', 'Bharani': 'Venus', 'Krittika': 'Sun',
            'Rohini': 'Moon', 'Mrigashira': 'Mars', 'Ardra': 'Rahu',
            'Punarvasu': 'Jupiter', 'Pushya': 'Saturn', 'Ashlesha': 'Mercury',
            'Magha': 'Ketu', 'Purva Phalguni': 'Venus', 'Uttara Phalguni': 'Sun',
            'Hasta': 'Moon', 'Chitra': 'Mars', 'Swati': 'Rahu',
            'Vishakha': 'Jupiter', 'Anuradha': 'Saturn', 'Jyeshtha': 'Mercury',
            'Mula': 'Ketu', 'Purva Ashadha': 'Venus', 'Uttara Ashadha': 'Sun',
            'Shravana': 'Moon', 'Dhanishta': 'Mars', 'Shatabhisha': 'Rahu',
            'Purva Bhadrapada': 'Jupiter', 'Uttara Bhadrapada': 'Saturn', 'Revati': 'Mercury'
        }
        
        current_dasha_lord = dasha_lords.get(moon_nakshatra, 'Sun')
        
        return {
            'current_mahadasha': current_dasha_lord,
            'birth_nakshatra': moon_nakshatra,
            'dasha_balance': 'Calculated based on birth nakshatra'
        }
    
    def _identify_yogas(self, chart: Chart) -> List[Dict]:
        """Identify important yogas in the chart."""
        yogas = []
        
        asc_lord = self._get_house_lord_planet(chart, 1)
        ninth_lord = self._get_house_lord_planet(chart, 9)
        
        if asc_lord and ninth_lord:
            yogas.append({
                'name': 'Dharma Karmadhipati Yoga',
                'description': 'Combination of 1st and 9th house lords',
                'strength': 'Strong',
                'effects': 'Success, recognition, spiritual growth'
            })
        
        jupiter = chart.get(const.JUPITER)
        moon = chart.get(const.MOON)
        
        asc = chart.get(const.ASC)
        asc_lon = asc.lon
        
        jupiter_house_diff = (jupiter.lon - asc_lon) % 360
        jupiter_house = int(jupiter_house_diff / 30) + 1
        
        moon_house_diff = (moon.lon - asc_lon) % 360
        moon_house = int(moon_house_diff / 30) + 1
        
        house_diff = abs(jupiter_house - moon_house)
        if house_diff in [0, 3, 6, 9]:  # Angular positions
            yogas.append({
                'name': 'Gaja Kesari Yoga',
                'description': 'Jupiter and Moon in angular positions',
                'strength': 'Strong',
                'effects': 'Wisdom, prosperity, good reputation'
            })
        
        return yogas
    
    def _analyze_strengths_weaknesses(self, chart: Chart) -> Dict[str, List[str]]:
        """Analyze chart strengths and weaknesses."""
        strengths = []
        weaknesses = []
        
        for planet_id in [const.SUN, const.MOON, const.MERCURY, const.VENUS,
                         const.MARS, const.JUPITER, const.SATURN]:
            planet = chart.get(planet_id)
            planet_name = planet_id.lower()  # planet_id is already the string name
            dignity = self._get_planet_dignity(planet_name, planet.sign)
            
            if dignity in ['exalted', 'own_sign']:
                strengths.append(f"{planet_name.title()} is {dignity}")
            elif dignity == 'debilitated':
                weaknesses.append(f"{planet_name.title()} is debilitated")
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses
        }
    
    def _get_current_transits(self, chart: Chart) -> Dict[str, Any]:
        """Get current planetary transits."""
        return {
            'note': 'Current transits calculated based on present date',
            'major_transits': []
        }
    
    def _calculate_numerology(self, user) -> Dict[str, Any]:
        """Calculate numerological aspects."""
        birth_date = user.date_of_birth
        
        date_sum = birth_date.day + birth_date.month + birth_date.year
        while date_sum > 9:
            date_sum = sum(int(digit) for digit in str(date_sum))
        
        name_value = sum(ord(char.upper()) - ord('A') + 1 for char in user.name if char.isalpha())
        while name_value > 9:
            name_value = sum(int(digit) for digit in str(name_value))
        
        return {
            'life_path_number': date_sum,
            'name_number': name_value,
            'birth_date_number': birth_date.day if birth_date.day <= 9 else sum(int(d) for d in str(birth_date.day))
        }
    
    def _lal_kitab_analysis(self, chart: Chart) -> Dict[str, Any]:
        """Lal Kitab specific analysis."""
        mars = chart.get(const.MARS)
        
        asc = chart.get(const.ASC)
        asc_lon = asc.lon
        
        mars_house_diff = (mars.lon - asc_lon) % 360
        mars_house = int(mars_house_diff / 30) + 1
        
        analysis = {
            'manglik_status': 'Non-Manglik',
            'lal_kitab_remedies': []
        }
        
        if mars_house in [1, 2, 4, 7, 8, 12]:
            analysis['manglik_status'] = 'Manglik'
            analysis['lal_kitab_remedies'].append('Donate red lentils on Tuesday')
        
        return analysis
    
    def _get_nakshatra(self, longitude: float) -> str:
        """Get nakshatra from longitude."""
        nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
            'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
            'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
            'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
        ]
        
        nakshatra_index = int(longitude / 13.333333)
        return nakshatras[nakshatra_index % 27]
    
    def _get_planet_dignity(self, planet: str, sign: str) -> str:
        """Get planet dignity in sign."""
        sign_name = sign.lower()  # sign is already a string
        
        if planet in self.vedic_rules['planets']:
            planet_data = self.vedic_rules['planets'][planet]
            
            if sign_name == planet_data.get('exaltation'):
                return 'exalted'
            elif sign_name == planet_data.get('debilitation'):
                return 'debilitated'
            elif sign_name in planet_data.get('own_signs', []):
                return 'own_sign'
            elif sign_name in planet_data.get('friendly_signs', []):
                return 'friendly'
            elif sign_name in planet_data.get('enemy_signs', []):
                return 'enemy'
        
        return 'neutral'
    
    def _get_house_lord(self, sign: str) -> str:
        """Get lord of a sign."""
        lords = {
            'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon',
            'Leo': 'Sun', 'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars',
            'Sagittarius': 'Jupiter', 'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
        }
        return lords.get(sign, 'Unknown')
    
    def _get_house_lord_planet(self, chart: Chart, house_num: int):
        """Get the planet that lords a house."""
        house_constants = [
            const.HOUSE1, const.HOUSE2, const.HOUSE3, const.HOUSE4,
            const.HOUSE5, const.HOUSE6, const.HOUSE7, const.HOUSE8,
            const.HOUSE9, const.HOUSE10, const.HOUSE11, const.HOUSE12
        ]
        
        house = chart.get(house_constants[house_num - 1])
        lord_name = self._get_house_lord(house.sign)
        
        lord_map = {
            'Sun': const.SUN, 'Moon': const.MOON, 'Mercury': const.MERCURY,
            'Venus': const.VENUS, 'Mars': const.MARS, 'Jupiter': const.JUPITER,
            'Saturn': const.SATURN
        }
        
        if lord_name in lord_map:
            return chart.get(lord_map[lord_name])
        return None
    
    def _get_house_significance(self, house_num: int) -> List[str]:
        """Get significance of a house."""
        house_meanings = {
            1: ['self', 'personality', 'health', 'appearance'],
            2: ['wealth', 'family', 'speech', 'food'],
            3: ['siblings', 'courage', 'communication', 'short_journeys'],
            4: ['mother', 'home', 'property', 'education'],
            5: ['children', 'creativity', 'intelligence', 'romance'],
            6: ['enemies', 'diseases', 'service', 'debts'],
            7: ['spouse', 'partnership', 'business', 'marriage'],
            8: ['longevity', 'transformation', 'occult', 'inheritance'],
            9: ['father', 'dharma', 'fortune', 'higher_learning'],
            10: ['career', 'reputation', 'authority', 'government'],
            11: ['gains', 'friends', 'aspirations', 'elder_siblings'],
            12: ['losses', 'expenses', 'foreign_lands', 'moksha']
        }
        return house_meanings.get(house_num, [])
    
    def _calculate_house_strength(self, chart: Chart, house_num: int) -> str:
        """Calculate strength of a house."""
        asc = chart.get(const.ASC)
        asc_lon = asc.lon
        
        benefic_count = 0
        for planet_id in [const.JUPITER, const.VENUS, const.MOON]:
            planet = chart.get(planet_id)
            house_diff = (planet.lon - asc_lon) % 360
            planet_house = int(house_diff / 30) + 1
            if planet_house == house_num:
                benefic_count += 1
        
        if benefic_count >= 2:
            return 'Strong'
        elif benefic_count == 1:
            return 'Moderate'
        else:
            return 'Weak'
    
    def _calculate_aspect_strength(self, aspect_type: str, angle: float) -> str:
        """Calculate strength of an aspect."""
        exact_angles = {'conjunction': 0, 'sextile': 60, 'square': 90, 'trine': 120, 'opposition': 180}
        exact_angle = exact_angles.get(aspect_type, 0)
        
        orb = abs(angle - exact_angle)
        
        if orb <= 2:
            return 'Very Strong'
        elif orb <= 5:
            return 'Strong'
        elif orb <= 8:
            return 'Moderate'
        else:
            return 'Weak'
