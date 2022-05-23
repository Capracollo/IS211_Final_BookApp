import urllib.request
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import select
import json

# Activate environment from command prompt if you need to install packages with pip or conda
#    > conda activate IS211_FinalAssignment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    pagecount = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, pagecount):
        self.title = title
        self.author = author
        self.pagecount = pagecount


class Isbn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.Integer, nullable=False)

    def __init__(self, isbn):
        self.isbn = isbn


@app.route('/', methods=['POST', 'GET'])
def login():
    title = "Login"
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        if userid == 'admin' and password == 'password':
            return redirect('/dashboard')
        else:
            return render_template("index.html", title=title)
    else:
        return render_template("index.html", title=title)


@app.route('/dashboard', methods=['POST', 'GET'])
def displayall():
    title = "My Books"
    books = Books.query.order_by(Books.id)
    if request.method == 'POST':
        book_delete = request.form['ID']
        db.session.query(Books).filter(Books.id == book_delete).delete()
        db.session.commit()
        return render_template("dashboard.html", books=books, title=title)
    else:
        return render_template("dashboard.html", books=books, title=title)


@app.route('/search', methods=['POST', 'GET'])
def search():
    title = "Search for book"
    if request.method == 'POST':
        isbn = request.form['ISBN']
        try:
            newisbn = Isbn(isbn=isbn)
            db.session.add(newisbn)
            db.session.commit()
            r = urllib.request.urlopen(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
            data = json.load(r)
            book_title = data["items"][0]["volumeInfo"]["title"]
            author = data["items"][0]["volumeInfo"]["authors"][0]
            pagecount = data["items"][0]["volumeInfo"]["pageCount"]
            sentence = f'{book_title} by {author}, {pagecount} pages'
            return render_template("search.html", sentence=sentence)
        except:
            error = "That ISBN record does not exist. Please try another ISBN."
            return render_template("search.html", error=error)
    else:
        return render_template("search.html", title=title)


@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    title = "Addbook"
    if request.method == 'POST':
        isbn = db.session.query(Isbn.isbn).order_by(Isbn.id.desc()).first().isbn
        try:
            r = urllib.request.urlopen(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}')
            data = json.load(r)
            book_title = data["items"][0]["volumeInfo"]["title"]
            author = data["items"][0]["volumeInfo"]["authors"][0]
            pagecount = data["items"][0]["volumeInfo"]["pageCount"]
            newbook = Books(title=book_title, author=author, pagecount=pagecount)
            db.session.add(newbook)
            db.session.commit()
            return redirect('/search')
        except:
            error = "I couldn't add this book. Sorry."
            return render_template("search.html", error=error)
    else:
        return render_template("search.html", title=title)


if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)
