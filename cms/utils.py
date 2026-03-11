import logging

from django.db import transaction
from wagtail.models import Page

from cms.tasks import send_telegram_message
from config.models import OutboxStatus, OutboxTask


logger = logging.getLogger(__name__)


def enqueue_page_event(page: Page, message: str, task_name: str) -> None:
    """Create an OutboxTask for a page event and schedule a Telegram message.

    This function creates an OutboxTask instance with the given page information
    and message, marks it as pending, and schedules a Celery task to send the
    message to Telegram after the current database transaction commits.

    Args:
        page (Page): The Wagtail Page instance associated with this event.
        message (str): The message text to send via Telegram.
        task_name (str): The name of the task/event being logged."""
    outbox = OutboxTask.objects.create(
        payload={
            "page_id": page.id,
            "title": page.title,
            "message_text": message,
        },
        task_name=task_name,
        status=OutboxStatus.PENDING,
    )
    logger.info(
        "Enqueued page event: %s (ID = %s) with task '%s', outbox ID = %s",
        page.title,
        page.id,
        task_name,
        outbox.id,
    )

    transaction.on_commit(lambda: send_telegram_message.delay(outbox.id))
    logger.info(
        "Scheduled Celery task 'send_telegram_message' for Outbox ID = %s", outbox.id
    )
