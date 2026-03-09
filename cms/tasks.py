from typing import Any

from celery import shared_task

from config.models import OutboxStatus, OutboxTask
from telegram.utils import send_message


@shared_task(bind=True, max_retries=3)
def send_telegram_message(self: Any, outbox_id: str) -> None:
    outbox = OutboxTask.objects.get(id=outbox_id)

    try:
        payload = outbox.payload
        if payload is None:
            outbox.status = OutboxStatus.FAILED
            outbox.save(update_fields=["status"])
            return

        text: str = payload["message_text"]
        send_message(text)

        outbox.status = OutboxStatus.SUCCESS
        outbox.save(update_fields=["status"])

    except Exception as e:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status", "updated_at"])

        raise self.retry(exc=e, countdown=10) from e
