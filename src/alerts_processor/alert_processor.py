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
        """
        Initialize the AlertProcessor with its pipeline dependencies.
        
        Parameters:
            sanitizer: Component that sanitizes incoming raw alerts before validation.
            validator: Component that verifies alert validity and produces validation results.
            enricher: Component that enriches validated alerts with additional data.
            repository: Component that persists processed alerts.
        """
        self._sanitizer = sanitizer
        self._validator = validator
        self._enricher = enricher
        self._repository = repository

    def process(self, raw: RawAlert) -> ProcessedAlert:
        """
        Run a sanitize → validate → enrich → persist pipeline for a raw alert.
        
        Sanitizes the input, validates the sanitized result, enriches the validated data, and persists a ProcessedAlert. Invalid alerts are still enriched and saved with status "invalid" for auditing; valid alerts are saved with status "processed".
        
        Parameters:
            raw (RawAlert): The incoming raw alert to process.
        
        Returns:
            ProcessedAlert: The persisted processed alert containing a generated `alert_id`, `status` ("invalid" or "processed"), the enriched `payload`, and the `received_at` UTC timestamp.
        """
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
