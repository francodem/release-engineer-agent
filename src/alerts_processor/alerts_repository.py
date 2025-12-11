from __future__ import annotations

from threading import Lock
from typing import List

from .interfaces import IAlertsRepository
from .models import ProcessedAlert


class AlertsRepository(IAlertsRepository):
    """In-memory repository. Replace with SQL/NoSQL implementation as needed."""

    def __init__(self) -> None:
        self._items: List[ProcessedAlert] = []
        self._lock = Lock()

    def save(self, alert: ProcessedAlert) -> None:
        with self._lock:
            self._items.append(alert)

    def all(self) -> List[ProcessedAlert]:
        with self._lock:
            return list(self._items)

