from flask import Flask
import requests
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
post_URL = "http://www.livedinn.com/jokes_server/updatehoroscope.php"

signs = [
    "aries",
    "libra",
    "taurus",
    "gemini",
    "cancer",
    "leo",
    "virgo",
    "scorpio",
    "sagittarius",
    "capricon",
    "aquarius",
    "pisces"
]


@app.route("/")
def hello():
    for sign in signs:
        # get_URL = f"https://www.washingtonpost.com/entertainment/horoscopes/{sign}/"
        get_URL = f"https://www.astrotak.com/daily-horoscope/{sign}-daily-horoscope"

        headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
        page = requests.get(get_URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("script", {"id": "__NEXT_DATA__"})
        
        
        predition = results.text.strip()
        res = json.loads(predition)
        result = res['props']['pageProps']['zodiacData']['today']['prediction']
        body = {'sign': sign, 'txt' : json.dumps(result) }
        

        headers = {'Content-Type': 'application/json', 'User-Agent': 'PostmanRuntime/7.36.3'}
        session = requests.Session()
        session.headers.update(headers)

        response = session.post(post_URL, data=json.dumps(body))
        # print(f"{sign}: {response.__dict__ }")
        print(response.status_code)
        print(response.text)


if __name__ == "__main__":
    app.run()