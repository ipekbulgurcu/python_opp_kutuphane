from __future__ import annotations

import json
import os
from typing import List, Dict, Any


class Storage:
    """Abstract storage interface for Library persistence."""

    def read(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    def write(self, data: List[Dict[str, Any]]) -> None:
        raise NotImplementedError


class JsonFileStorage(Storage):
    """JSON file-based storage implementation."""

    def __init__(self, path: str) -> None:
        self.path = path

    def read(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            if isinstance(raw, list):
                return [item for item in raw if isinstance(item, dict)]
            return []
        except Exception:
            # Bozuk dosya durumunda sıfırdan başla
            return []

    def write(self, data: List[Dict[str, Any]]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


