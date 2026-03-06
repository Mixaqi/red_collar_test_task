from uuid import uuid4

from django.db.models import (
    CharField,
    DateTimeField,
    JSONField,
    Model,
    TextChoices,
    UUIDField,
)


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
    payload = JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.task_name} ({self.status})"
