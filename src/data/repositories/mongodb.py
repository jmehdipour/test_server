from datetime import datetime

from data.connections.mongodb import mongo_db


def save_sum_in_db(a: int, b: int, sum_value):
    mongo_db['sums'].insert_one({"a": a, "b": b, "sum": sum_value, "createdAt": datetime.now()})
    return True


# cache
def get_sum_history(offset, limit):
    return list(mongo_db['sums'].find({}, {"a": 1, "b": 1, "_id": 0}).skip(offset).limit(limit))
