from __future__ import annotations

from .interfaces import IEnricher, IK8sClient
from .models import EnrichedAlert, ValidatedAlert


class K8sEnricher(IEnricher):
    """Enriches alerts with live deployment metadata from Kubernetes."""

    def __init__(self, k8s_client: IK8sClient) -> None:
        self._k8s = k8s_client

    def enrich(self, alert: ValidatedAlert) -> EnrichedAlert:
        deployment_info = self._k8s.get_deployment_info(alert.namespace, alert.deployment_name)
        return EnrichedAlert(
            cluster_verified=True,
            deployment_info=deployment_info,
            alert_name=alert.alert_name,
            severity=alert.severity,
        )

