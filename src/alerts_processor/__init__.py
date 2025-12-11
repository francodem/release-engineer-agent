"""
Alerts Processor package implementing alert ingestion, validation, enrichment,
and persistence following the documented architecture.
"""

from .models import (
    AlertmanagerPayload,
    RawAlert,
    SanitizedAlert,
    ValidatedAlert,
    EnrichedAlert,
    ProcessedAlert,
    DeploymentInfo,
)
from .interfaces import (
    IAlertsReceiver,
    IAlertProcessor,
    ISanitizer,
    IValidator,
    IEnricher,
    IAlertsRepository,
    IK8sClient,
)
from .alerts_receiver import AlertsReceiver
from .alert_processor import AlertProcessor
from .basic_sanitizer import BasicSanitizer
from .k8s_validator import K8sValidator
from .k8s_enricher import K8sEnricher
from .alerts_repository import AlertsRepository
from .k8s_client import KubernetesClient

__all__ = [
    "AlertmanagerPayload",
    "RawAlert",
    "SanitizedAlert",
    "ValidatedAlert",
    "EnrichedAlert",
    "ProcessedAlert",
    "DeploymentInfo",
    "IAlertsReceiver",
    "IAlertProcessor",
    "ISanitizer",
    "IValidator",
    "IEnricher",
    "IAlertsRepository",
    "IK8sClient",
    "AlertsReceiver",
    "AlertProcessor",
    "BasicSanitizer",
    "K8sValidator",
    "K8sEnricher",
    "AlertsRepository",
    "KubernetesClient",
]

