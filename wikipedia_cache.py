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
    # new_lines = []
    # for line in response_lines:
    #     if 'href="/w/' in line:
    #         new_line = line.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
    #         new_lines.append(new_line)
    #     elif 'src="/w/' in line:
    #         new_line = line.replace('src="/w/', 'src="https://en.wikipedia.org/w/')
    #         new_lines.append(new_line)
    #     else:
    #         new_lines.append(line)
    #
    # for line in new_lines:
    #     if 'href="' in line:
    #         print(line)
    #     elif 'src="' in line:
    #         print(line)
    #
    # new_html = "\\n".join(new_lines)
    new_html = response_html.replace('href="/w/', 'href="https://en.wikipedia.org/w/')
    new_html = new_html.replace('src="/w/', 'src="https://en.wikipedia.org/w/')

    return new_html

if __name__ == '__main__':
    app.run()
