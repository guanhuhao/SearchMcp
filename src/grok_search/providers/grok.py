import httpx
import json
from typing import List
from .base import BaseSearchProvider, SearchResult
from ..utils import search_prompt, fetch_prompt
from ..logger import log_info
from ..config import config


class GrokSearchProvider(BaseSearchProvider):
    def __init__(self, api_url: str, api_key: str, model: str = "grok-4-fast"):
        super().__init__(api_url, api_key)
        self.model = model

    def get_provider_name(self) -> str:
        return "Grok"

    async def search(self, query: str, platform: str = "", min_results: int = 3, max_results: int = 10, ctx=None) -> List[SearchResult]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        platform_prompt = ""
        return_prompt = ""

        if platform:
            platform_prompt = "\n\nYou should search the web for the information you need, and focus on these platform: " + platform

        if max_results:
            return_prompt = "\n\nYou should return the results in a JSON format, and the results should at least be " + str(min_results) + " and at most be " + str(max_results) + " results."

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": search_prompt,
                },
                {"role": "user", "content": query + platform_prompt + return_prompt },
            ],
            "stream": True,
        }

        await log_info(ctx, f"platform_prompt: { query + platform_prompt + return_prompt}", config.debug_enabled)

        timeout = httpx.Timeout(connect=6.0, read=50.0, write=10.0, pool=None)
        
        
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            async with client.stream(
                "POST",
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                content = await self._parse_streaming_response(response, ctx)

        return content

    async def fetch(self, url: str, ctx=None) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": fetch_prompt,
                },
                {"role": "user", "content": url + "\n获取该网页内容并返回其结构化Markdown格式" },
            ],
        }
        timeout = httpx.Timeout(connect=6.0, read=50.0, write=10.0, pool=None)

        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            async with client.stream(
                "POST",
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                response.raise_for_status()
                content = await self._parse_streaming_response(response, ctx)
        return content

    async def _parse_streaming_response(self, response, ctx=None) -> str:
        content = ""
        chunk_count = 0
        
        async for line in response.aiter_lines():
            line = line.strip()
            if not line or line == "data: [DONE]":
                continue
            if line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    if "content" in delta:
                        content += delta["content"]
                        chunk_count += 1
                        if chunk_count % 100 == 0:
                            preview = content[-100:] if len(content) > 100 else content
                except json.JSONDecodeError:
                    continue
        

        return content
