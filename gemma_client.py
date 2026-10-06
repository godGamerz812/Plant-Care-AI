import os
from typing import Any
import requests

class GemmaClient:
    def __init__(self) -> None:
        self.api_url = os.getenv("GEMMA_API_URL", "").strip()
        self.model = os.getenv("GEMMA_MODEL", "gemma-3-1b-it").strip()

    @property
    def is_configured(self) -> bool:
        return bool(self.api_url)

    def chat(self, prompt: str) -> str:
        if not self.api_url:
            raise RuntimeError("GEMMA_API_URL is not configured.")
        r = requests.post(self.api_url, json={"model": self.model, "prompt": prompt}, timeout=60)
        r.raise_for_status()
        data: Any = r.json()
        for key in ("response", "text", "output", "content"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value
        raise RuntimeError("Gemma endpoint returned no text.")
