import requests
import re
import warnings

warnings.filterwarnings("ignore")

DATA_URL = "https://www.gcettb.ac.in/js/data.js"


def fetch_notices():
    response = requests.get(
        DATA_URL,
        timeout=20,
        verify=False
    )

    response.raise_for_status()

    data = response.text

    # Extract ONLY the student notices array
    match = re.search(
        r"var\s+sNotices\s*=\s*\[(.*?)\];",
        data,
        re.DOTALL
    )

    if not match:
        raise RuntimeError("Could not find sNotices array")

    notices_data = match.group(1)

    # Extract individual notice objects
    pattern = re.compile(
        r"\{\s*id:\s*(\d+),\s*"
        r"text:\s*'([^']*)',\s*"
        r"newNotice:\s*(\d+),\s*"
        r"link:\s*'([^']*)'\s*\}"
    )

    matches = pattern.findall(notices_data)

    notices = []

    for notice_id, title, new_flag, link in matches:
        notices.append({
            "id": int(notice_id),
            "title": title.strip(),
            "new_notice": int(new_flag),
            "link": link.strip()
        })

    return notices


if __name__ == "__main__":
    notices = fetch_notices()

    print(f"Found {len(notices)} student notices.")
    print()

    for notice in notices[-10:]:
        print("Title:", notice["title"])
        print("Link :", notice["link"])
        print("-" * 80)