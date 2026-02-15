from pymongo import MongoClient
from config.settings import settings

client = MongoClient(settings.DATA_LAKE_DB_URI)
db = client["MLOps"]
collection = db["jobs"]