from datetime import datetime
from pymongo import MongoClient

class DBConfig:
    _client = None

    @classmethod
    def get_db(cls):
        if cls._client is None:
            cls._client = MongoClient("mongodb://localhost:27017")
        return cls._client["library"]

    @classmethod
    def log_action(cls, action, collection, detail=""):
        db = cls.get_db()
        db.audit_logs.insert_one({
            "action": action,
            "collection": collection,
            "detail": detail,
            "timestamp": datetime.now()
        })
