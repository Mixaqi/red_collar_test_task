import logging

from httpx import Client

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


logger = logging.getLogger(__name__)
_client = Client(base_url=f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/")


def _post(method: str, data: dict[str, str | int]) -> None:
    """Send a POST request to a Telegram Bot API method.

    Args:
        method (str): Telegram API method name (e.g., 'sendMessage').
        data (dict[str, str | int]): Data to include in the request.

    Raises:
        httpx.HTTPStatusError: If the Telegram API returns an error response.
    """
    response = _client.post(method, data=data)
    response.raise_for_status()


def send_message(text: str) -> None:
    """Send a message to the configured Telegram chat.

    Args:
        text (str): Text of the message to send.

    Raises:
        httpx.HTTPStatusError: If sending the message fails due to a Telegram API error.
    """
    logger.debug("Sending Telegram message: %s", text)
    _post("sendMessage", {"chat_id": TELEGRAM_CHAT_ID, "text": text})
