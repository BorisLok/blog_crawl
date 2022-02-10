import io
from datetime import datetime, timezone

import yaml
from dotenv import load_dotenv, find_dotenv

from core import crawl_from_website, get_from_database
from magazine import Magazine, MagazineBuilder

if __name__ == '__main__':
    load_dotenv(find_dotenv(), verbose=True)
    time = datetime(2020, 1, 1, 0, 0, 0).replace(tzinfo=timezone.utc).timestamp()
    magazines = get_from_database(time)