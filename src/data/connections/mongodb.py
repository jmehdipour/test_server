import pymongo
from config import get_settings

my_client = pymongo.MongoClient(get_settings().mongo_url)
mongo_db = my_client[get_settings().mongo_db_name]
sum_collection = mongo_db["sums"]
