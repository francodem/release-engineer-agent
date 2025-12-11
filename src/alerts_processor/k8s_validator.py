from __future__ import annotations

from .interfaces import IValidator, IK8sClient
from .models import SanitizedAlert, ValidatedAlert


class K8sValidator(IValidator):
    """Validates that referenced Kubernetes resources exist."""

    def __init__(self, k8s_client: IK8sClient) -> None:
        self._k8s = k8s_client

    def validate(self, alert: SanitizedAlert) -> ValidatedAlert:
        if not self._k8s.namespace_exists(alert.namespace):
            return ValidatedAlert(
                is_valid=False,
                reason=f"Namespace '{alert.namespace}' not found",
                deployment_name=alert.deployment_name,
                namespace=alert.namespace,
                alert_name=alert.alert_name,
                severity=alert.severity,
            )

        if not self._k8s.deployment_exists(alert.namespace, alert.deployment_name):
            return ValidatedAlert(
                is_valid=False,
                reason=f"Deployment '{alert.deployment_name}' not found",
                deployment_name=alert.deployment_name,
                namespace=alert.namespace,
                alert_name=alert.alert_name,
                severity=alert.severity,
            )

        return ValidatedAlert(
            is_valid=True,
            reason=None,
            deployment_name=alert.deployment_name,
            namespace=alert.namespace,
            alert_name=alert.alert_name,
            severity=alert.severity,
        )

