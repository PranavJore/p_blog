from flask import Flask, render_template, request, redirect, url_for, session, flash
from gnews_scrape import getNews
import tracemalloc
tracemalloc.start()
import asyncio

app = Flask(__name__)


@app.route("/news")
def home():
    # NewsList = getNews()
    title, time, auth, link  = asyncio.run(getNews())
    print("links",link)
    combList = list(zip(title, link, auth, time))
    return render_template("news.html", news = combList)


@app.route("/")
def index():
    
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
