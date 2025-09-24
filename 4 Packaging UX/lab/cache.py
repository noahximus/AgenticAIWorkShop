import json, os, time
from typing import Any, Optional

class JsonCache:
    def __init__(self, path: str, ttl_sec: int = 600):
        self.path = path
        self.ttl = ttl_sec
        self._data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}

    def _save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key: str) -> Optional[Any]:
        item = self._data.get(key)
        if not item:
            return None
        ts = item.get("_ts", 0)
        if time.time() - ts > self.ttl:
            self._data.pop(key, None)
            self._save()
            return None
        return item.get("value")

    def set(self, key: str, value: Any):
        self._data[key] = {"_ts": time.time(), "value": value}
        self._save()
