from typing import Any

from celery import Task, shared_task
from httpx import HTTPStatusError, RequestError

from config.models import OutboxTask
from telegram.utils import send_message


@shared_task(bind=True, acks_late=True, max_retries=5, default_retry_delay=30)
def send_telegram_message(self: Task, outbox_id: str) -> None:
    try:
        outbox: OutboxTask = OutboxTask.objects.get(id=outbox_id)
    except OutboxTask.DoesNotExist:
        return

    payload: dict[str, Any] | None = outbox.payload
    if not payload or "message_text" not in payload:
        outbox.mark_failed(self.request.retries)
        return

    try:
        send_message(payload["message_text"])
        outbox.mark_success(self.request.retries)

    except (RequestError, HTTPStatusError) as e:
        outbox.mark_failed(self.request.retries)
        raise self.retry(exc=e) from e

    except Exception:
        outbox.mark_failed(self.request.retries)
