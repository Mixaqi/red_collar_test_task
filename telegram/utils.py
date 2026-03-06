from httpx import Client, HTTPStatusError

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


_client = Client(base_url=f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/")


def _post(method: str, data: dict[str, str | int]) -> None:
    response = _client.post(method, data=data)
    response.raise_for_status()


def send_message(text: str) -> None:
    try:
        _post("sendMessage", {"chat_id": TELEGRAM_CHAT_ID, "text": text})
    except HTTPStatusError as exc:
        print(f"Error: {exc.response.json()}")  # add logging
