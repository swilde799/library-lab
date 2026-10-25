from pymongo import MongoClient

MONGO_URI = "mongodb://127.0.0.1:27017/"
DB_NAME = "library"

_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        _client.admin.command("ping")
    return _client

def get_db():
    return get_client()[DB_NAME]

def get_collection(name):
    return get_db()[name]

def get_borrow_collection():
    """
    优先使用普通镜像集合 borrow_logs_plain，
    便于完成 update/delete 和 $lookup。
    如果没有镜像集合，则退回时间序列集合 borrow_logs。
    """
    db = get_db()
    names = db.list_collection_names()
    if "borrow_logs_plain" in names:
        return db["borrow_logs_plain"]
    return db["borrow_logs"]

def close():
    global _client
    if _client is not None:
        _client.close()
        _client = None