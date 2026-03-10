from celery import Task, shared_task
from httpx import HTTPStatusError, RequestError

from config.models import OutboxStatus, OutboxTask
from telegram.utils import send_message


@shared_task(bind=True, acks_late=True, max_retries=5, default_retry_delay=30)
def send_telegram_message(self: Task, outbox_id: str) -> None:
    try:
        outbox: OutboxTask = OutboxTask.objects.get(id=outbox_id)
    except OutboxTask.DoesNotExist:
        return

    payload = outbox.payload
    if payload is None:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status"])
        return

    try:
        message_text: str = payload["message_text"]
        send_message(message_text)

        outbox.status = OutboxStatus.SUCCESS
        outbox.save(update_fields=["status"])

    except RequestError as e:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status"])

        raise self.retry(exc=e) from e

    except HTTPStatusError as e:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status"])

        raise self.retry(exc=e) from e

    except Exception:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status"])
