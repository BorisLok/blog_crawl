import os
from typing import Dict

import mysql.connector
import requests
import yaml
from bs4 import BeautifulSoup

from magazine import Magazine, MagazineBuilder


# Get the magazine information from website.
def crawl_from_website(magazine: Magazine):
    if magazine.url is None:
        raise Exception('magazine id: %(id)s' % {"id": magazine.id})
    response = requests.get(magazine.url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        with open("config.yml", "r") as stream:
            data = yaml.safe_load(stream=stream)
            for key, item in data.items():
                tag = item["tag"]
                tag_type = item["type"]
                if tag is not None:
                    html_tag = soup.select_one(tag)
                    value = None
                    if tag_type == "text":
                        value = html_tag.text if html_tag else ""
                    elif tag_type == "img":
                        value = html_tag["src"] if html_tag["src"].startswith("http") else html_tag["data-src"]

                    setattr(magazine, key, value)

    else:
        raise Exception('magazine id: %(id)s' % {"id": magazine.id})


# Get the magazine information from database.
def get_from_database(time):
    magazines = {}
    language = {}
    conn = None
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("MYSQL_DATABASE"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            port=os.getenv("MYSQL_PORT")
        )

        if conn.is_connected():
            print("==== database connect successful ====")
            cursor = conn.cursor()

            sql = """
                        SELECT
                            p.id,
                            p.post_title,
                            p.post_date_gmt,
                            p.post_modified_gmt,
                            p.`guid`,
                            wtt.taxonomy,
                            wt.name,
                            wt.slug
                        FROM `wp_posts` as p
                        LEFT JOIN `wp_term_relationships` as wtr on p.id = wtr.object_id
                        LEFT JOIN `wp_term_taxonomy` as wtt on wtr.term_taxonomy_id = wtt.term_taxonomy_id
                        LEFT JOIN `wp_terms` as wt on wtt.term_id = wt.term_id
                        where (
                            p.post_status = 'publish'
                            and (wtt.taxonomy = 'category' or wtt.taxonomy = 'post_tag' or wtt.taxonomy = 'language')
                            and UNIX_TIMESTAMP(p.post_modified_gmt) >= %(time)f
                        )
                    """ % {
                "time": time
            }

            cursor.execute(sql)

            for (identifier, title, createdAt, updatedAt, url, category, tag, slug) in cursor:
                if category == "language":
                    language[identifier] = slug
                elif identifier in magazines:
                    if category == "category":
                        magazines[identifier].set_category(tag)
                    else:
                        magazines[identifier].magazine.tags.add(tag)
                else:
                    magazine = MagazineBuilder()
                    magazine.set_id(identifier)
                    magazine.set_url(url)
                    magazine.set_title(title)
                    magazine.set_created_at(createdAt)
                    magazine.set_updated_at(updatedAt)
                    magazine.set_category(tag)
                    magazine.set_tags(set() if category == "category" else set(tag))
                    magazines[identifier] = magazine

            for key in magazines:
                magazines[key].set_language(
                    "zh" if language[key] is None or language[key] == "zh-tw" else language[key])
    except Exception as e:
        print("exception: ", e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
        return magazines


# upload magazine to the server
def upload(magazines: Dict[str, MagazineBuilder], domain: str):
    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*'
    }

    for key in magazines:
        magazine = magazines[key].magazine.to_json()
        response = requests.post(domain, json=[magazine], headers=headers)

        if not response.ok:
            print("==== upsert post to %(domain)s: %(id)s failed ====" % {"id": key, "domain": domain})
            return False

    return True
