from scraper import fetch_notices
from database import create_database, notice_exists, save_notice

create_database()

notices = fetch_notices()

print(f"Found {len(notices)} student notices.")

for notice in notices:
    if not notice_exists(notice["link"]):
        save_notice(
            notice["title"],
            notice["link"]
        )

print("All existing notices marked as seen.")