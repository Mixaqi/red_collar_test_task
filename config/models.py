import logging
from uuid import uuid4

from django.db.models import (
    CharField,
    DateTimeField,
    IntegerField,
    JSONField,
    Model,
    TextChoices,
    UUIDField,
)


logger = logging.getLogger(__name__)


class TimeStampedModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OutboxStatus(TextChoices):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OutboxTask(TimeStampedModel):
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    task_name = CharField(max_length=255)
    status = CharField(
        max_length=20,
        choices=OutboxStatus.choices,
        default=OutboxStatus.PENDING,
    )
    retries = IntegerField(default=0)
    payload = JSONField(null=True, blank=True)

    def mark_failed(self, retries: int) -> None:
        self.status = OutboxStatus.FAILED
        self.retries = retries
        self.save(update_fields=["status", "retries"])
        logger.warning(
            "OutboxTask FAILED: ID = %s, task_name = '%s', retries=%s",
            self.id,
            self.task_name,
            retries,
        )

    def mark_success(self, retries: int) -> None:
        self.status = OutboxStatus.SUCCESS
        self.retries = retries
        self.save(update_fields=["status", "retries"])
        logger.info(
            "OutboxTask SUCCESS: ID = %s, task_name = '%s', retries = %s",
            self.id,
            self.task_name,
            retries,
        )

    def __str__(self) -> str:
        return f"{self.task_name} ({self.status})"
