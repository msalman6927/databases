from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("db_url"))
db = client["fb_app"]

users_col = db["users"]
posts_col = db["posts"]
friends_col = db["friends"]
