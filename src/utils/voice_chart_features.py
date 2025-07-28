"""
Voice and Chart Visualization Features
Includes TTS, birth chart images, and voice message support
"""

import io
import base64
from typing import Optional, Dict, Any
from loguru import logger
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge
import numpy as np

class VoiceChartFeatures:
    """Voice and chart visualization features for personal/family astrology."""
    
    def __init__(self):
        self.zodiac_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        self.zodiac_degrees = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
    
    def generate_birth_chart_image(self, user_data: Dict[str, Any]) -> Optional[bytes]:
        """Generate a birth chart image."""
        try:
            # Create figure
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_aspect('equal')
            
            # Draw outer circle (chart boundary)
            circle = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
            ax.add_patch(circle)
            
            # Draw zodiac divisions
            for i in range(12):
                angle = i * 30
                x = 0.8 * np.cos(np.radians(angle))
                y = 0.8 * np.sin(np.radians(angle))
                ax.text(x, y, self.zodiac_signs[i], ha='center', va='center', 
                       fontsize=8, fontweight='bold')
            
            # Add planets (simplified positions)
            planets = {
                'Sun': {'angle': 45, 'color': 'gold', 'size': 100},
                'Moon': {'angle': 120, 'color': 'silver', 'size': 80},
                'Mercury': {'angle': 60, 'color': 'green', 'size': 60},
                'Venus': {'angle': 90, 'color': 'pink', 'size': 70},
                'Mars': {'angle': 150, 'color': 'red', 'size': 65},
                'Jupiter': {'angle': 200, 'color': 'orange', 'size': 90},
                'Saturn': {'angle': 250, 'color': 'brown', 'size': 75}
            }
            
            for planet, data in planets.items():
                x = 0.6 * np.cos(np.radians(data['angle']))
                y = 0.6 * np.sin(np.radians(data['angle']))
                ax.scatter(x, y, s=data['size'], c=data['color'], alpha=0.7)
                ax.text(x, y, planet, ha='center', va='center', fontsize=6, fontweight='bold')
            
            # Add title
            ax.set_title(f"Birth Chart - {user_data.get('name', 'User')}", 
                        fontsize=14, fontweight='bold', pad=20)
            
            # Remove axes
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating birth chart image: {e}")
            return None
    
    def generate_prediction_image(self, prediction_text: str, user_name: str) -> Optional[bytes]:
        """Generate an image with prediction text."""
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            
            # Add background
            ax.set_facecolor('#f0f8ff')
            
            # Add title
            ax.text(5, 9, f"Daily Prediction for {user_name}", 
                   ha='center', va='center', fontsize=16, fontweight='bold')
            
            # Add prediction text (simplified)
            ax.text(5, 5, "🌟 Cosmic Guidance\n\nTrust your intuition\nand follow your heart's calling!", 
                   ha='center', va='center', fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))
            
            # Remove axes
            ax.set_xticks([])
            ax.set_yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            # Save to bytes
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            plt.close()
            
            return img_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error generating prediction image: {e}")
            return None
    
    def text_to_speech(self, text: str) -> Optional[bytes]:
        """Convert text to speech (simplified implementation)."""
        try:
            # For now, return None as we'll implement TTS later
            # This is a placeholder for future TTS integration
            logger.info(f"TTS requested for text: {text[:50]}...")
            return None
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return None
    
    def create_voice_message(self, text: str) -> Optional[bytes]:
        """Create a voice message from text."""
        try:
            # Placeholder for voice message creation
            # In a full implementation, this would use TTS libraries
            logger.info(f"Voice message requested for: {text[:50]}...")
            return None
        except Exception as e:
            logger.error(f"Error creating voice message: {e}")
            return None

# Global instance
voice_chart_features = VoiceChartFeatures() 