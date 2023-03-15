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

@app.route("/write")
def writeblog():
    return render_template("addblog.html")

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

# news jinja inheritance starts here
@app.route("/news/home")
def newsHome():
    return render_template("newshome.html")
@app.route("/news/home/<topic>")
def newsHomeTop(topic):
    if topic == 'top':
        getUrl = 'https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en'
    elif topic == 'techonlogy':
        getUrl = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSFFpZ0FQAQ?hl=en-GB&gl=GB&ceid=GB%3Aen'
    elif topic == 'business':
        getUrl = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3'
    elif topic == 'local':
        getUrl = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRFIyYlhBU0JXVnVMVWRDS0FBUAE?ceid=GB:en&oc=3';
    elif topic == 'sports':
        getUrl = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3';
    elif topic == 'science':
        getUrl = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp0Y1RjU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3';
    elif topic == 'entertainment':
        getUrl = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JXVnVMVWRDR2dKSFFpZ0FQAQ?ceid=GB:en&oc=3';
    title, time, auth, link  = asyncio.run(getNews(getUrl))
    combList = list(zip(title, link, auth, time))
    return render_template("news_top.html", news = combList, topic=topic)
@app.route("/news/home/technology")
def newsHomeTech():
    getUrl = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSFFpZ0FQAQ?hl=en-GB&gl=GB&ceid=GB%3Aen'
    title, time, auth, link  = asyncio.run(getNews(getUrl))
    print("links",link)
    combList = list(zip(title, link, auth, time))
    return render_template("news_top.html", news = combList)


if __name__ == "__main__":
    app.run(debug=True)
