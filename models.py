from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Registrations(db.Model):
    __tablename__ = "registrations"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

class books(db.Model):
    __tablename__ = "booksList"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)

hjahjkasjaskdhfkj
