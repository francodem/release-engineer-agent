from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from .interfaces import IAlertsReceiver, IAlertProcessor
from .models import AlertmanagerPayload, RawAlert


class AlertsReceiver(IAlertsReceiver):
    """
    Receives Alertmanager webhook payloads and dispatches each RawAlert
    through the processing pipeline with bounded concurrency.
    """

    def __init__(self, processor: IAlertProcessor, max_workers: int = 8) -> None:
        self._processor = processor
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def handle_webhook(self, payload: AlertmanagerPayload) -> None:
        for raw in payload.alerts:
            self._dispatch(raw)

    def _dispatch(self, raw: RawAlert) -> None:
        self._executor.submit(self._processor.process, raw)

    def shutdown(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait)

