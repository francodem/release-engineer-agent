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
        """
        Create a new AlertsReceiver that dispatches RawAlert items to the given processor using a bounded thread pool.
        
        Parameters:
            processor (IAlertProcessor): Processor instance used to handle each RawAlert.
            max_workers (int): Maximum number of worker threads in the internal ThreadPoolExecutor (default 8).
        """
        self._processor = processor
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def handle_webhook(self, payload: AlertmanagerPayload) -> None:
        """
        Dispatch each alert in an Alertmanager webhook payload to the processing pipeline.
        
        Parameters:
            payload (AlertmanagerPayload): Alertmanager webhook payload whose `alerts` list will be iterated and each contained RawAlert dispatched for processing.
        """
        for raw in payload.alerts:
            self._dispatch(raw)

    def _dispatch(self, raw: RawAlert) -> None:
        """
        Schedule processing of a RawAlert on the receiver's thread pool.
        
        Parameters:
            raw (RawAlert): The alert to submit for asynchronous processing by the configured IAlertProcessor.
        """
        self._executor.submit(self._processor.process, raw)

    def shutdown(self, wait: bool = True) -> None:
        """
        Shut down the receiver's worker pool, optionally waiting for in-flight tasks to complete.
        
        Parameters:
            wait (bool): If True, block until all running tasks complete; if False, return immediately without waiting for running tasks.
        """
        self._executor.shutdown(wait=wait)
