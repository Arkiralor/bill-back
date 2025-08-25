from pymongo import MongoClient
from config.global_settings import global_settings

cluster = MongoClient(str(global_settings.MONGO_URL))
database = cluster[global_settings.MONGO_NAME]