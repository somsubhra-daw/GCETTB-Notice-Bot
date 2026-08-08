import logging

from scraper import fetch_notices
from database import create_database, notice_exists, save_notice
from telegram import send_message


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def check_for_new_notices():
    logger.info("Checking GCETTB for new notices...")

    notices = fetch_notices()

    logger.info("Found %d student notices.", len(notices))

    new_count = 0

    for notice in notices:
        title = notice["title"]
        link = notice["link"]

        if notice_exists(link):
            continue

        logger.info("New notice: %s", title)

        try:
            send_message(title, link)

            save_notice(title, link)

            new_count += 1

            logger.info("Telegram notification sent.")

        except Exception as error:
            logger.error(
                "Failed to send notification: %s",
                error
            )

    if new_count == 0:
        logger.info("No new notices.")

    else:
        logger.info(
            "%d new notice(s) sent.",
            new_count
        )


if __name__ == "__main__":
    create_database()
    check_for_new_notices()