from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from .interfaces import IAlertProcessor, ISanitizer, IValidator, IEnricher, IAlertsRepository
from .models import RawAlert, ProcessedAlert


class AlertProcessor(IAlertProcessor):
    """Pipeline: sanitize -> validate -> enrich -> persist."""

    def __init__(
        self,
        sanitizer: ISanitizer,
        validator: IValidator,
        enricher: IEnricher,
        repository: IAlertsRepository,
    ) -> None:
        self._sanitizer = sanitizer
        self._validator = validator
        self._enricher = enricher
        self._repository = repository

    def process(self, raw: RawAlert) -> ProcessedAlert:
        sanitized = self._sanitizer.sanitize(raw)
        validated = self._validator.validate(sanitized)

        # If invalid, we still persist with status "invalid" for auditing.
        if not validated.is_valid:
            enriched = self._enricher.enrich(validated)
            processed = ProcessedAlert(
                alert_id=str(uuid4()),
                status="invalid",
                payload=enriched,
                received_at=datetime.utcnow(),
            )
            self._repository.save(processed)
            return processed

        enriched = self._enricher.enrich(validated)
        processed = ProcessedAlert(
            alert_id=str(uuid4()),
            status="processed",
            payload=enriched,
            received_at=datetime.utcnow(),
        )
        self._repository.save(processed)
        return processed

