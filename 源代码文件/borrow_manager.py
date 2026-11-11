from db_config import DBConfig
db = DBConfig.get_db()

def get_borrow_logs_by_reader(card_no):
    return db.borrow_logs.count_documents({"reader_card": card_no})

def get_borrow_log_count():
    return db.borrow_logs.count_documents({})
