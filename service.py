from flask import Flask
from flask_pymongo import pymongo


CONNECTION_STRING = "mongodb+srv://root:abcd1234@quasi-gamers.ayeicnx.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('QuasiGamers')
user_collection = pymongo.collection.Collection(db, 'analytics')