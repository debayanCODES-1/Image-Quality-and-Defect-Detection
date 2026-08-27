from __future__ import annotations

import os
from typing import Any

import requests


class ImaggaClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("IMAGGA_API_KEY")
        self.api_secret = os.getenv("IMAGGA_API_SECRET")
        base_url = os.getenv("IMAGGA_API_URL", "https://api.imagga.com").rstrip("/")
        self.category_url = os.getenv("IMAGGA_CATEGORY_URL", f"{base_url}/v2/categories/predict")
        self.tags_url = os.getenv("IMAGGA_TAGS_URL", f"{base_url}/v2/tags")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key and self.api_secret)

    def _request(self, url: str, contents: bytes, filename: str, content_type: str) -> dict[str, Any]:
        response = requests.post(
            url,
            auth=(self.api_key, self.api_secret),
            files={"image": (filename, contents, content_type)},
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def analyze(self, contents: bytes, filename: str, content_type: str | None) -> dict[str, Any]:
        if not self.enabled:
            return {"status": "disabled", "categories": [], "tags": []}

        try:
            category_payload = self._request(
                self.category_url, contents, filename, content_type or "application/octet-stream"
            )
            tags_payload = self._request(
                self.tags_url, contents, filename, content_type or "application/octet-stream"
            )
            return {
                "status": "available",
                "categories": category_payload.get("result", {}).get("categories", []),
                "tags": tags_payload.get("result", {}).get("tags", []),
            }
        except (requests.RequestException, ValueError) as error:
            return {
                "status": "error",
                "categories": [],
                "tags": [],
                "error": str(error),
            }


imagga = ImaggaClient()
