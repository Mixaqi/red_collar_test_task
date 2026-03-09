from celery import Task, shared_task

from config.models import OutboxStatus, OutboxTask
from telegram.utils import send_message


@shared_task(bind=True, acks_late=True)
def send_telegram_message(self: Task, outbox_id: str) -> None:
    outbox = OutboxTask.objects.get(id=outbox_id)

    payload = outbox.payload
    if payload is None:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status"])
        return

    try:
        text: str = payload["message_text"]
        send_message(text)

    except Exception:
        outbox.status = OutboxStatus.FAILED
        outbox.save(update_fields=["status"])

    else:
        outbox.status = OutboxStatus.SUCCESS
        outbox.save(update_fields=["status"])
