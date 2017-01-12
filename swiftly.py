from flask import Flask, render_template, request, url_for
from flask import make_response  # FOR SETTING SESSIONS VIA COOKIES
import datetime
import feedparser

app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'nytimes': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
             'spiegel': 'http://www.spiegel.de/schlagzeilen/tops/index.rss',
             'france24': 'http://www.france24.com/fr/france/rss',
             'ndtv': 'http://feeds.feedburner.com/ndtvnews-trending-news',
             'elpais': 'http://ep00.epimg.net/rss/elpais/portada.xml',
             'bbca': 'http://feeds.bbci.co.uk/arabic/rss.xml',
             'russia':  'https://russian.rt.com/inotv/s/rss/inotv_main.rss',
             }

DEFAULTS = {'publication': 'bbc'}


@app.route('/')
def home():
    # NEWS
    publication = get_value_with_fallback('publication')  # crete an instance of the function
    articles = get_news(publication)  # crete an instance of the function
    # SETTING COOKIES
    response = make_response(render_template('home.html', articles=articles, publication=publication))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('publication', publication, expires=expires)
    return response


def get_news(query):
    name = None
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)

    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


if __name__ == "__main__":
    app.run(port=5000, debug=True)
