import time

from celery import shared_task


@shared_task
def test_task(message: str) -> str:
    print(f"Task received: {message}")
    time.sleep(2)
    return f"Processed: {message}"
