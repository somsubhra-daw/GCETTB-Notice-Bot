import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing from .env")

if not CHAT_ID:
    raise RuntimeError("CHAT_ID is missing from .env")


def send_message(title, link):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    message = (
        "🔔 <b>New GCETTB Notice</b>\n\n"
        f"<b>{title}</b>\n\n"
        f"📄 <a href=\"{link}\">Open Notice</a>"
    )

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        },
        timeout=20
    )

    response.raise_for_status()

    result = response.json()

    if not result.get("ok"):
        raise RuntimeError(result)

    return True