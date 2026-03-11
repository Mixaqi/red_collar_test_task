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
    """Abstract base model that provides self-updating created and updated fields.

    Attributes:
        created_at (DateTimeField): Timestamp when the object was created.
        updated_at (DateTimeField): Timestamp when the object was last updated.
    """

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OutboxStatus(TextChoices):
    """Enumeration of possible statuses for an OutboxTask."""

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OutboxTask(TimeStampedModel):
    """Represents a task to send a message

    Stores payload data, task name, status, and retry count. Used to track
    the execution of tasks such as sending Telegram messages.

    Attributes:
        id (UUIDField): UUID primary key of the task.
        task_name (CharField): Name of the task.
        status (CharField): Current status of the task (PENDING, SUCCESS, FAILED).
        retries (IntegerField): Number of times the task has been retried.
        payload (JSONField): Optional dictionary containing task-specific data.
    """

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
        """Mark the task as failed and update retry count.

        Logs a warning with task ID, name, and retries.

        Args:
            retries (int): Number of times the task has been retried.
        """
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
        """Mark the task as successful and update retry count.

        Logs info with task ID, name, and retries.

        Args:
            retries (int): Number of times the task has been retried.
        """
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
