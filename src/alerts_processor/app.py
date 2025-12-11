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
    """Convert a single Alertmanager alert dict into RawAlert."""
    labels = alert.get("labels", {}) or {}
    annotations = alert.get("annotations", {}) or {}
    status_ = alert.get("status", "firing")
    starts_at_raw = alert.get("startsAt")
    ends_at_raw = alert.get("endsAt")

    def _to_dt(value: Any) -> datetime:
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
    Receives Alertmanager webhook payloads and dispatches alerts to the processor.
    Returns 200 immediately to avoid Alertmanager retries.
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
    receiver.shutdown(wait=True)

