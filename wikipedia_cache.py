from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/<page_requested>')
def cache(page_requested):
    response = requests.get("https://en.wikipedia.org/wiki/%s" % page_requested)
    response_html = response.content
    response_html = response_html.decode("utf-8")
    new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
    new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')

    return new_html

if __name__ == '__main__':
    app.run()
