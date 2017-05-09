from flask import Flask
import requests
import pymysql.cursors
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

def insert_to_table(page_requested, new_html):
    last_updated = str(datetime.now())
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='1q2w3e4r',
                                 db='wikipedia-cache',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "REPLACE INTO `pages` (`name`, `data`, `last_updated`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (page_requested, new_html, last_updated))

        connection.commit()
    finally:
        connection.close()


@app.route('/<page_requested>')
def cache(page_requested):
    response = requests.get("https://en.wikipedia.org/wiki/%s" % page_requested)
    response_html = response.content
    response_html = response_html.decode("utf-8")
    new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
    new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')
    insert_to_table(page_requested, new_html)

    return new_html

if __name__ == '__main__':
    app.run()

