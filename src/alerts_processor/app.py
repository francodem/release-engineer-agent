from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from .alert_processor import AlertProcessor
from .alerts_receiver import AlertsReceiver
from .alerts_repository import AlertsRepository
from .basic_sanitizer import BasicSanitizer
from .k8s_client import KubernetesClient
from .k8s_enricher import K8sEnricher
from .k8s_validator import K8sValidator
from .models import AlertmanagerPayload, RawAlert


def _parse_alert(alert: Dict[str, Any]) -> RawAlert:
    """
    Convert a single Alertmanager alert dictionary into a RawAlert.
    
    Parses labels and annotations (defaults to empty dicts if missing), reads status (defaults to "firing"), and converts startsAt/endsAt timestamp strings to UTC datetimes. If a timestamp is missing or cannot be parsed, the current UTC time is used; ends_at is None when endsAt is not provided.
    
    Parameters:
        alert (Dict[str, Any]): Alertmanager alert payload dictionary; may contain keys "labels", "annotations", "status", "startsAt", and "endsAt".
    
    Returns:
        RawAlert: Structured alert with fields `labels`, `annotations`, `status`, `starts_at`, and `ends_at`.
    """
    labels = alert.get("labels", {}) or {}
    annotations = alert.get("annotations", {}) or {}
    status_ = alert.get("status", "firing")
    starts_at_raw = alert.get("startsAt")
    ends_at_raw = alert.get("endsAt")

    def _to_dt(value: Any) -> datetime:
        """
        Convert an ISO 8601 timestamp string to a datetime, falling back to the current UTC time when missing or invalid.
        
        Parameters:
            value (Any): An ISO 8601 timestamp string (e.g., "2023-01-02T15:04:05Z") or a falsy/invalid value.
        
        Returns:
            datetime: The parsed timestamp as a `datetime`, or the current UTC datetime when `value` is missing or cannot be parsed.
        """
        if not value:
            return datetime.utcnow()
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return datetime.utcnow()

    starts_at = _to_dt(starts_at_raw)
    ends_at = _to_dt(ends_at_raw) if ends_at_raw else None
    return RawAlert(
        labels=labels,
        annotations=annotations,
        status=status_,
        starts_at=starts_at,
        ends_at=ends_at,
    )


def _parse_payload(payload: Dict[str, Any]) -> AlertmanagerPayload:
    """
    Convert an Alertmanager webhook payload into an AlertmanagerPayload model.
    
    Parameters:
        payload (Dict[str, Any]): The raw webhook JSON payload; may include an "alerts" list of alert objects.
    
    Returns:
        AlertmanagerPayload: Parsed payload containing a list of RawAlert instances (empty list if input had no alerts).
    """
    alerts_raw: List[Dict[str, Any]] = payload.get("alerts") or []
    alerts = [_parse_alert(item) for item in alerts_raw]
    return AlertmanagerPayload(alerts=alerts)


# Build pipeline components
k8s_client = KubernetesClient()
sanitizer = BasicSanitizer()
validator = K8sValidator(k8s_client)
enricher = K8sEnricher(k8s_client)
repository = AlertsRepository()
processor = AlertProcessor(sanitizer, validator, enricher, repository)

max_workers = int(os.getenv("ALERTS_MAX_WORKERS", "8"))
receiver = AlertsReceiver(processor, max_workers=max_workers)

app = FastAPI(title="Alerts Processor Webhook")


@app.post("/alertmanager/webhook")
async def alertmanager_webhook(payload: Dict[str, Any]):
    """
    Handle an Alertmanager webhook payload and dispatch parsed alerts to the processing pipeline.
    
    Parses the incoming Alertmanager webhook payload and forwards the resulting alerts to the receiver for asynchronous processing. Always returns an acknowledgement response to prevent Alertmanager from retrying.
    
    Parameters:
        payload (Dict[str, Any]): The raw JSON payload received from Alertmanager.
    
    Returns:
        JSONResponse: A response with {"status": "accepted"} and HTTP 200 to acknowledge receipt.
    
    Raises:
        HTTPException: Raised with status 400 if the payload cannot be parsed or processed.
    """
    try:
        parsed = _parse_payload(payload)
        receiver.handle_webhook(parsed)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid payload: {exc}",
        ) from exc
    return JSONResponse({"status": "accepted"}, status_code=status.HTTP_200_OK)


@app.on_event("shutdown")
def _shutdown_executor() -> None:
    """
    Shut down the alerts receiver and wait for in-progress work to complete.
    
    Blocks until the receiver's shutdown completes (wait=True), allowing running tasks to finish and resources to be released.
    """
    receiver.shutdown(wait=True)
