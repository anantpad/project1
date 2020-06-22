import csv
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))

# Creating a table called booksList, with columns: ISBN, title, author, and year
def main():
    db.execute("CREATE TABLE booksList (id SERIAL, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")
    print("Table booksList created successfully")
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO booksList (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn":isbn, "title":title, "author":author, "year":year})
        print(f"Added {title} by {author}, published in {year} and has ISBN value of {isbn}")
    db.commit()

#run
if __name__ == "__main__":
    main()