import io

import yaml
from core import crawl_from_website, get_from_database
from magazine import Magazine, MagazineBuilder

if __name__ == '__main__':
    magazine = MagazineBuilder()
    magazine.set_id("123")
    magazine.set_url("https://blog.velodash.co/2022/01/26/2022-spring-couplets/")
    crawl_from_website(magazine.magazine)
    print(magazine.magazine.to_json())