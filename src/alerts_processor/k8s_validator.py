from __future__ import annotations

from .interfaces import IValidator, IK8sClient
from .models import SanitizedAlert, ValidatedAlert


class K8sValidator(IValidator):
    """Validates that referenced Kubernetes resources exist."""

    def __init__(self, k8s_client: IK8sClient) -> None:
        """
        Create a K8sValidator using the provided Kubernetes client.
        
        Stores the given IK8sClient for use by validation methods.
        """
        self._k8s = k8s_client

    def validate(self, alert: SanitizedAlert) -> ValidatedAlert:
        """
        Validate that the Kubernetes namespace and deployment referenced by an alert exist.
        
        Parameters:
            alert (SanitizedAlert): Alert containing deployment_name, namespace, alert_name, and severity to validate.
        
        Returns:
            ValidatedAlert: Validation result. If the namespace is missing, `is_valid` is `False` and `reason` indicates the namespace was not found. If the deployment is missing, `is_valid` is `False` and `reason` indicates the deployment was not found. If both exist, `is_valid` is `True` and `reason` is `None`. The returned object preserves `deployment_name`, `namespace`, `alert_name`, and `severity` from the input alert.
        """
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
