import requests

page_requested = "Epic_Rap_Battles_of_History"

response = requests.get("https://en.wikipedia.org/wiki/%s" % page_requested)
response_html = response.content
with open("/Users/shaioz/%s.html" % page_requested, "w") as f:
    f.write(str(response_html))