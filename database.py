import json
import os

DATABASE = "seen_notices.json"


def create_database():
    if not os.path.exists(DATABASE):
        with open(DATABASE, "w", encoding="utf-8") as file:
            json.dump([], file)


def load_notices():
    create_database()

    with open(DATABASE, "r", encoding="utf-8") as file:
        return json.load(file)


def notice_exists(link):
    notices = load_notices()
    return link in notices


def save_notice(title, link):
    notices = load_notices()

    if link not in notices:
        notices.append(link)

        with open(DATABASE, "w", encoding="utf-8") as file:
            json.dump(notices, file, indent=2)