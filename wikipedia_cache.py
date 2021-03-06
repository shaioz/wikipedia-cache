from flask import Flask
import pymysql
import requests
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"


def get_cache_if_page_exists(page_requested):
    conn = pymysql.Connect(host="localhost", user="root", password="1q2w3e4r", db="wikipedia-cache")
    cur = conn.cursor()
    cur.execute("SELECT data from pages where name = %s", (page_requested))
    page_html_from_db = cur.fetchone()
    if page_html_from_db:
        cur.execute("SELECT TIMESTAMPDIFF(minute,(SELECT last_updated from pages where name = %s), now())", page_requested)
        time_diff = cur.fetchone()[0]          #####  time_diff is in minutes
        if time_diff > 60:
            return False
        return page_html_from_db
    return False


def get_cache_if_image_exists(image_requested):
    conn = pymysql.Connect(host="localhost", user="root", password="1q2w3e4r", db="wikipedia-cache")
    cur = conn.cursor()
    cur.execute("SELECT data from pages where name = %s", (image_requested))
    image_html_from_db = cur.fetchone()
    if image_html_from_db:
        cur.execute("SELECT TIMESTAMPDIFF(minute,(SELECT last_updated from images where name = %s), now())", image_requested)
        time_diff = cur.fetchone()[0]          #####  time_diff is in minutes
        if time_diff > 60:
            return False
        return image_html_from_db
    return False


def insert_to_pages_table(page_requested, new_html):
    last_updated = datetime.now()
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1q2w3e4r',
                                 db='wikipedia-cache')

    try:
        with connection.cursor() as cursor:
            sql = "REPLACE INTO `pages` (`name`, `data`, `last_updated`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (page_requested, new_html, last_updated))

        connection.commit()
    finally:
        connection.close()


def insert_to_images_table(image_requested, new_html):
    last_updated = datetime.now()
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1q2w3e4r',
                                 db='wikipedia-cache')

    try:
        with connection.cursor() as cursor:
            sql = "REPLACE INTO `images` (`name`, `data`, `last_updated`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (image_requested, new_html, last_updated))

        connection.commit()
    finally:
        connection.close()


@app.route('/<page_requested>')
def cache(page_requested):
    cache = get_cache_if_page_exists(page_requested)
    if not cache:
        response = requests.get("https://en.wikipedia.org/wiki/%s" % page_requested)
        response_html = response.content
        response_html = response_html.decode("utf-8")
        new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
        new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')


        new_html = new_html.encode('utf-8')
        insert_to_pages_table(page_requested, new_html)
        print("returning %s from wikipedia..." % page_requested)
        return new_html
    else:
        print("returning %s from db cache..." % page_requested)
        return cache


@app.route('/wiki/<image_requested>')
def cache_for_image(image_requested):
    cache = get_cache_if_image_exists(image_requested)
    if not cache:
        response = requests.get("https://en.wikipedia.org/wiki/%s" % image_requested)
        response_html = response.content
        response_html = response_html.decode("utf-8")
        new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
        new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')
        new_html = new_html.encode('utf-8')
        insert_to_images_table(image_requested, new_html)
        print("returning %s from wikipedia..." % image_requested)
        return new_html
    else:
        print("returning %s from db cache..." % image_requested)
        return cache


if __name__ == '__main__':
    app.run()

