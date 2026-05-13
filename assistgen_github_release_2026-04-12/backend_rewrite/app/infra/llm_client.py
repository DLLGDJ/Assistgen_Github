from __future__ import annotations

import json
from collections.abc import AsyncIterator

import httpx


class LLMClient:
    def __init__(
        self,
        provider: str,
        base_url: str,
        api_key: str,
        default_model: str,
        timeout_seconds: float = 60,
    ) -> None:
        self._provider = provider
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._default_model = default_model
        self._timeout = timeout_seconds

    def _resolve_model(self, model: str | None) -> str:
        return (model or self._default_model).strip() or self._default_model

    async def complete(self, prompt: str, model: str | None = None) -> str:
        if self._provider == "ollama":
            return await self._complete_with_ollama(prompt, model)
        if self._provider in {"deepseek", "openai"}:
            return await self._complete_with_openai_compat(prompt, model)
        return f"[mock:{self._resolve_model(model)}] {prompt}"

    async def stream(self, prompt: str, model: str | None = None) -> AsyncIterator[str]:
        if self._provider == "ollama":
            async for chunk in self._stream_with_ollama(prompt, model):
                yield chunk
            return

        if self._provider in {"deepseek", "openai"}:
            async for chunk in self._stream_with_openai_compat(prompt, model):
                yield chunk
            return

        staged = ["已接收问题，开始分析。", f"问题摘要：{prompt[:50]}", "这是 mock 模型输出，可切换到真实 LLM。"]
        for item in staged:
            yield item

    async def _complete_with_ollama(self, prompt: str, model: str | None) -> str:
        base_url = self._base_url or "http://127.0.0.1:11434"
        payload = {
            "model": self._resolve_model(model),
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(f"{base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return data.get("message", {}).get("content", "")

    async def _stream_with_ollama(self, prompt: str, model: str | None) -> AsyncIterator[str]:
        base_url = self._base_url or "http://127.0.0.1:11434"
        payload = {
            "model": self._resolve_model(model),
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream("POST", f"{base_url}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    line = line.strip()
                    if not line:
                        continue
                    data = json.loads(line)
                    chunk = data.get("message", {}).get("content", "")
                    if chunk:
                        yield chunk

    async def _complete_with_openai_compat(self, prompt: str, model: str | None) -> str:
        base_url = self._base_url or "https://api.deepseek.com"
        payload = {
            "model": self._resolve_model(model),
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(f"{base_url}/chat/completions", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "")

    async def _stream_with_openai_compat(self, prompt: str, model: str | None) -> AsyncIterator[str]:
        base_url = self._base_url or "https://api.deepseek.com"
        payload = {
            "model": self._resolve_model(model),
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            async with client.stream(
                "POST",
                f"{base_url}/chat/completions",
                json=payload,
                headers=headers,
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    line = line.strip()
                    if not line or not line.startswith("data:"):
                        continue
                    data_str = line[5:].strip()
                    if data_str == "[DONE]":
                        break
                    data = json.loads(data_str)
                    choices = data.get("choices", [])
                    if not choices:
                        continue
                    delta = choices[0].get("delta", {}).get("content", "")
                    if delta:
                        yield delta

