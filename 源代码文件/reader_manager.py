from db_config import DBConfig
db = DBConfig.get_db()

def get_all_readers_paged(page=1, size=10):
    skip = (page - 1) * size
    return list(db.readers.find({}, {"_id": 0}).skip(skip).limit(size))

def get_reader_count():
    return db.readers.count_documents({})
