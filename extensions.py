from pymongo import MongoClient

client = MongoClient("")
db = client["test"]
users_collection = db["users"]
