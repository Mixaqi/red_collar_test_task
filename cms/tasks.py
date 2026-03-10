import logging
from typing import Any

from celery import Task, shared_task
from httpx import HTTPStatusError, RequestError

from config.models import OutboxTask
from telegram.utils import send_message


logger = logging.getLogger(__name__)


@shared_task(bind=True, acks_late=True, max_retries=5, default_retry_delay=30)
def send_telegram_message(self: Task, outbox_id: str) -> None:
    try:
        outbox: OutboxTask = OutboxTask.objects.get(id=outbox_id)
    except OutboxTask.DoesNotExist:
        logger.warning("OutboxTask %s not found", outbox_id)
        return

    payload: dict[str, Any] | None = outbox.payload
    if not payload or "message_text" not in payload:
        logger.error("Invalid payload for OutboxTask %s: %s", outbox_id, payload)
        outbox.mark_failed(self.request.retries)
        return

    try:
        logger.info("Sending Telegram message for OutboxTask %s", outbox_id)
        send_message(payload["message_text"])
        logger.info("Telegram message successfully sent for OutboxTask %s", outbox_id)
        outbox.mark_success(self.request.retries)

    except (RequestError, HTTPStatusError) as e:
        logger.warning(
            "Telegram request error for OutboxTask %s (retry %s): %s",
            outbox_id,
            self.request.retries,
            e,
        )
        outbox.mark_failed(self.request.retries)
        raise self.retry(exc=e) from e

    except Exception as e:
        logger.exception(
            "Unexpected error in send_telegram_message for OutboxTask %s. %s",
            outbox_id,
            e,
        )
        outbox.mark_failed(self.request.retries)
