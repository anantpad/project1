# Project 1

Web Programming with Python and JavaScript

application.py: This is the main file that defines the routes for the various pages in my project. 
app.py: This is just a mimic of the application.py file. 
books.csv: This is the file with the entire list of books
import.py: This is the python code I wrote to import the csv file with the list of books to a SQL database. 
models.py: This is just a file defining classes that can connect with the SQL database and function but it is not really used in this project. 

Under templates, 
register.html: This is the first page and allows user to register their account to read and write reviews for the books. 
login.html: This is the page where the user can use their login username and password to login to the website, write, and read reviews. 
home.html: This is the first page that the user would be led into right after logging in to the website. The primary function of this page is to allow the user to search for books
results.html: This is the page that displays the results searched by the user in home.html. The main functionality of this page is to allow for the user to select a book from results. 
reviews.html: This is the page that displays detailed information for the book selected. The user may read reviews for the selected book, write reviews and rate the book

The user may also type "/api/<isbn>" and search for the particular book to receive a json format of information. 
