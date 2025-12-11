from __future__ import annotations

from .interfaces import IK8sClient
from .models import DeploymentInfo


class KubernetesClient(IK8sClient):
    """Lightweight placeholder client. Replace with the official Kubernetes client."""

    def deployment_exists(self, ns: str, name: str) -> bool:
        # TODO: Implement using Kubernetes Python client
        return True

    def namespace_exists(self, ns: str) -> bool:
        # TODO: Implement using Kubernetes Python client
        return True

    def get_deployment_info(self, ns: str, name: str) -> DeploymentInfo:
        # TODO: Implement real lookup
        return DeploymentInfo(
            replicas=3,
            available_replicas=3,
            updated_replicas=3,
            image="registry.example.com/app:latest",
        )

