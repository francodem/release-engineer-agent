from __future__ import annotations

from .interfaces import IK8sClient
from .models import DeploymentInfo


class KubernetesClient(IK8sClient):
    """Lightweight placeholder client. Replace with the official Kubernetes client."""

    def deployment_exists(self, ns: str, name: str) -> bool:
        # TODO: Implement using Kubernetes Python client
        """
        Check whether a Deployment with the given name exists in the specified Kubernetes namespace.
        
        Parameters:
            ns (str): Kubernetes namespace to query.
            name (str): Name of the Deployment to check.
        
        Returns:
            bool: `True` if the Deployment exists, `False` otherwise.
        """
        return True

    def namespace_exists(self, ns: str) -> bool:
        # TODO: Implement using Kubernetes Python client
        """
        Check whether a Kubernetes namespace exists.
        
        Parameters:
            ns (str): Name of the namespace to check.
        
        Returns:
            bool: `True` if the namespace exists, `False` otherwise. Note: current implementation is a placeholder and always returns `True`.
        """
        return True

    def get_deployment_info(self, ns: str, name: str) -> DeploymentInfo:
        # TODO: Implement real lookup
        """
        Return deployment metadata for the given deployment in the specified namespace.
        
        Returns:
            DeploymentInfo: Deployment information. Currently returns hardcoded values: replicas=3, available_replicas=3, updated_replicas=3, image="registry.example.com/app:latest".
        """
        return DeploymentInfo(
            replicas=3,
            available_replicas=3,
            updated_replicas=3,
            image="registry.example.com/app:latest",
        )
