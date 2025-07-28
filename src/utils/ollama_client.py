import requests

class OllamaClient:
    def __init__(self, host='http://localhost:11434'):
        self.host = host.rstrip('/')

    def chat(self, prompt, model='llama3', system_prompt=None, context=None):
        url = f"{self.host}/api/chat"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt or "You are a helpful astrology assistant."},
                {"role": "user", "content": prompt}
            ]
        }
        if context:
            payload["context"] = context
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"] if "message" in data else data.get("response", "") 