from django.db import transaction
from wagtail.models import Page

from cms.tasks import send_telegram_message
from config.models import OutboxStatus, OutboxTask


def enqueue_page_event(page: Page, message: str, task_name: str) -> None:
    outbox = OutboxTask.objects.create(
        payload={
            "page_id": page.id,
            "title": page.title,
            "message_text": message,
        },
        task_name=task_name,
        status=OutboxStatus.PENDING,
    )
    transaction.on_commit(lambda: send_telegram_message.delay(outbox.id))
