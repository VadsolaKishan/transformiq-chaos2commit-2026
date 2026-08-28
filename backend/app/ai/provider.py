import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.config.settings import settings

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    @abstractmethod
    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Dict[str, Any],
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        pass

class OpenAIProvider(AIProvider):
    def __init__(self):
        import httpx
        self.client = httpx.AsyncClient(timeout=60.0)
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.base_url = settings.OPENAI_API_BASE or "https://api.openai.com/v1"

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Dict[str, Any],
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt_with_schema = f"{user_prompt}\n\nYou MUST return valid JSON conforming to this schema:\n{json.dumps(json_schema)}"
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_with_schema}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        
        resp = await self.client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        resp = await self.client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

class AzureOpenAIProvider(AIProvider):
    def __init__(self):
        import httpx
        self.client = httpx.AsyncClient(timeout=60.0)
        self.endpoint = settings.AZURE_OPENAI_ENDPOINT
        self.api_key = settings.AZURE_OPENAI_API_KEY
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT
        self.api_version = settings.AZURE_OPENAI_API_VERSION

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        json_schema: Dict[str, Any],
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not self.api_key or not self.endpoint:
            raise ValueError("Azure OpenAI credentials not configured")

        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        prompt_with_schema = f"{user_prompt}\n\nYou MUST return valid JSON conforming to this schema:\n{json.dumps(json_schema)}"
        
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_with_schema}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        resp = await self.client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        context_data: Optional[Dict[str, Any]] = None
    ) -> str:
        if not self.api_key or not self.endpoint:
            raise ValueError("Azure OpenAI credentials not configured")

        headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        payload = {
            "messages": messages,
            "temperature": 0.7
        }
        resp = await self.client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
