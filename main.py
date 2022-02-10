from datetime import datetime, timezone
from time import ctime, sleep

from dotenv import load_dotenv, find_dotenv

from core import crawl_from_website, get_from_database

if __name__ == '__main__':
    load_dotenv(find_dotenv(), verbose=True)
    time = datetime(2020, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc).timestamp()
    magazines = get_from_database(time)
    delay = 2

    for key in magazines:
        print("====%(time)s Processing id: %(id)s ====" % {"time": ctime(), "id": key})
        magazine = magazines[key]
        crawl_from_website(magazine)
        sleep(delay)
