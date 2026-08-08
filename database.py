import sqlite3

DATABASE = "notices.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def notice_exists(link):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM notices WHERE link = ?",
        (link,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None


def save_notice(title, link):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO notices (title, link)
        VALUES (?, ?)
        """,
        (title, link)
    )

    connection.commit()
    connection.close()