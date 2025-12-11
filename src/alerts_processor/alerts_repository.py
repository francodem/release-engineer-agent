from __future__ import annotations

from threading import Lock
from typing import List

from .interfaces import IAlertsRepository
from .models import ProcessedAlert


class AlertsRepository(IAlertsRepository):
    """In-memory repository. Replace with SQL/NoSQL implementation as needed."""

    def __init__(self) -> None:
        """
        Initialize the in-memory repository storage and its synchronization primitive.
        
        Creates an empty list used to store ProcessedAlert instances and a threading Lock to protect concurrent access to that list.
        """
        self._items: List[ProcessedAlert] = []
        self._lock = Lock()

    def save(self, alert: ProcessedAlert) -> None:
        """
        Store a processed alert in the repository.
        
        Appends the provided ProcessedAlert to the repository's in-memory store using a lock to ensure thread-safe writes.
        
        Parameters:
            alert (ProcessedAlert): The processed alert to persist in the repository.
        """
        with self._lock:
            self._items.append(alert)

    def all(self) -> List[ProcessedAlert]:
        """
        Return a shallow copy of all stored processed alerts.
        
        Returns:
            List[ProcessedAlert]: A new list containing the stored ProcessedAlert instances (shallow copy).
        """
        with self._lock:
            return list(self._items)
