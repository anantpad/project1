import csv
from pymongo import MongoClient

client = MongoClient("mongodb://sridhar:asdf@cluster0-shard-00-00-aou9c.mongodb.net:27017,cluster0-shard-00-01-aou9c.mongodb.net:27017,cluster0-shard-00-02-aou9c.mongodb.net:27017/goodreads?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.goodreads
coll = db.bookLists

reader = csv.DictReader(open("C:/Users/srramachandran/OneDrive/PythonProjects/goodReads/books.csv"))
result = {}
ordered_dict_from_Csv = []
for row in reader:
    coll.insert_one(dict(row.items()))
    print(dict(row.items()))

    # ordered_dict_from_Csv.append(list(reader))
    # print(ordered_dict_from_Csv)
# dict_from_Csv = dict(ordered_dict_from_Csv)
# print(dict_from_Csv)