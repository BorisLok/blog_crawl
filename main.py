import os
from datetime import datetime, timezone
from time import ctime, sleep

from dotenv import load_dotenv, find_dotenv

from core import crawl_from_website, get_from_database, upload


def main(env: str, _now: float):
    delay = 2
    if env == "staging":
        log = os.getenv("LOG_STAGING_FILE_PATH")
        domain = os.getenv("STAGING_DOMAIN")
    else:
        log = os.getenv("LOG_PRODUCTION_FILE_PATH")
        domain = os.getenv("PRODUCTION_DOMAIN")

    with open(log, 'r') as f:
        try:
            time = float(f.readline())
        finally:
            time = datetime(2020, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc).timestamp()

    magazines = get_from_database(time)
    for key in magazines:
        print("====%(time)s Processing id: %(id)s ====" % {"time": ctime(), "id": key})
        magazine = magazines[key]
        crawl_from_website(magazine.magazine)
        sleep(delay)

    is_success = upload(magazines=magazines, domain=domain + "/blog")

    if is_success:
        with open(log, 'w') as f:
            f.write(str(_now))


if __name__ == '__main__':
    load_dotenv(find_dotenv(), verbose=True)
    now = datetime.now().replace(tzinfo=timezone.utc).timestamp()
    main("staging", now)
    main("production", now)
