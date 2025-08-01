"""
OpenRouter Service for Free LLM Integration
"""

import os
import json
from typing import Dict, Any, Optional
import httpx
from loguru import logger

class OpenRouterService:
    """Service for interacting with OpenRouter API."""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.default_model = "meta-llama/llama-3.1-8b-instruct:free"  # Free model
        
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY not found. AI features will be limited.")
    
    async def generate_response(self, prompt: str, system_prompt: str = None, model: str = None) -> str:
        """Generate response using OpenRouter API."""
        if not self.api_key:
            return "AI service not available. Please configure OpenRouter API key."
        
        try:
            model = model or self.default_model
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://astro-ai-companion.onrender.com",
                "X-Title": "Astro AI Companion"
            }
            
            data = {
                "model": model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                    return "Sorry, I couldn't generate a response at this time."
                    
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            return "Sorry, there was an error generating your response."
    
    async def get_available_models(self) -> list:
        """Get list of available models."""
        if not self.api_key:
            return []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("data", [])
                else:
                    logger.error(f"Error fetching models: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error fetching available models: {e}")
            return []

# Global instance
openrouter_service = OpenRouterService()