from __future__ import annotations

from .interfaces import IEnricher, IK8sClient
from .models import EnrichedAlert, ValidatedAlert


class K8sEnricher(IEnricher):
    """Enriches alerts with live deployment metadata from Kubernetes."""

    def __init__(self, k8s_client: IK8sClient) -> None:
        """
        Initialize the enricher with a Kubernetes client used to fetch deployment metadata.
        
        Parameters:
            k8s_client (IK8sClient): Client used to retrieve deployment information from the cluster.
        """
        self._k8s = k8s_client

    def enrich(self, alert: ValidatedAlert) -> EnrichedAlert:
        """
        Enriches a validated alert with live Kubernetes deployment metadata.
        
        Parameters:
            alert (ValidatedAlert): The validated alert whose namespace and deployment_name are used to fetch deployment metadata.
        
        Returns:
            EnrichedAlert: An alert populated with `cluster_verified=True`, `deployment_info` retrieved from the cluster, and `alert_name` and `severity` copied from the input.
        """
        deployment_info = self._k8s.get_deployment_info(alert.namespace, alert.deployment_name)
        return EnrichedAlert(
            cluster_verified=True,
            deployment_info=deployment_info,
            alert_name=alert.alert_name,
            severity=alert.severity,
        )
