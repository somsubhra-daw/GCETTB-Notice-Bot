import time
import logging

from scraper import fetch_notices
from database import create_database, notice_exists, save_notice
from telegram import send_message


# How often to check GCETTB
CHECK_INTERVAL = 10 * 60  # 10 minutes


# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def check_for_new_notices():
    logger.info("Checking GCETTB for new notices...")

    try:
        notices = fetch_notices()

        logger.info("Found %d student notices.", len(notices))

        new_count = 0

        for notice in notices:

            title = notice["title"]
            link = notice["link"]

            # Already sent/saved?
            if notice_exists(link):
                continue

            logger.info("New notice found: %s", title)

            try:
                send_message(title, link)

                save_notice(title, link)

                new_count += 1

                logger.info("Notification sent successfully.")

            except Exception as error:
                logger.error(
                    "Failed to send notice '%s': %s",
                    title,
                    error
                )

        if new_count == 0:
            logger.info("No new notices.")

        else:
            logger.info(
                "%d new notice(s) sent to Telegram.",
                new_count
            )

    except Exception as error:
        logger.exception(
            "Error while checking GCETTB: %s",
            error
        )


def main():
    logger.info("======================================")
    logger.info("GCETTB Notice Bot started")
    logger.info("Checking every 10 minutes")
    logger.info("======================================")

    create_database()

    while True:
        check_for_new_notices()

        logger.info(
            "Next check in %d minutes.",
            CHECK_INTERVAL // 60
        )

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()