from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class RawAlert:
    labels: Dict[str, str]
    annotations: Dict[str, str]
    status: str
    starts_at: datetime
    ends_at: Optional[datetime] = None


@dataclass
class SanitizedAlert:
    alert_name: str
    severity: str
    deployment_name: str
    namespace: str
    timestamp: datetime


@dataclass
class ValidatedAlert:
    is_valid: bool
    reason: Optional[str]
    deployment_name: str
    namespace: str
    alert_name: str
    severity: str


@dataclass
class DeploymentInfo:
    replicas: int
    available_replicas: int
    updated_replicas: int
    image: str


@dataclass
class EnrichedAlert:
    cluster_verified: bool
    deployment_info: DeploymentInfo
    alert_name: str
    severity: str


@dataclass
class ProcessedAlert:
    alert_id: str
    status: str
    payload: EnrichedAlert
    received_at: datetime


@dataclass
class AlertmanagerPayload:
    alerts: List[RawAlert]

