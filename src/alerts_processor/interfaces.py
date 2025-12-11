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
    def handle_webhook(self, payload: AlertmanagerPayload) -> None: ...


class IAlertProcessor(Protocol):
    def process(self, raw: RawAlert) -> ProcessedAlert: ...


class ISanitizer(Protocol):
    def sanitize(self, raw: RawAlert) -> SanitizedAlert: ...


class IValidator(Protocol):
    def validate(self, alert: SanitizedAlert) -> ValidatedAlert: ...


class IEnricher(Protocol):
    def enrich(self, alert: ValidatedAlert) -> EnrichedAlert: ...


class IAlertsRepository(Protocol):
    def save(self, alert: ProcessedAlert) -> None: ...


class IK8sClient(Protocol):
    def deployment_exists(self, ns: str, name: str) -> bool: ...

    def namespace_exists(self, ns: str) -> bool: ...

    def get_deployment_info(self, ns: str, name: str) -> DeploymentInfo: ...

