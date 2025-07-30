import requests
from typing import Optional, Dict, Any, List, Tuple

class OpenRouterClient:
    def __init__(self, api_key: str, host: str = 'https://openrouter.ai/api'):
        self.api_key = api_key
        self.host = host.rstrip('/')
    
    def chat(self, prompt: str, model: str = 'openai/gpt-3.5-turbo', system_prompt: Optional[str] = None, context: Optional[List[int]] = None) -> str:
        """
        Send a chat request to OpenRouter API.
        
        Args:
            prompt: The user's message
            model: The model to use (default: openai/gpt-3.5-turbo)
            system_prompt: Optional system prompt
            context: Optional context for stateful conversations
            
        Returns:
            The model's response as a string
        """
        url = f"{self.host}/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://astro-ai-companion.app",  # Replace with your site URL
            "X-Title": "Astro AI Companion"  # Your app name
        }
        
        messages = [
            {"role": "system", "content": system_prompt or "You are a helpful astrology assistant."},
            {"role": "user", "content": prompt}
        ]
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if context:
            payload["context"] = context
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                return "No response from the model."
                
        except requests.exceptions.RequestException as e:
            return f"Error communicating with OpenRouter: {str(e)}"
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of available models from OpenRouter.
        
        Returns:
            List of model information dictionaries
        """
        url = f"{self.host}/v1/models"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "data" in data:
                return data["data"]
            else:
                return []
                
        except requests.exceptions.RequestException:
            return []
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test the connection to OpenRouter API and verify the API key.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        if not self.api_key or self.api_key.strip() == "":
            return False, "API key is missing"
        
        url = f"{self.host}/v1/models"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check for authentication errors
            if response.status_code == 401 or response.status_code == 403:
                return False, "Invalid API key or authentication failed"
            
            # Check for other errors
            if response.status_code != 200:
                return False, f"API error: HTTP {response.status_code}"
            
            # Verify we got a valid response
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                model_count = len(data["data"])
                return True, f"Connection successful. {model_count} models available."
            else:
                return False, "Connection successful but no models found"
                
        except requests.exceptions.ConnectionError:
            return False, "Connection error: Could not connect to OpenRouter"
        except requests.exceptions.Timeout:
            return False, "Connection error: Request timed out"
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"