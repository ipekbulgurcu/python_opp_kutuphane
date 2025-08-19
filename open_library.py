"""Open Library API client (Aşama 2)
Uses httpx to fetch book details by ISBN.
"""

from __future__ import annotations

import httpx


class OpenLibraryClient:
    BASE_URL = "https://openlibrary.org"

    def __init__(self, timeout_seconds: float = 10.0):
        self._timeout = timeout_seconds

    def fetch_by_isbn(self, isbn: str) -> dict:
        url = f"{self.BASE_URL}/isbn/{isbn}.json"
        try:
            resp = httpx.get(url, timeout=self._timeout)
            if resp.status_code == 404:
                raise ValueError("Kitap bulunamadı")
            resp.raise_for_status()
            data = resp.json()
            # authors alanı genelde key listesi; isimleri çözümlemek için ek istek gerekebilir.
            # Basit yaklaşım: authors -> name alanını varsa al, yoksa boş bırak.
            authors = []
            if isinstance(data.get("authors"), list):
                for a in data["authors"]:
                    if isinstance(a, dict) and "name" in a:
                        authors.append(a["name"])
            data["authors"] = authors
            return data
        except httpx.RequestError as e:
            raise RuntimeError(f"Ağ hatası: {e}")


