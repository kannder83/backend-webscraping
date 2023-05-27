from pymongo import MongoClient
from config.conf import settings

mongo_user = settings.database_username
mongo_pass = settings.database_password
mongo_host = settings.database_hostname
mongo_port = settings.database_port

if settings.debug:
    URL = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/admin?verbose=true"
else:
    URL = f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/admin"


if settings.debug:
    db_client = MongoClient(URL).test
else:
    db_client = MongoClient(URL).webscraping
