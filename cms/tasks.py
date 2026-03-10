from celery import shared_task
from httpx import HTTPStatusError, RequestError

from config.models import OutboxStatus, OutboxTask
from telegram.utils import send_message


@shared_task(acks_late=True)
def send_telegram_message(outbox_id: str) -> None:
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

    except HTTPStatusError as e:
        outbox.status = OutboxStatus.FAILED
        print(e)  # add logging

    except RequestError as e:
        outbox.status = OutboxStatus.FAILED
        print(e)  # add logging

    except Exception as e:
        outbox.status = OutboxStatus.FAILED
        print(e)  # add logging

    outbox.save(update_fields=["status"])
