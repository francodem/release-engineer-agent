from __future__ import annotations

from typing import Protocol

from .models import (
    AlertmanagerPayload,
    RawAlert,
    SanitizedAlert,
    ValidatedAlert,
    EnrichedAlert,
    ProcessedAlert,
    DeploymentInfo,
)


class IAlertsReceiver(Protocol):
    def handle_webhook(self, payload: AlertmanagerPayload) -> None: """
Handle an incoming Alertmanager webhook payload.

Parameters:
    payload (AlertmanagerPayload): The webhook payload received from Alertmanager to be processed by the receiver.
"""
...


class IAlertProcessor(Protocol):
    def process(self, raw: RawAlert) -> ProcessedAlert: """
Convert a RawAlert into a ProcessedAlert suitable for persistence and downstream handling.

Parameters:
	raw (RawAlert): The unprocessed alert payload received from the source.

Returns:
	ProcessedAlert: The processed alert with normalized and enriched fields required by downstream consumers.
"""
...


class ISanitizer(Protocol):
    def sanitize(self, raw: RawAlert) -> SanitizedAlert: """
Prepare a RawAlert for downstream processing by producing a sanitized representation.

Parameters:
    raw (RawAlert): Incoming raw alert payload to be cleaned and normalized.

Returns:
    SanitizedAlert: Alert data with invalid or extraneous fields removed, required defaults applied, and values normalized for validation and enrichment.
"""
...


class IValidator(Protocol):
    def validate(self, alert: SanitizedAlert) -> ValidatedAlert: """
Validate a sanitized alert and produce a validated alert.

Parameters:
	alert (SanitizedAlert): A sanitized alert ready for validation.

Returns:
	validated_alert (ValidatedAlert): The alert after validation, including any validation metadata or status.
"""
...


class IEnricher(Protocol):
    def enrich(self, alert: ValidatedAlert) -> EnrichedAlert: """
Enriches a validated alert with additional contextual information.

Parameters:
	alert (ValidatedAlert): The validated alert to augment with enrichment data.

Returns:
	EnrichedAlert: The input alert augmented with enrichment metadata (for example, external lookups, related resource details, or contextual links).
"""
...


class IAlertsRepository(Protocol):
    def save(self, alert: ProcessedAlert) -> None: """
Persist a processed alert to the repository.

Parameters:
    alert (ProcessedAlert): The processed alert to persist.
"""
...


class IK8sClient(Protocol):
    def deployment_exists(self, ns: str, name: str) -> bool: """
Check whether a Kubernetes deployment with the given name exists in the specified namespace.

Parameters:
    ns (str): Kubernetes namespace to search.
    name (str): Name of the deployment to check.

Returns:
    bool: `True` if the deployment exists in the namespace, `False` otherwise.
"""
...

    def namespace_exists(self, ns: str) -> bool: """
Check whether a Kubernetes namespace exists.

Parameters:
    ns (str): The name of the Kubernetes namespace to check.

Returns:
    bool: `True` if the namespace exists, `False` otherwise.
"""
...

    def get_deployment_info(self, ns: str, name: str) -> DeploymentInfo: """
Retrieve metadata and status information for a Kubernetes Deployment in the given namespace.

Parameters:
    ns (str): Kubernetes namespace containing the deployment.
    name (str): Name of the deployment to retrieve.

Returns:
    deployment_info (DeploymentInfo): Deployment metadata and status for the specified namespace and name.
"""
...
