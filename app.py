import os
import requests, json
from flask import Flask, session, request, render_template, redirect, flash, jsonify, url_for
from flask_session import Session
from sqlalchemy import create_engine, and_, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://nzcyryjmdzcgpe:3d72cb38f88503ad143713a9a6b040e5b3f8fba69b1d4b944983c3a55956f348@ec2-54-236-169-55.compute-1.amazonaws.com:5432/d82d3c2l0picn7")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/index")
def index():
    return "Project 1: TODO"

@app.route("/", methods=['GET', 'POST'])
def registerUser():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        checkEmail = db.execute("SELECT email FROM registrations WHERE email = :email", {"email": email}).fetchone()
        checkUsername = db.execute("SELECT username FROM registrations WHERE username = :username",
                                   {"username": username}).fetchone()
        if checkEmail and checkUsername:
            return redirect("/")
        elif checkUsername:
            return redirect("/")
        elif checkEmail:
            return redirect("/")
        elif name == "" or username == "" or password == "" or email == "":
            return redirect("/")
        else:
            db.execute(
                "INSERT INTO registrations(name, username, password, email) VALUES(:name, :username, :password, :email)",
                {"name": name, "username": username, "password": password, "email": email})
            db.commit()
            return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        checkUsername = db.execute(
            "SELECT username FROM registrations WHERE username = :username and password = :password",
            {"username": username, "password": password}).fetchone()
        # checkUsername = Registrations.query.filter(and_(Registrations.username == username, Registrations.password == password)).all()
        if checkUsername:
            session["user"] = checkUsername[0]
            # return redirect("/search")
            return redirect(url_for('home', username=username))
        else:
            return redirect("/login")

@app.route('/home/<username>', methods=['GET', 'POST'])
def home(username):
    if request.method == 'GET':
        return render_template('home.html', username=username)
    else:
        search = request.form.get('search')
        return redirect(url_for('search', search=search))

@app.route('/search/<search>', methods=['GET', 'POST'])
def search(search):
    if request.method == 'GET':
        isbn = db.execute("SELECT isbn FROM booksList WHERE isbn = :search OR title = :search OR author = :search", {"search": search}).fetchone()
        title = db.execute("SELECT title FROM booksList WHERE isbn = :search OR title = :search OR author = :search",{"search": search}).fetchone()
        author = db.execute("SELECT author FROM booksList WHERE isbn = :search OR title = :search OR author = :search",{"search": search}).fetchone()
        year = db.execute("SELECT year FROM booksList WHERE isbn = :search OR title = :search OR author = :search",{"search": search}).fetchone()
        username = session['user']
        return render_template('results.html', isbn=isbn[0], title=title[0], author=author[0], year=year[0], username=username)
    else:
        isbn = request.header('isbn')
        print(isbn)
        return redirect(url_for('book', isbn=isbn))

@app.route("/book/<isbn>", methods=['GET', 'POST'])
def book(isbn):
    if request.method == 'GET':
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "YyLgmPuVjytu4377OeIjLg", "isbns": isbn})
        response = res.json()
        bookInfo = db.execute("SELECT isbn, title, author, year FROM booksList WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
        username = session['user']
        reviews = db.execute("SELECT username, rating, review FROM reviews WHERE bookId = :isbn", {"isbn": isbn}).fetchall()
        return render_template('reviews.html', response=response, bookInfo=bookInfo, username=username, reviews=reviews)
    else:
        review = request.form.get('review')
        rating = request.form.get('rating')
        user = session['user']
        db.execute("INSERT INTO reviews (bookId, username, rating, review) VALUES(:bookId, :user, :rating, :review)", {"bookId":isbn, "user":user, "rating":rating, "review":review})
        db.commit()
        return redirect(url_for('book', isbn=isbn))

@app.route("/api/<isbn>")
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "YyLgmPuVjytu4377OeIjLg", "isbns": isbn})
    bookInfo = db.execute("SELECT isbn, title, author, year FROM booksList WHERE isbn = :isbn",
                          {"isbn": isbn}).fetchall()
    if bookInfo:
        response = res.json()
        return response
    else:
        return ("Invalid ISBN. Please Check")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('loginUser'))

#run
if __name__ == "__main__":
    app.run()