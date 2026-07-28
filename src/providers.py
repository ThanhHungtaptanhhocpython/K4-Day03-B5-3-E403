"""
Multi-provider LLM adapter for the lab.
"""

from __future__ import annotations

import os
import sys

import requests
from dotenv import load_dotenv

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()


def _clean_env_value(value: str | None) -> str:
    """Normalize .env values that may include spaces or wrapping quotes."""
    return str(value or "").strip().strip('"').strip("'")


def _read_int_env(name: str, default: int, minimum: int = 1, maximum: int = 4000) -> int:
    raw_value = _clean_env_value(os.getenv(name))
    if not raw_value:
        return default
    try:
        value = int(raw_value)
    except ValueError:
        return default
    return max(minimum, min(value, maximum))


class BaseLLMProvider:
    """Base interface for all LLM providers."""

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider using a Google AI Studio API key."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = _clean_env_value(api_key or os.getenv("GEMINI_API_KEY"))
        self.model_name = _clean_env_value(model or os.getenv("LLM_MODEL")) or "gemini-2.5-flash"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return "[Gemini Error]: Chưa cấu hình GEMINI_API_KEY trong file .env."
        if not self.api_key.startswith("AIza"):
            return (
                "[Gemini Error]: GEMINI_API_KEY không đúng dạng API key. "
                "Hãy dùng key từ Google AI Studio, thường bắt đầu bằng 'AIza...', "
                "không dùng OAuth/access token."
            )
        try:
            from google import genai

            client = genai.Client(api_key=self.api_key)
            contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = client.models.generate_content(model=self.model_name, contents=contents)
            return response.text
        except Exception as exc:
            return f"[Gemini Exception]: {exc}"


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = _clean_env_value(api_key or os.getenv("OPENAI_API_KEY"))
        self.model_name = _clean_env_value(model or os.getenv("LLM_MODEL")) or "gpt-4o-mini"
        self.max_tokens = _read_int_env("MAX_TOKENS", 1500)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            return "[OpenAI Error]: Chưa cấu hình OPENAI_API_KEY trong file .env."
        try:
            import openai

            client = openai.OpenAI(api_key=self.api_key)
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:
            return f"[OpenAI Exception]: {exc}"


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude provider."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = _clean_env_value(api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.model_name = _clean_env_value(model or os.getenv("LLM_MODEL")) or "claude-3-haiku-20240307"
        self.max_tokens = _read_int_env("MAX_TOKENS", 1500)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_anthropic_api_key_here":
            return "[Anthropic Error]: Chưa cấu hình ANTHROPIC_API_KEY trong file .env."
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)
            kwargs = {
                "model": self.model_name,
                "max_tokens": self.max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            response = client.messages.create(**kwargs)
            return response.content[0].text
        except Exception as exc:
            return f"[Anthropic Exception]: {exc}"


class OpenRouterProvider(BaseLLMProvider):
    """OpenRouter provider."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = _clean_env_value(api_key or os.getenv("OPENROUTER_API_KEY"))
        self.model_name = _clean_env_value(model or os.getenv("LLM_MODEL")) or "google/gemini-2.5-flash"
        self.max_tokens = _read_int_env("MAX_TOKENS", 1500)

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            return "[OpenRouter Error]: Chưa cấu hình OPENROUTER_API_KEY trong file .env."
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
            }
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            if res.status_code == 200:
                data = res.json()
                return data["choices"][0]["message"]["content"]
            return f"[OpenRouter API Error {res.status_code}]: {res.text}"
        except Exception as exc:
            return f"[OpenRouter Exception]: {exc}"


class MockProvider(BaseLLMProvider):
    """Offline mock provider for running the lab without API keys."""

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return "🤖 [Mock Provider]: Phản hồi giả lập offline cho bài test."


def get_llm_provider(provider_name: str | None = None) -> BaseLLMProvider:
    """Select provider from LLM_PROVIDER."""
    name = _clean_env_value(provider_name or os.getenv("LLM_PROVIDER") or "mock").lower()

    if name == "gemini":
        return GeminiProvider()
    if name == "openai":
        return OpenAIProvider()
    if name == "anthropic":
        return AnthropicProvider()
    if name == "openrouter":
        return OpenRouterProvider()
    return MockProvider()


if __name__ == "__main__":
    print("=== TEST MULTI-PROVIDER LLM ADAPTER ===")
    provider = get_llm_provider()
    print(f"Provider: {provider.__class__.__name__}")
    print(f"Model: {getattr(provider, 'model_name', 'Offline Mock Mode')}")
    print(f"Max tokens: {getattr(provider, 'max_tokens', 'n/a')}")
    print(f"Response: {provider.generate('Trả lời đúng một câu: OK')}")