from flask import Flask, render_template, request, redirect, url_for, session, flash
from gnews_scrape import getNews
import tracemalloc
tracemalloc.start()
import asyncio
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ourBlog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

@app.route("/addBlog", methods=['GET', 'POST'])
def addBlog():
    title = request.form['name']
    cont = request.form['message']
    dt=datetime.datetime.now()
    addBlog = blog(title=title, content=cont, date=dt.strftime("%c"))
    db.session.add(addBlog)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/blogs/")
def dispBlog():
    return render_template("showBlog.html", dispBlog = blog.query.all())


if __name__ == "__main__":
    app.run(debug=True)
