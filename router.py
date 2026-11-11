"""Маршрутизатор запросов к ИИ с балансировкой и fallback."""
from __future__ import annotations

import random
import threading
from dataclasses import dataclass, field


@dataclass
class Backend:
    name: str
    weight: int = 1
    failures: int = 0
    successes: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def healthy(self) -> bool:
        return self.failures < 5


@dataclass
class Response:
    backend: str
    data: object
    ok: bool


class Router:
    def __init__(self) -> None:
        self.backends: list[Backend] = []
        self._lock = threading.Lock()

    def add(self, backend: Backend) -> "Router":
        with self._lock:
            self.backends.append(backend)
        return self

    def _pick(self) -> Backend:
        healthy = [b for b in self.backends if b.healthy()]
        pool = healthy or self.backends
        return random.choices(pool, weights=[b.weight for b in pool], k=1)[0]

    def request(self, payload: dict) -> Response:
        attempts = len(self.backends) or 1
        for _ in range(attempts):
            b = self._pick()
            try:
                result = self._call(b, payload)
                with b.lock:
                    b.successes += 1
                return Response(b.name, result, True)
            except Exception:
                with b.lock:
                    b.failures += 1
        return Response("none", None, False)

    def _call(self, backend: Backend, payload: dict) -> object:
        # заглушка: здесь реальный вызов модели
        return {"echo": payload, "model": backend.name}
