from flask import Flask
import pymysql
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"


def check_if_page_cached(page_requested):
    return False


@app.route('/<page_requested>')
def cache(page_requested):
    is_cached = check_if_page_cached(page_requested)
    if not is_cached:
        response = requests.get("https://en.wikipedia.org/wiki/%s" % page_requested)
        response_html = response.content
        response_html = response_html.decode("utf-8")
        new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
        new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')
        return new_html


if __name__ == '__main__':
    app.run()
