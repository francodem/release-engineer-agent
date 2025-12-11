from __future__ import annotations

from datetime import datetime

from .interfaces import ISanitizer
from .models import RawAlert, SanitizedAlert


class BasicSanitizer(ISanitizer):
    """Extracts minimal, required fields from a RawAlert."""

    def sanitize(self, raw: RawAlert) -> SanitizedAlert:
        """
        Create a minimal SanitizedAlert by extracting key fields from a RawAlert.
        
        Parameters:
            raw (RawAlert): The incoming alert to sanitize.
        
        Returns:
            SanitizedAlert: A sanitized alert containing:
                - alert_name: from `raw.labels["alertname"]` or `"unknown_alert"`.
                - severity: from `raw.labels["severity"]` or `"unknown"`.
                - deployment_name: from `raw.labels["deployment"]`, otherwise `raw.labels["deployment_name"]`, otherwise `"unknown"`.
                - namespace: from `raw.labels["namespace"]` or `"default"`.
                - timestamp: from `raw.starts_at` or the current UTC time.
        """
        labels = raw.labels or {}
        alert_name = labels.get("alertname", "unknown_alert")
        severity = labels.get("severity", "unknown")
        deployment = labels.get("deployment", labels.get("deployment_name", "unknown"))
        namespace = labels.get("namespace", "default")
        timestamp = raw.starts_at or datetime.utcnow()

        return SanitizedAlert(
            alert_name=alert_name,
            severity=severity,
            deployment_name=deployment,
            namespace=namespace,
            timestamp=timestamp,
        )
