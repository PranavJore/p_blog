from flask import Flask, render_template, request, redirect, url_for, session, flash
from gnews_scrape import getNews
import tracemalloc
tracemalloc.start()
import asyncio
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
    
try:
    db.create_all()
    print("DB create command")
except:
    pass

class blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    content = db.Column(db.String(10000))
    date = db.Column(db.String(100))

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
