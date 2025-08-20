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
            # Bazı ISBN uçları 302 ile /books/.. kaynağına yönlendirir.
            # Yönlendirmeleri takip ederek nihai JSON'u al.
            resp = httpx.get(url, timeout=self._timeout, follow_redirects=True)
            if resp.status_code == 404:
                raise ValueError("Kitap bulunamadı")
            resp.raise_for_status()
            data = resp.json()
            # Authors alanını isimlere çözümle
            authors_field = data.get("authors")
            author_names: list[str] = []
            if isinstance(authors_field, list):
                for a in authors_field:
                    if isinstance(a, dict):
                        # Bazı dönüşlerde doğrudan name bulunur
                        if "name" in a and isinstance(a["name"], str):
                            author_names.append(a["name"].strip())
                        # Çoğunlukla sadece key gelir: "/authors/OL...A"
                        elif "key" in a and isinstance(a["key"], str):
                            author_url = f"{self.BASE_URL}{a['key']}.json"
                            try:
                                a_resp = httpx.get(author_url, timeout=self._timeout, follow_redirects=True)
                                if a_resp.status_code == 200:
                                    a_data = a_resp.json()
                                    name = a_data.get("name")
                                    if isinstance(name, str) and name.strip():
                                        author_names.append(name.strip())
                            except httpx.RequestError:
                                # Yazar adı çözümlenemese de akışı bozmayalım
                                pass

            # Ek fallback: by_statement varsa ve yazar adları yoksa onu kullan
            if not author_names:
                by_stmt = data.get("by_statement")
                if isinstance(by_stmt, str) and by_stmt.strip():
                    author_names = [by_stmt.strip()]

            data["authors"] = author_names
            return data
        except httpx.RequestError as e:
            raise RuntimeError(f"Ağ hatası: {e}")


