from flask import Flask
import pymysql
import requests
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

def get_cache_if_exists(page_requested):
    conn = pymysql.Connect(host="localhost", user="root", password="shai7588", db="wikipedia-cache")
    cur = conn.cursor()
    cur.execute("SELECT data from pages where name = %s", (page_requested))
    res = cur.fetchone()
    if res:
        return res
    return False


def insert_to_table(page_requested, new_html):
    last_updated = str(datetime.now())
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='shai7588',
                                 db='wikipedia-cache')

    try:
        with connection.cursor() as cursor:
            sql = "REPLACE INTO `pages` (`name`, `data`, `last_updated`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (page_requested, new_html, last_updated))

        connection.commit()
    finally:
        connection.close()


@app.route('/<page_requested>')
def cache(page_requested):
    cache = get_cache_if_exists(page_requested)
    if not cache:
        response = requests.get("https://en.wikipedia.org/wiki/%s" % page_requested)
        response_html = response.content
        response_html = response_html.decode("utf-8")
        new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
        new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')
        new_html = new_html.encode('utf-8')
        insert_to_table(page_requested, new_html)
        print("returning %s from wikipedia..." % page_requested)
        return new_html
    else:
        print("returning %s from db cache..." % page_requested)
        return cache


if __name__ == '__main__':
    app.run()

