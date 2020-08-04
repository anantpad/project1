import requests
from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.debug = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/goodreads?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
# app.config["MONGO_URI"] = "mongodb://sridhar:asdf@cluster0-aou9c.mongodb.net/test?retryWrites=true&w=majority"
mongo = PyMongo(app)

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
        checkEmail = mongo.db.registrations.find_one({"email":email})
        checkUsername = mongo.db.registrations.find_one({"username": username})
        if checkEmail and checkUsername:
            return redirect("/")
        elif checkUsername:
            return redirect("/")
        elif checkEmail:
            return redirect("/")
        elif name == "" or username == "" or password == "" or email == "":
            return redirect("/")
        else:
            mongo.db.registrations.insert_one(
                {"name": name, "username": username, "password": password, "email": email})
            return redirect("/login")

@app.route('/login', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        checkUsername = mongo.db.registrations.find_one({"username": username, "password":password})
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
        isbn = mongo.db.bookList.find_one({"search": search})
        title = mongo.db.bookList.find_one({"search": search})
        author = mongo.db.bookList.find_one({"search": search})
        year = mongo.db.bookList.find_one({"search": search})
        username = session['user']
        return render_template('results.html', isbn=isbn[0], title=title[0], author=author[0], year=year[0], username=username)
    else:
        isbn = request.header('isbn')
        print(isbn)
        return redirect(url_for('book', isbn=isbn))

@app.route("/book/<isbn>", methods=['GET', 'POST'])
def book(isbn):
    if request.method == 'GET':
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": isbn})
        response = res.json()
        bookInfo = mongo.db.bookList.find({"isbn": isbn})
        username = session['user']
        reviews = mongo.db.bookList.find({"isbn": isbn})
        return render_template('reviews.html', response=response, bookInfo=bookInfo, username=username, reviews=reviews)
    else:
        review = request.form.get('review')
        rating = request.form.get('rating')
        user = session['user']
        mongo.db.insert_one(
            {"bookId":isbn, "user":user, "rating":rating, "review":review})
        return redirect(url_for('book', isbn=isbn))

@app.route("/api/<isbn>")
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "KEY", "isbns": isbn})
    bookInfo = mongo.db.bookList.find({"isbn": isbn})
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